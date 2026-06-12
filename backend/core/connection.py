import mysql.connector

from dotenv import load_dotenv
import os
import pathlib

root = pathlib.Path(__file__).parent.parent
env_path = root / '.env'

load_dotenv(dotenv_path=env_path)

load_dotenv() 

def conectar_banco():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

    except mysql.connector.Error:
        raise ConnectionError(
            "Não foi possível conectar ao banco de dados."
        )