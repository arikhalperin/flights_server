import os

from flask import Flask

from app import create_app
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./app/UTILS/google_creds.json"
app = create_app()