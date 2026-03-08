
import logging
from flask import Flask, jsonify
import psycopg2
from config.config import Config
import utils.azure_vault as vault_utils
import os

print("Starting the Flask application...")
# Logging configuration
log_dir = Config.LOG_DIR
log_file = os.path.join(log_dir, 'app.log')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file, mode='a')
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def get_db_connection():
    try:
        logger.info('Fetching database credentials from Azure Key Vault.')
        db_username, db_password = vault_utils.get_db_credentials()
        logger.info('Attempting to connect to the database.')
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            dbname=Config.DB_NAME,
            user=db_username,
            password=db_password,
            sslmode='require'
        )
        logger.info('Database connection established.')
        return conn
    except Exception as e:
        logger.error(f'Failed to connect to the database: {e}')
        raise

@app.route('/', methods=['GET'])
def get_data():
    logger.info('Received request for data.')
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        logger.info('Executing SQL query.')
        cur.execute('SELECT * FROM users;')
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        data = [dict(zip(colnames, row)) for row in rows]
        logger.info(f'Retrieved {len(data)} records from the database.')
        return jsonify(data), 200
    except Exception as e:
        logger.error(f'Error retrieving data: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        if cur:
            try:
                cur.close()
                logger.info('Database cursor closed.')
            except Exception as e:
                logger.warning(f'Error closing cursor: {e}')
        if conn:
            try:
                conn.close()
                logger.info('Database connection closed.')
            except Exception as e:
                logger.warning(f'Error closing connection: {e}')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
