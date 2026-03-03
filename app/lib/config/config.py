import os

class Config:
	ENV = os.getenv('APP_ENV', 'dev')
	if ENV == 'dev':
		DB_HOST = os.getenv('DB_HOST', 'lab-db.postgres.database.azure.com')
		DB_PORT = int(os.getenv('DB_PORT', 5432))
		DB_NAME = os.getenv('DB_NAME', 'flaskappdb')
		DB_USER = os.getenv('DB_USER', 'pgadminuser')
		DB_PASSWORD = os.getenv('DB_PASSWORD', '')
		LOG_DIR = os.getenv('LOG_DIR', '/home/azureuser/myapi/logs')
	else:
		DB_HOST = os.getenv('DB_HOST')
		DB_PORT = int(os.getenv('DB_PORT', 5432))
		DB_NAME = os.getenv('DB_NAME')
		DB_USER = os.getenv('DB_USER')
		DB_PASSWORD = os.getenv('DB_PASSWORD')
		LOG_DIR = os.getenv('LOG_DIR', '/var/log/app')
