import json
import os
from urllib.parse import quote_plus

import boto3


def get_database_url():
    secret_arn = os.getenv("DATABASE_SECRET_ARN")

    if not secret_arn:
        return None

    region = os.getenv("AWS_REGION", "eu-central-1")

    client = boto3.client(
        "secretsmanager",
        region_name=region
    )

    response = client.get_secret_value(
        SecretId=secret_arn
    )

    secret = json.loads(response["SecretString"])

    username = quote_plus(secret["username"])
    password = quote_plus(secret["password"])
    host = secret["host"]
    port = secret["port"]
    database = secret["dbname"]

    return (
        f"postgresql+psycopg://{username}:{password}"
        f"@{host}:{port}/{database}?sslmode=require"
    )