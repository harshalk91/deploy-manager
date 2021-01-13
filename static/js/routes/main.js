routes = (typeof routes != 'undefined' && routes instanceof Array) ? routes : [];

routes = routes.concat([
    {
        'url': '/',
        'templateUrl': 'static/views/homepage.html',
        'controller': 'HomeController'
    }
]);
