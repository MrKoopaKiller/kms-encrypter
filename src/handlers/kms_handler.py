import base64
import boto3
import botocore
import logging

class KmsHandler:
    def __init__(self, profile_name, region):
        self.region = region
        self.profile_name = profile_name
        self.session = self._session(profile_name, region)

    # Create a AWS session
    def _session(self, profile_name, region):
        try:
            session = boto3.Session(profile_name=profile_name, region_name=region)
        except botocore.exceptions.ProfileNotFound:
            logging.error(f"[ERROR] Profile '{profile_name}' not found")
            exit(1)
        return session
    
    # Get list of all KMS keys
    def list_keys(self):
        kms = self.session.client("kms")
        return kms.list_keys()

    # Get list of all KMS aliases
    def list_aliases(self):
        kms = self.session.client("kms")
        aliases = []
        for alias in kms.list_aliases()["Aliases"]:
            if alias.get("TargetKeyId"):
                aliases.append(alias)
        return aliases

    # Search key_arn in list of all KMS keys by alias
    def search_key_arn(self, key_alias):
        for alias in self.list_aliases():
            if alias.get("AliasName").endswith(key_alias):
                for key in self.list_keys()["Keys"]:
                    if alias.get("TargetKeyId") in key.get("KeyId"):
                        return key.get("KeyArn")
        return None

    def _context(self, context):
        if context is None:
            return {}

        encryption_context = {}
        for item in context.split(","):
            key, value = item.split("=")
            encryption_context[key] = value
        return encryption_context

    # Encrypt a string with a KMS key
    def encrypt(self, key_id, plaintext, context):
        kms = self.session.client("kms")
        encryption_context = self._context(context)
        result = kms.encrypt(
            KeyId=key_id,
            Plaintext=bytes(plaintext, "utf-8"),
            EncryptionContext=encryption_context,
        )
        return base64.b64encode(result.get("CiphertextBlob")).decode("utf-8")

    def decrypt(self, ciphertext, context):
        kms = self.session.client("kms")
        encryption_context = self._context(context)
        result = kms.decrypt(
            CiphertextBlob=bytes(base64.b64decode(ciphertext)),
            EncryptionContext=encryption_context,
        )
        return result.get("Plaintext").decode("utf-8")