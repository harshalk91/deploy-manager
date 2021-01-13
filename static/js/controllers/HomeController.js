configApp.controller('HomeController', ['$rootScope', '$scope', '$http', function ($rootScope, $scope, $http) {


    $scope.$watch(function () {
        return $rootScope.providers;
    }, function () {
        $scope.providers = $rootScope.providers;
    }, true);


    $scope.goToProvider = function (code, id) {

        location.href = "#" + code + "/?id=" + id;

    };

}]);
