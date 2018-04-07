angular.module('starter.controllers', ["firebase"])

.controller('DashCtrl', ['$scope','$firebaseObject','$firebaseStorage','$state',function($scope, $firebaseObject,$firebaseStorage, $state){
  
 
   var myData = firebase.database().ref().child("TReal");
   $scope.data = $firebaseObject(myData.child('values'));
  console.log($scope.data);

   var storageRef = firebase.storage().ref("images/realTime.jpg");
  storage = $firebaseStorage(storageRef);
      
  storage.$getDownloadURL().then(function(url) {
     $scope.url =url;
     console.log(url);
    });
  
 
  }])


.filter('trusted', ['$sce', function ($sce) {
    return function(url) {
        return $sce.trustAsResourceUrl(url);
    };
}])



.controller('ChatsCtrl', ['$scope','$firebaseArray','$firebaseStorage','$state',function($scope, $firebaseArray, $firebaseStorage,$state ){
 
  var myData = firebase.database().ref("values");
  var VideosData = firebase.database().ref("Videos");
  $scope.data = $firebaseArray(myData);
  $scope.VideoData = $firebaseArray(VideosData);
  console.log($scope.data);
  console.log($scope.VideoData);


  // Video





 }])






.controller('ChatDetailCtrl', ["$scope", "$state" ,"$firebaseObject",'$firebaseStorage', function($scope, $state, $firebaseObject, $firebaseStorage) {
   
  
   var VideosData = firebase.database().ref("Videos");
   $scope.VideoData = $firebaseObject(VideosData.child($state.params.id));
   var NameVideo = $firebaseObject(VideosData.child($state.params.id).child("Name"));
   
   NameVideo.$loaded().then(function() {
              
              var RefVideo = NameVideo.$value; 
              console.log(NameVideo.$value); // "Name"

              var storageRefVideo = firebase.storage().ref("video/"+RefVideo+".mp4");
              storageVideo = $firebaseStorage(storageRefVideo);
    
               storageVideo.$getDownloadURL().then(function(urlVideo) {
               //$scope.urlVideo =urlVideo;

               $scope.urlVideo = urlVideo;

             
        });

   ////////////////////////  Image  /////////////

             var storageRef = firebase.storage().ref("images/"+RefVideo+".jpg");
             storage = $firebaseStorage(storageRef);
    
              storage.$getDownloadURL().then(function(url) {
                    $scope.url =url;
                    console.log(url);
              });

    //////////7////////////  Video    ///////////////

 // var storageRefVideo = firebase.storage().ref("video/"+RefVideo+".mp4");
 // storageVideo = $firebaseStorage(storageRefVideo);
    
 // storageVideo.$getDownloadURL().then(function(urlVideo) {
     //$scope.urlVideo =urlVideo;

   //  $scope.urlVideo = urlVideo;
      
     //console.log(urlVideo);
    

    });
   
 
  }])


.filter('trusted', ['$sce', function ($sce) {
    return function(url) {
        return $sce.trustAsResourceUrl(url);
    };
}])


///////////////////////////////////////


   







.controller('AccountCtrl', ["$scope", "$firebaseObject", function($scope, $firebaseObject) {    
  

    var myData = firebase.database().ref().child("TReal");
   
    $scope.open = $firebaseObject(myData.child('values'));
    console.log($scope.open);


}]);
