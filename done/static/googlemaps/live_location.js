// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.
let map, infoWindow;
let workerMarkers = [];

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 10,
        center: { lat: 52.27965560005034, lng: 21.134200062347926 },
    });
    infoWindow = new google.maps.InfoWindow();

    const locationButton = document.createElement("button");

    locationButton.textContent = "Pan to Current Location";
    locationButton.classList.add("custom-map-control-button");
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);
    locationButton.addEventListener("click", () => {
        // Try HTML5 geolocation.
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };

                    map.setCenter(pos);

                    // Get worker locations from your Django backend
                    fetchWorkerLocations(pos);
                },
                () => {
                    handleLocationError(true, infoWindow, map.getCenter());
                }
            );
        } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, infoWindow, map.getCenter());
        }
    });
};

function sendLocationsToBackend(workerLocation, clientLocation) {
  // Convert workerLocation and clientLocation to JSON objects
  const workerData = {
    lat: workerLocation.lat(),
    lng: workerLocation.lng(),
  };

  const clientData = {
    lat: clientLocation.lat(),
    lng: clientLocation.lng(),
  };


  // Center the map on the client's location from the beginning
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const initialPos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };
        map.setCenter(initialPos);

        // Get worker locations from your Django backend
        fetchWorkerLocations(initialPos);
      },
      () => {
        // handleLocationError(true, infoWindow, map.getCenter());
      }
    );
  } else {
    // Browser doesn't support Geolocation
    // handleLocationError(false, infoWindow, map.getCenter());
  }
}
function fetchWorkerLocations(customerLocation) {
    // Perform an AJAX request to your Django backend to fetch worker locations
    fetch("/live_location/?latitude=en&lat=" + customerLocation.lat + "&lng=" + customerLocation.lng)
        .then((response) => response.json())
        .then((data) => {


            // Create marker for customer location
            let customerMarker = new google.maps.Marker({
            position: customerLocation,
            map: map,
            title: "Customer Location",
            });

            // Set new zoom level
            map.setZoom(15);

            // Set center of the map to customer location
            map.setCenter(customerLocation);

            // Create marker for each worker location
            console.log(data);
            data.forEach((worker) => {
                let workerLocation = {lat: parseFloat(worker.latitude), lng: parseFloat(worker.longitude)};
                let workerMarkers = new google.maps.Marker({
                position: workerLocation,
                map: map,

                });
                console.log(worker);
                // Add worker marker to the array of worker markers
                // workerMarkers.push(workerMarkers);
            });
        })
        .catch((error) => {
            console.error("Error fetching worker locations:", error);

        });
}

// function clearWorkerMarkers() {
//   workerMarkers.forEach((marker) => {
//     marker.setMap(null);
//   });
//    workerMarkers = [];
// }



// Rest of the code...

window.initMap = initMap;



