var near_checkbox = document.getElementById("near_me");
var x_input = document.getElementById("locationX");
var y_input = document.getElementById("locationY");

function set_near_me() {
    x_input.disabled = near_checkbox.checked;
    y_input.disabled = near_checkbox.checked;
    if (near_checkbox.checked) {
        navigator.geolocation.getCurrentPosition(function(position) {
            x_input.value = position.coords.longitude;
            y_input.value = position.coords.latitude;
        });
    }
}

near_checkbox.onchange = set_near_me;
