configApp.controller('AWSDeploymentsController',
    ['$scope', '$window', '$route', 'data', 'AWSDeploymentService', 'DTOptionsBuilder',
        function ($scope, $window, $route, data, deploymentService, DTOptionsBuilder) {

            $scope.dtOptions = DTOptionsBuilder.newOptions().withOption('order', []);
            $scope.deployments = data;
            $scope.provider_id = $route.current.params.id;

            $scope.view = function (e, deployment_id) {
                e.stopPropagation();

                location.href = "#aws/deployment/" + deployment_id;
                return false;
            }


        }]);
