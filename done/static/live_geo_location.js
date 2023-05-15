function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    console.log("Geolocation is not supported by this browser.");
  }
}

function showPosition(position) {
  let latitude = position.coords.latitude;
  let longitude = position.coords.longitude;
  // Send the latitude and longitude to your Django server to update the worker or customer model.
  updateLocation(latitude, longitude);
}

function updateLocation(latitude, longitude) {
  // Send an AJAX request to your Django server to update the worker or customer model with the new location.
  // You can use the Fetch API or jQuery.ajax() to send the request.
  fetch('/update-location/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      latitude: latitude,
      longitude: longitude
    })
  }).then(response => {
    console.log('Location updated successfully.');
  }).catch(error => {
    console.error('Error updating location:', error);
  });
}
