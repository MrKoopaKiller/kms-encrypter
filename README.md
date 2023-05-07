# KMS Encrypter

## Description

This is a simple Flask web application that allows you to encrypt data using AWS KMS.

It is usefeul to encrypt secrets to commit in a repository, since the only one that can decrypt the data is who has access to the KMS key.

The motivation for this project is to provide a simple way to encrypt data to be used in [Terraform](https://www.terraform.io/) projects.

## How it works

It uses the AWS SDK for Python (Boto3) to connect to AWS KMS and encrypt the data. The encrypted data is displayed in the web page and can be copied to the clipboard. **The data is not stored anywhere.**


## How to use

1. **Authenticate** - The index page is protected by a login form. The user and password are defined by `APP_ADMIN_EMAIL` and `APP_ADMIN_PASSWORD` environment variables. Check the default values in the [Environment variables](#environment-variables) section.
2. **List KMS keys** - After login, the user can select the account and region and click on the `List Keys` button to list the available KMS keys.

3. **Encrypt** - The user can type the data to be encrypted ib the textarea box and click on the `Encrypt` button. It's also possible to define the encryption context to be used in the ecnryption process. 

The encryption context is a set of key-value pairs that are used to check for data integrity. 

When you decrypt data, you **must** specify the same encryption context that you specified when you encrypted the data. Otherwise, the request to decrypt the data will fail. The encryption context is optional.

4. The encrypted data will be displayed in the second box below the `Encrypt` button. Click on the `Copy` button to copy the encrypted data to the clipboard.

## Environment variables

| Variable | Description | Default value |
|----------|-------------|---------------|
| `APP_ADMIN_EMAIL` | Admin email | `admin@admin.com` |
| `APP_ADMIN_PASSWORD` | Admin password | `Admin123` |
| `APP_CONFIG_FILE` | Configuration file | `config.yaml` |
| `APP_DEBUG` | Debug mode | False |
| `APP_SECRET_KEY`  | Secret key | `pf9Wkove4IKEAXvy-cQkp0rkv9Cb3Ag-wyJILbq_dFw` |
| `APP_SECURITY_PASSWORD_SALT`  | Password salt | `146585145368132386173225678016728509634` |
| `SQLALCHEMY_DATABASE_URI` | Database URI | sqlite:///myapp.db |

## Configuration file

There is a configuration file called `config.yaml` that can be used to configure the regions and accounts that will be displayed in the web page.
It has a simple format:

```yaml
regions:
  - us-east-1
  - eu-central-1
  - eu-north-1

accounts:
  - default
```

The accounts should exist in the `~/.aws/credentials` file. Check the [AWS CLI documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) for more information.

## Docker-compose

There is a `docker-compose.yml` file that can be used to run the application in a container.
In order to load the aws configuration correctly, you need to mount two files in the container: the `~/.aws` directory in the container and the `config.yaml` with the regions and accounts you want to display. (It will be improved in the future)

The application runs under a non-root user called `nonroot` with UID 1000. The container exposes the port 5000.

The docker-compose is configured to mount the `config_local.yaml` file as `config.yaml` in the conteiner, also mounrting  the `~/.aws` directory.
Change this configuration according to your needs.

Start the container with:

```bash
docker-compose up -d
```

The output should be something like this:

```bash
Creating kmsencrypter_web_1 ... done
Attaching to kmsencrypter_web_1
web_1  |  * Debug mode: off
web_1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
web_1  |  * Running on all addresses (0.0.0.0)
web_1  |  * Running on http://127.0.0.1:5000
web_1  |  * Running on http://172.19.0.2:5000
web_1  | Press CTRL+C to quit
```

You can now access http://127.0.0.1:5000 in your browser and do the login with the user and password defined in the docker-compose file. Default values are `dev@company.com` and `ItWorks-0n-my-pc`.

## Kubernetes deployment
> TODO

There is a `k8s` directory with the Kubernetes deployment files. You can use them to deploy the application in a Kubernetes cluster.

Adjust the `configmap.yaml` file to match your needs. The aws configuration can be used as a secret. Check the `secret.yaml` file.