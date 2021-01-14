from db_queries.DeploymentQuery import DeploymentQuery
from sqlalchemy import orm
from db_queries import engine

class AWSService:
    def __init__(self):
        self.deployment_query = DeploymentQuery()

    def get_all_aws_deployments(self, provider_id=None):
        deployments = []
        sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False, expire_on_commit=True)
        db_session = orm.scoped_session(sm)
        deployments_res = self.deployment_query.get_all(session=db_session)
        db_session.close()
        if deployments_res:
            for deployment in deployments_res:
                deployment_dict = dict()
                deployment_dict['id'] = deployment.id
                deployment_dict['name'] = deployment.name
                deployment_dict['description'] = deployment.description
                deployment_dict['state'] = deployment.state
                deployment_dict['created_by'] = deployment.created_by
                deployment_dict['created_date'] = deployment.created_date
                deployments.append(deployment_dict)

        return deployments