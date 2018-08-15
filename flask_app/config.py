import os
from whoosh.analysis import StemmingAnalyzer

class Config:
    ### Turn these into environment variables later
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "postgresql://jack:1399@localhost:5432/codon"
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    ### Stripe
    CLIENT_SECRET = "sk_test_dZBIm0mCoNKvRb3P503B2sE2"

    MSEARCH_INDEX_NAME = "whoosh_index"
    # simple,whoosh
    MSEARCH_BACKEND = "whoosh"
    # auto create or update index
    MSEARCH_ENABLE = True
