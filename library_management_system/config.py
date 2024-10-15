import os
from dotenv import load_dotenv 

# Load environment variables from .env file
load_dotenv()

# Database configuration
class Config:
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'library_user'),
        'password': os.getenv('DB_PASSWORD', 'password123'),  
        'database': os.getenv('DB_NAME', 'library_management_system'),          
        'port': int(os.getenv('DB_PORT', 3306))
    }

    # Application settings
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    
    # File paths
    LOG_FILE = os.getenv('LOG_FILE', 'library.log')

    # Other application-specific settings
    @classmethod  
    def get_db_uri(cls):
        return f"mysql://{cls.DB_CONFIG['user']}:{cls.DB_CONFIG['password']}@{cls.DB_CONFIG['host']}:{cls.DB_CONFIG['port']}/{cls.DB_CONFIG['database']}"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DB_CONFIG = Config.DB_CONFIG.copy()
    DB_CONFIG['database'] = 'test_' + DB_CONFIG['database']

def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig