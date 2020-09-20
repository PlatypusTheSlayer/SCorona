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

let negative_count;
let positive_count;
let news_count;
let tweet_count;

let county_geojson;
$(document).ready(function(){
    $.get("http://127.0.0.1:5000/map-data", function(data, status){
      county_geojson = data;
    });
});

map.on('load', function() {

    for (var i = 0; i < county_geojson.length; i++) {

        // Color under label
        var layers = map.getStyle().layers;
        var firstSymbolId;
        for (var i = 0; i < layers.length; i++) {
            if (layers[i].type === 'symbol') {
                firstSymbolId = layers[i].id;
                break;
            }
        }

        id = i.toString()
        map.addSource(county_geojson[i].county.name, county_geojson[i].county.geojson);

        map.addLayer({
            'id': id,
            'type': 'fill',
            'source': county_geojson[i].county.name,
            'layout': {},
            'paint': {
                'fill-color': '#D15D48',
                'fill-opacity': county_geojson[i].opacity
            }
        }, firstSymbolId); // Color under label

        news_count = county_geojson[i].newscount;
        tweet_count = county_geojson[i].tweetcount;
        negative_count = county_geojson[i].emotions.negative;
        positive_count = county_geojson[i].emotions.positive;
        map.on('click', id, function (e) {
            new mapboxgl.Popup()
                .setLngLat(e.lngLat)
                .setHTML('<h6>News count: ' + news_count + '<br>Tweets count: ' + tweet_count
                         + '<br>Positive: ' + positive_count + '<br>Negative: ' + negative_count + '</h6>')
                .addTo(map);
        });


        map.on('mouseenter', id, function () {
            map.getCanvas().style.cursor = 'pointer';
        });


        map.on('mouseleave', id, function () {
            map.getCanvas().style.cursor = '';
        });

    }

    document.getElementById("news").innerHTML = news_count;
    document.getElementById("tweets").innerHTML = tweet_count;
    document.getElementById("neg").innerHTML = negative_count;
    document.getElementById("pos").innerHTML = positive_count;

})


map.addControl(new mapboxgl.NavigationControl());

picker.flatpickr({
    dateFormat: "d F Y",
    maxDate: "today",
    defaultDate: "today",
});

function dateSelected() {
    alert("Currently, only real-time data functionality is available.");
}