import os

# prefer storing all config variables in a class in a seperate module
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'siri-ya-wawili-si-siri'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        # 'sqlite:///' + os.path.join(basedir, 'app.db')
    
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.environ.get('DATABASE_USERNAME')}:{os.environ.get('DATABASE_PASSWORD')}"
        f"@{os.environ.get('DATABASE_HOST')}:{os.environ.get('DATABASE_PORT')}/{os.environ.get('DATABASE_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False