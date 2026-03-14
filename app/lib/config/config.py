import os

class Config:
	ENV = os.getenv('APP_ENV', 'dev')
	if ENV == 'dev':
		DB_HOST = os.getenv('DB_HOST', 'lab-db.postgres.database.azure.com')
		DB_PORT = int(os.getenv('DB_PORT', 5432))
		DB_NAME = os.getenv('DB_NAME', 'flaskappdb')
		LOG_DIR = os.getenv('LOG_DIR', '/home/LogFiles')
	else:
		DB_HOST = os.getenv('DB_HOST')
		DB_PORT = int(os.getenv('DB_PORT', 5432))
		DB_NAME = os.getenv('DB_NAME')
		LOG_DIR = os.getenv('LOG_DIR', '/var/log/app')
