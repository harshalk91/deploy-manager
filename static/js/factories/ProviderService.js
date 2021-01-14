configApp.factory('ProviderService',
    ['$http', '$q',
        function ($http, $q) {
            var service = {};

            service.getCloudProvidersData = function (show_waiting) {
                var delay = $q.defer();

                if (show_waiting) {
                    waitingDialog.show('Please Wait...');
                }

                $http({
                    method: 'GET',
                    params: {'foobar': new Date().getTime()},
                    url: "/api/providers"
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

                    delay.reject(data);
                });
                return delay.promise;
            };

            service.getProvider = function (provider_id, show_waiting) {
                var delay = $q.defer();

                if (show_waiting) {
                    waitingDialog.show('Please Wait...');
                }

                $http({
                    method: 'GET',
                    params: {'foobar': new Date().getTime()},
                    url: "/api/config/provider/" + provider_id
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

                    delay.reject(data);
                });
                return delay.promise;
            };

            return service;
        }]);