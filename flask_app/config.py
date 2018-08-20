import os
import flask_app.keys as keys
from whoosh.analysis import StemmingAnalyzer

class Config:
    ### Turn these into environment variables later
    SECRET_KEY = keys.sec_key
    SQLALCHEMY_DATABASE_URI = keys.db_uri
    MAIL_SERVER = "mail.privateemail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
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
    ### Recaptcha
    RECAPTCHA_ENABLED = True
    RECAPTCHA_PUBLIC_KEY = keys.rc_pub_key
    RECAPTCHA_PRIVATE_KEY = keys.rc_priv_key
