import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-me'
    
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_PORT = os.environ.get('DB_PORT') or '5432'
    DB_NAME = os.environ.get('DB_NAME') or 'NodeHub'  
    DB_USER = os.environ.get('DB_USER') or 'postgres'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'admin'
    
    @property
    def DB_DSN(self):
        return (
            f"host={self.DB_HOST} "
            f"port={self.DB_PORT} "
            f"dbname={self.DB_NAME} "
            f"user={self.DB_USER} "
            f"password={self.DB_PASSWORD} "
            f"client_encoding=UTF8"       
        )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False