angular.module('starter.controllers', [])

.controller('AppCtrl', function($scope, $ionicModal, $timeout) {

  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //$scope.$on('$ionicView.enter', function(e) {
  //});

  // Form data for the login modal
  $scope.loginData = {};

  // Create the login modal that we will use later
  $ionicModal.fromTemplateUrl('templates/login.html', {
    scope: $scope
  }).then(function(modal) {
    $scope.modal = modal;
  });

  // Triggered in the login modal to close it
  $scope.closeLogin = function() {
    $scope.modal.hide();
  };

  // Open the login modal
  $scope.login = function() {
    $scope.modal.show();
  };

  // Perform the login action when the user submits the login form
  $scope.doLogin = function() {
    console.log('Doing login', $scope.loginData);

    // Simulate a login delay. Remove this and replace with your login
    // code if using a login system
    $timeout(function() {
      $scope.closeLogin();
    }, 1000);
  };
})

.controller('CitationsCtrl', function($scope, $http) {
    $scope.citations = []
    $http({
      method: 'POST',
      url: "http://ffdd892f.ngrok.io",
      transformRequest: function(obj) {
        var str = [];
        for(var p in obj)
        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
        return str.join("&");
      },
      data: {From: "+16504408236", Body: 'CITATIONS'},
      headers: {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    }).then(function(resp) {
        console.log(resp.data)
        var re = /(.*<Sms>)([\s\S]*)(<\/Sms>.*)/;
        var body = resp.data.replace(re, "$2");

        citations = body.split('\n')

        angular.forEach(citations, function(citation) {
          if (citation != '') {
            $scope.citations.push({
              title: citation
            })
          }
        });
      });
})

.controller('PlaylistCtrl', function($scope, $stateParams) {
})

.controller('ViolationsCtrl', function($scope, $http) {
    $scope.violations = []
    $http({
      method: 'POST',
      url: "http://ffdd892f.ngrok.io",
      transformRequest: function(obj) {
        var str = [];
        for(var p in obj)
        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
        return str.join("&");
      },
      data: {From: "+16504408236", Body: 'VIOLATIONS'},
      headers: {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    }).then(function(resp) {
        console.log(resp.data)
        var re = /(.*<Sms>)([\s\S]*)(<\/Sms>.*)/;
        var body = resp.data.replace(re, "$2");

        violations = body.split('\n')

        angular.forEach(violations, function(violation) {
          if (violation != '') {
            $scope.violations.push({
              title: violation
            })
          }
        });
      });
})

.controller('WarrantsCtrl', function($scope, $http) {
    $scope.warrants = []
    $http({
      method: 'POST',
      url: "http://ffdd892f.ngrok.io",
      transformRequest: function(obj) {
        var str = [];
        for(var p in obj)
        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
        return str.join("&");
      },
      data: {From: "+16504408236", Body: 'WARRANTS'},
      headers: {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    }).then(function(resp) {
        console.log(resp.data)
        var re = /(.*<Sms>)([\s\S]*)(<\/Sms>.*)/;
        var body = resp.data.replace(re, "$2");

        warrants = body.split('\n')

        angular.forEach(warrants, function(warrant) {
          if (warrant != '') {
            $scope.warrants.push({
              title: warrant
            })
          }
        });
      });
})

.directive('input', function($timeout) {
  return {
    restrict: 'E',
    scope: {
      'returnClose': '=',
      'onReturn': '&',
      'onFocus': '&',
      'onBlur': '&'
    },
    link: function(scope, element, attr) {
      element.bind('focus', function(e) {
        if (scope.onFocus) {
          $timeout(function() {
            scope.onFocus();
          });
        }
      });
      element.bind('blur', function(e) {
        if (scope.onBlur) {
          $timeout(function() {
            scope.onBlur();
          });
        }
      });
      element.bind('keydown', function(e) {
        if (e.which == 13) {
          if (scope.returnClose) element[0].blur();
          if (scope.onReturn) {
            $timeout(function() {
              scope.onReturn();
            });
          }
        }
      });
    }
  }
})

.controller('ChatCtrl', function($scope, $timeout, $http, $ionicScrollDelegate) {

  $scope.hideTime = true;

  var alternate,
    isIOS = ionic.Platform.isWebView() && ionic.Platform.isIOS();

  $scope.sendMessage = function() {

    var d = new Date();
    d = d.toLocaleTimeString().replace(/:\d+ /, ' ');

    var body = $scope.data.message;
    $scope.messages.push({
      mine: true,
      text: body,
    });

    delete $scope.data.message;

    $http({
      method: 'POST',
      url: "http://ffdd892f.ngrok.io",
      transformRequest: function(obj) {
        var str = [];
        for(var p in obj)
        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
        return str.join("&");
      },
      data: {From: "+16504408236", Body: body},
      headers: {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    }).then(function(resp) {
        console.log(resp.data)
        var re = /(.*<Sms>)([\s\S]*)(<\/Sms>.*)/;
        var body = resp.data.replace(re, "$2");

        $scope.messages.push({
          mine: false,
          text: body
        });

        $ionicScrollDelegate.scrollBottom(true);
      });

    $ionicScrollDelegate.scrollBottom(true);

  };


  $scope.inputUp = function() {
    if (isIOS) $scope.data.keyboardHeight = 216;
    $timeout(function() {
      $ionicScrollDelegate.scrollBottom(true);
    }, 300);

  };

  $scope.inputDown = function() {
    if (isIOS) $scope.data.keyboardHeight = 0;
    $ionicScrollDelegate.resize();
  };

  $scope.closeKeyboard = function() {
    // cordova.plugins.Keyboard.close();
  };


  $scope.data = {};
  $scope.myId = '12345';
  $scope.messages = [];

});
