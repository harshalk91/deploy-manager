routes = (typeof routes != 'undefined' && routes instanceof Array) ? routes : [];

routes = routes.concat([
    {
        'url': '/',
        'templateUrl': '../../../templates/index.html',
        'controller': 'HomeController'
    }
]);
