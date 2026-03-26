
$(document).ready(
    function(){

        $('.nav').click(

            function(){
                $('.header_bottom_bar').toggleClass('open');
                $('.app_functions').toggleClass('open');
                $('.searchbox').toggleClass('open');
                // ham nav animation
                $('.bar1').toggleClass('active');
                $('.bar2').toggleClass('active');
                $('.bar3').toggleClass('active');
                $('.back-drop').show();
            }
            
        )

    }
)


// // Initialize the map
//     var map = L.map('map').setView([0, 0], 13);

//     // Add the OpenStreetMap tiles to the map
//     L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//         attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
//     }).addTo(map);

//     // Get the user's current location
//     navigator.geolocation.getCurrentPosition(function(position) {
//         var lat = position.coords.latitude;
//         var lng = position.coords.longitude;
//         var latLng = new L.LatLng(lat, lng);
//         map.setView(latLng, 13);

//         // Add a marker to the user's current location
//         var marker = L.marker(latLng).addTo(map);

//         // Track the user's movement on the map
//         navigator.geolocation.watchPosition(function(position) {
//             var lat = position.coords.latitude;
//             var lng = position.coords.longitude;
//             var latLng = new L.LatLng(lat, lng);
//             marker.setLatLng(latLng);
//             map.setView(latLng, 13);
//         });
//     });