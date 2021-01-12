from services.MongoService import MongoService

class DeploymentService:
    def __init__(self):
        self.mongo_service = MongoService()

    def get_all_deployments(self):
        print("I am under getting all deployments")

    def get_cloud_provider_deployments(self, cloud_provider=None):
        print(f"I am fetching deployments for provider - {cloud_provider}")

    def get_deployment(self, deployment_id=None):
        print("I am fetching details for specific deployment")

    def createDeployment(self, data=None):
        print("Create deployment ")