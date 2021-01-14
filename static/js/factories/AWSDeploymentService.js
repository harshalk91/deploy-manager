configApp.factory('AWSDeploymentService',
    ['$http', '$q',
        function ($http, $q) {
            var service = {};

            service.get_deployments = function (query, show_waiting) {
                var delay = $q.defer();

                if (show_waiting) {
                    waitingDialog.show('Please Wait...');
                }


                $http({
                    method: 'GET',
                    params: {
                        'foobar': new Date().getTime(),
                        'query': query
                    },
                    url: "/api/aws/deployments"
                }).success(function (data, status, headers, config) {
                    // this callback will be called asynchronously
                    // when the response is available
                    if (show_waiting) {
                        waitingDialog.hide();
                        $('.modal-backdrop').remove();
                        waitingDialog.hide();
                    }

                    delay.resolve(data);
                }).error(function (data, status, headers, config) {
                    // called asynchronously if an error occurs
                    // or server returns response with an error status.
                    if (show_waiting) {
                        waitingDialog.hide();
                        $('.modal-backdrop').remove();
                    }
                    $("#error-alert").fadeTo(2000, 500).slideUp(500, function () {
                        $("#success-alert").slideUp(500);
                    });

                    delay.reject(data);
                });
                return delay.promise;
            };

            return service;
        }]);