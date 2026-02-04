import os

from bitwarden_sdk import (
    BitwardenClient,
    ClientSettings,
    DeviceType,
    ResponseForProjectsResponse,
    ResponseForSecretIdentifiersResponse,
    SecretIdentifiersResponse,
    ResponseForSecretResponse
)
from typing import List
from dotenv import load_dotenv


load_dotenv(overwrite = True)


# Configured when creating the Vault
access_token = os.getenv('BITWARDEN_ACCESS_TOKEN')
organization_id = os.getenv('BITWARDEN_ORGANIZATION_ID')

if not access_token or not organization_id:
    raise ValueError('You should define the env vars: BITWARDEN_ACCESS_TOKEN and BITWARDEN_ORGANIZATION_ID')

settings = ClientSettings(
    device_type = DeviceType.SDK,
    user_agent = 'python'
)

client = BitwardenClient(settings)
client.auth().login_access_token(access_token)  # authentication

# Getting all projects
#projects = client.projects().list(organization_id)
#print(projects.data)

# Getting all secrets
raw_secrets: ResponseForSecretIdentifiersResponse = client.secrets().list(organization_id)
#print(raw_secrets)
secrets: List[SecretIdentifiersResponse] = raw_secrets.data
#print(secrets)

# From each secret getting value
for secret in secrets.data:
    #print(secret)
    secret_content: ResponseForSecretResponse = client.secrets().get(id = secret.id).data
    secret_name: str = secret_content.key
    secret_value: str = secret_content.value
    print(f'Name: "{secret_name}" - Value: "{secret_value}"')
