from flask import Flask
import os

app = Flask(__name__)
if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

if not os.path.exists(app.config["DOC_UPLOADS"]):
    os.makedirs(app.config["DOC_UPLOADS"])

from app import views