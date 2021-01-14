from services.DatabaseService import DatabaseService

class AWSService:
    def __init__(self):
        self.db_service = DatabaseService()

    def get_all_aws_deployments(self):
        print("I am under getting all deployments")

    def get_aws_deployment(self, provider=None, deployment_id=None):
        print("I am fetching details for specific deployment from aws")