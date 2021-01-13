configApp.controller('HeaderController',
    ['$scope', '$window', '$rootScope', '$route', '$sce', '$http', '$cookieStore', 'ConfigService',
        function ($scope, $window, $rootScope, $route, $sce, $http, $cookieStore, configService) {

            $('img').on("error", function () {
                $(this).attr('src', '/static/images/user-image.png');
            });

            get_home_page_config_promise = configService.getHomePageConfigData(true);

            get_home_page_config_promise.then(function (data) {


                $scope.providers = data.providers;
                $rootScope.providers = data.providers;
                console.log($scope.providers)

            });

            $scope.gotoSoftware = function (code) {

                location.href = "#" + code + "/";

            };

            $(".dropdown").hover(
                function () {
                    $('.dropdown-menu', this).not('.in .dropdown-menu').stop(true, true).slideDown("400");
                    $(this).toggleClass('open');
                },
                function () {
                    $('.dropdown-menu', this).not('.in .dropdown-menu').stop(true, true).slideUp("400");
                    $(this).toggleClass('open');
                }
            );

            $scope.logoutClick = function () {
                $('#logoutmodal').modal('toggle');
                $cookieStore.remove('iPlanetDirectoryPro');
                $window.location.assign('/logout');
            };

            $scope.goTo = function (target) {

                if (target == 'authorization') {
                    location.href = "#auth";
                }
                if (target == 'config') {
                    location.href = "#config";
                }


            }

        }]);

configApp.directive('checkauth', ['$timeout', 'AuthService', function ($timeout, authService) {
    return function ($scope, $element, $attrs) {

        if ($scope.$root.functions == null) {

            get_loggedin_user_function_promise = authService.getLoggedInUserFunctions(true);

            get_loggedin_user_function_promise.then(function (data) {
                $scope.$root.functions = data;
                if ($element[0].attributes.f_id && $scope.$root.functions.indexOf($element[0].attributes.f_id.value) == -1) {
                    $($element[0]).addClass("disabled");
                } else {
                    $($element[0]).removeClass("disabled");
                }
            });
        } else {
            if ($element[0].attributes.f_id && $scope.$root.functions.indexOf($element[0].attributes.f_id.value) == -1) {
                $($element[0]).addClass("disabled");
            } else {
                $($element[0]).removeClass("disabled");
            }
        }


    }
}]);
