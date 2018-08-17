import os
import flask_app.keys as keys
from whoosh.analysis import StemmingAnalyzer

class Config:
    ### Turn these into environment variables later
    SECRET_KEY = keys.sec_key
    SQLALCHEMY_DATABASE_URI = keys.db_uri
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = keys.mail_user
    MAIL_PASSWORD = keys.mail_pass

    ### Stripe
    CLIENT_SECRET = keys.stripe_client_key
    ### Whoosh Search
    MSEARCH_INDEX_NAME = "whoosh_index"
    # simple,whoosh
    MSEARCH_BACKEND = "whoosh"
    # auto create or update index
    MSEARCH_ENABLE = True
