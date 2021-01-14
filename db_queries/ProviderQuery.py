from datetime import datetime
from db_queries import base

providers = base.classes.providers

class ProviderQuery:
    def __init__(self):
        pass

    def get(self, provider_id=None, session=None):
        return session.query(providers).filter_by(id=provider_id).all()

    def get_all(self, session=None):
        return session.query(providers).filter_by(enable='True').order_by(providers.created_date.desc()).all()