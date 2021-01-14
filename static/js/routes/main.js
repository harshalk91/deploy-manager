routes = (typeof routes != 'undefined' && routes instanceof Array) ? routes : [];

routes = routes.concat([
    {
        'url': '/',
        'templateUrl': 'static/views/homepage.html',
        'controller': 'HomeController'
    },
    {
        'url': '/aws-deployments',
        'templateUrl': 'static/views/deployments.html',
        'resolve': {
            data: ['AWSDeploymentService', '$route', function (deploymentService, $route) {
                return deploymentService.get_deployments($route.current.params.id, true);
            }]
        },
        'controller': 'AWSDeploymentsController'
    }
]);
