import os

APP_ENV = os.getenv('APP_ENV', 'development')

DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'admin')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'admin')

DATABASE_HOST = os.getenv('DATABASE_HOST', '127.0.0.1')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'fastapi_ecom')

TEST_DATABASE_NAME = os.getenv('DATABASE_NAME', 'test_fastapi_ecom')
