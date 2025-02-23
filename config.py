import os

# prefer storing all config variables in a class in a seperate module
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'siri-ya-wawili-si-siri'