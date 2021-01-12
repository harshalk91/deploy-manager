class ProviderService:
    def __init__(self):
        pass

    def get_all_providers(self):
        providers = [
            {'name': 'AWS', 'description': 'AWS Cloud Provider', 'icon': 'aws'},
            {'name': 'GCP', 'description': 'Google Cloud Provider', 'icon': 'google'},
            {'name': 'Azure', 'description': 'Microsoft Azure Cloud Provider', 'icon': 'microsoft'},
        ]

        return providers