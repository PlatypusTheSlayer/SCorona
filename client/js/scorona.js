/* SCorona data handler */
/* Date: 18/09/20       */
/* V0.1                 */

let picker = document.getElementById('dateInput');
mapboxgl.accessToken = 'pk.eyJ1IjoicGF0YXRhOTAiLCJhIjoiY2tmOGtmcG1wMGQyZTJ2bzg4OG5mbWhtOSJ9.mlIFBXXVioUYkzAwC6KaXA';

var map = new mapboxgl.Map({
    container: 'map', 
    style: 'mapbox://styles/patata90/ckf8to3pi1q0x19npfqm7n3a4',
    center: [-2.199490, 53.548000],
    zoom: 5 
});

map.addControl(new mapboxgl.NavigationControl());

picker.flatpickr({
    dateFormat: "d F Y",
    maxDate: "today",
    defaultDate: "today",
});

function dateSelected() {
    alert(picker.value);
}