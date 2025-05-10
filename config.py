import os

#class Config:
#    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")
#    SQLALCHEMY_TRACK_MODIFICATIONS = False
#    SECRET_KEY = "your_secret_key"



class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:2933@localhost:5432/sensei_gpt"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
#class Config:
#    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey")
#    SQLALCHEMY_DATABASE_URI = "sqlite:///local.db"
#    SQLALCHEMY_TRACK_MODIFICATIONS = False

