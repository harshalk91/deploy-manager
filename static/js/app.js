//
var configApp = angular.module('dpaasApp', [
    'ngRoute', 'ngCookies', 'datatables', 'ui.bootstrap', 'angular.filter']);

configApp.config(['$routeProvider', function ($routeProvider) {
    angular.forEach(routes, function (r) {

        r_obj = {
            templateUrl: r.templateUrl,
            controller: r.controller
        };

        if (r.resolve) {
            r_obj['resolve'] = r.resolve;
        }
        $routeProvider.when(r.url, r_obj);


    });
    $routeProvider.otherwise({
        redirectTo: '/'
    })
}]);
