configApp.controller('HomeController', ['$rootScope', '$scope', '$http', function ($rootScope, $scope, $http) {

    console.log($rootScope);
    $scope.$watch(function () {
        return $rootScope.providers;
    }, function () {
        $scope.providers = $rootScope.providers;
    }, true);


    $scope.gotoProvider = function (code, id) {
        console.log(code);
        console.log(id);

        location.href = "#" + code + "/?id=" + id;

    };


    $scope.$on('ngRepeatReportsFinished', function (ngRepeatFinishedEvent) {
        $scope.rerunAuthCheck();

    });


}]);
