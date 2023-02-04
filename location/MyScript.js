// myScript.js

window.onload = function() {
    alert("Welcome to my website!");
  };
  function initMap() {
    navigator.geolocation.getCurrentPosition(function(position) {
      var lat = position.coords.latitude;
      var lng = position.coords.longitude;
      var myLatLng = { lat: lat, lng: lng };
      var map = new google.maps.Map(document.getElementById("map"), {
        zoom: 8,
        center: myLatLng
      });
      var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: "User's location"
      });
    });
  }