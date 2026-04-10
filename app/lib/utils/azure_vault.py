from azure.identity import DefaultAzureCredential
#from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

def get_db_credentials():
	"""
	Fetches the database username and password from Azure Key Vault.
	Returns:
		tuple: (db_username, db_password)
	"""
	vault_url = "https://lab-key-vault001.vault.azure.net/"
	#credential = ManagedIdentityCredential(client_id="f94f8e62-21ac-4eef-8faf-1ded9fb8e33d")
	credential = DefaultAzureCredential()
	client = SecretClient(vault_url=vault_url, credential=credential)
	db_username = client.get_secret("db-username").value
	db_password = client.get_secret("db-password").value
	return db_username, db_password