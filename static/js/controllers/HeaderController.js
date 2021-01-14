configApp.controller('HeaderController',
    ['$scope', '$window', '$rootScope', '$route', '$sce', '$http', '$cookieStore', 'ProviderService',
        function ($scope, $window, $rootScope, $route, $sce, $http, $cookieStore, providerService) {

            home_page_data = providerService.getCloudProvidersData(true);

            home_page_data.then(function (data) {

                $scope.providers = data;
                $rootScope.providers = data;

            });



        }]);
