from os import environ
from flask import Flask, render_template, request, jsonify
from flask_security import (
    Security,
    auth_required,
    hash_password,
    SQLAlchemySessionUserDatastore,
)
from database import db_session, init_db
from models import User, Role
from handlers.kms_handler import KmsHandler
from yaml import safe_load as yaml_load
import logging

# Check APP_DEBUG environment variable to enable debug mode
if environ.get("APP_DEBUG", "False") == "True":
    logging.basicConfig(level="DEBUG")

# Create app
app = Flask(
    __name__,
    static_url_path="",
    static_folder="web/static",
    template_folder="web/templates",
)
app.config["DEBUG"] = environ.get("APP_DEBUG", "False") == "True"
app.config["SECRET_KEY"] = environ.get(
    "APP_SECRET_KEY",
    "pf9Wkove4IKEAXvy-cQkp0rkv9Cb3Ag-wyJILbq_dFw",
)
app.config["SECURITY_PASSWORD_SALT"] = environ.get(
    "APP_SECURITY_PASSWORD_SALT",
    "146585145368132386173225678016728509634",
)
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
app.security = Security(app, user_datastore)


# Views
@app.route("/")
@auth_required()
def home():
    # Get config.yaml value
    try:
        with open(environ.get("APP_CONFIG_FILE", "config.yaml"), "r") as f:
            config = yaml_load(f)
    except FileNotFoundError:
        config = {"regions": ["Empty region"], "accounts": ["Empty account"]}

    regions = config["regions"]
    accounts = config["accounts"]

    return render_template("index.html", regions=regions, accounts=accounts)


@app.route("/api/getKMSAliases")
def get_aliases():
    # Get the account value from the request parameters
    account = request.args.get("account")
    region = request.args.get("region")
    kms = KmsHandler(profile_name=account, region=region)
    aliases = []
    for alias in kms.list_aliases():
        aliases.append(alias["AliasName"])
        
    return jsonify(aliases)


@app.route("/api/encryptData", methods=["POST"])
def encrypt_data():
    # Get the JSON data from the POST request
    data = request.get_json()
    # Get data from request
    account = data["account"]
    alias = data["alias"]
    context = data["context"]
    region = data["region"]
    text = data["input"]
    # Create a KMSHandler object
    kms = KmsHandler(profile_name=account, region=region)
    # Search for the key_arn using the alias
    key_id = kms.search_key_arn(alias)
    # Encrypt the text
    enc_text = kms.encrypt(key_id, text, context)
    
    return jsonify(encrypted=enc_text)

# Create an admin user
with app.app_context():
    adminEmail = environ.get("APP_ADMIN_EMAIL", "admin@admin.com")
    adminPassword = environ.get("APP_ADMIN_PASSWORD", "Admin123")
    init_db()
    if not app.security.datastore.find_user(email=adminEmail):
        app.security.datastore.create_user(
            email=adminEmail, password=hash_password(adminPassword)
        )
    db_session.commit()

if __name__ == "__main__":
    app.run(debug=False)
