from datetime import datetime
from db_queries import base

deployments = base.classes.deployments

class DeploymentQuery:
    def __init__(self):
        pass

    def get(self, deployment_id=None, session=None):
        return session.query(deployments).filter_by(id=deployment_id).all()

    def get_all(self, session=None):
        return session.query(deployments).order_by(deployments.created_date.desc()).all()

    def get_provider_deployment(self, provider_id=None, session=None):
        return session.query(deployments).filter_by(provider_id=provider_id).order_by(deployments.created_date.desc()).all()