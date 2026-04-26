import azure.functions as func
import psycopg2
from utils import azure_vault as vault_utils
from azure.appconfiguration import AzureAppConfigurationClient
from azure.identity import DefaultAzureCredential
import logging

def get_db_connection():
    try:
        logging.info('Fetching database credentials from Azure Key Vault.')
        db_username, db_password = vault_utils.get_db_credentials()
        logging.info('Attempting to connect to the database.')
        conn = psycopg2.connect(
            host="lab-db.postgres.database.azure.com",
            port=5432,
            dbname="flaskappdb",
            user=db_username,
            password=db_password,
            sslmode='require'
        )
        logging.info('Database connection established.')
        return conn
    except Exception as e:
        logging.error(f'Failed to connect to the database: {e}')
        raise

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="get_users")
def get_users(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        logging.info('Executing SQL query to fetch all users.')
        cur.execute('SELECT * FROM users;')
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        data = [dict(zip(colnames, row)) for row in rows]
        logging.info(f'Retrieved {len(data)} records from the database.')
        return func.HttpResponse(
            body=str(data),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error fetching users: {e}")
        return func.HttpResponse(
            f"Error fetching users: {e}",
            status_code=500
        )

@app.route(route="get_users_by_id/{id}")
def get_users_by_id(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_id = req.route_params.get('id') if hasattr(req, 'route_params') else req.params.get('id')
    if not user_id:
        return func.HttpResponse(
            "User ID is required.",
            status_code=400
        )
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        logging.info(f'Executing SQL query to fetch user with id: {user_id}.')
        cur.execute('SELECT * FROM users WHERE id = %s;', (user_id,))
        row = cur.fetchone()
        if row:
            colnames = [desc[0] for desc in cur.description]
            data = dict(zip(colnames, row))
            return func.HttpResponse(
                body=str(data),
                status_code=200,
                mimetype="application/json"
            )
        else:
            return func.HttpResponse(
                f"User not found for ID - {user_id}.",
                status_code=404
            )
    except Exception as e:
        logging.error(f"Error fetching user by id: {e}")
        return func.HttpResponse(
            f"Error fetching user by id: {e}",
            status_code=500
        )