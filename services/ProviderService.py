from db_queries.ProviderQuery import ProviderQuery
from sqlalchemy import orm
from db_queries import engine

class ProviderService:
    def __init__(self):
        self.provider_query = ProviderQuery()

    def get_all_providers(self):
        providers = []
        sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False, expire_on_commit=True)
        db_session = orm.scoped_session(sm)
        providers_res = self.provider_query.get_all(session=db_session)
        db_session.close()
        if providers_res:
            for provider in providers_res:
                provider_dict = dict()
                provider_dict['id'] = provider.id
                provider_dict['code'] = provider.code
                provider_dict['name'] = provider.name
                provider_dict['description'] = provider.description
                provider_dict['icon'] = provider.icon
                providers.append(provider_dict)

        return providers