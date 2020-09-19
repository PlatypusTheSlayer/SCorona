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

let london_geojson = {
	'type': 'geojson',
	'data': {
		'type': 'Feature',
		'geometry': {
			'type':'Polygon',
			'coordinates': [[
			[ 0.17379853095113162, 51.25988648550123],
		    [-0.7344108742125002, 51.462419773244875],
		    [-0.06406583706828428, 51.69087578714709],
			]]
		},
		"properties": {
			"name": "london"
		}
	}
}

let manchester_geojson = {
	'type': 'geojson',
	'data': {
		'type': 'Feature',
		'geometry': {
			'type':'Polygon',
			'coordinates': [[
			[-1.988072713912743, 53.23251119260354],
			[-1.3609757436810241, 53.477731559301304],
			[-1.123111375667662, 53.23251119260402]
			]]
		},
		"properties": {
			"name": "manchester"
		}
	}
}

let data =[{
    'county': {
      'name': 'london',
      'geojson': london_geojson
    },
    'color': "#088",
    'newscount': 2,
    'totalJoy': 1,
    'totalSadness': 2,
    'totalFear': 3,
    'totalAnger': 4,
    'totalGuilt': 5,
    'totalDisgust': 6,
    'totalShame': 7
  },
  {
    'county': {
      'name': 'manchester',
      'geojson': manchester_geojson
    },
    'color': "#088",
    'newscount': 2,
    'totalJoy': 1,
    'totalSadness': 2,
    'totalFear': 3,
    'totalAnger': 4,
    'totalGuilt': 5,
    'totalDisgust': 6,
    'totalShame': 7
  }
]

map.on('load', function() {
	for (var i = 0; i < data.length; i++) {
		map.addSource(data[i].county.name, data[i].county.geojson);

		map.addLayer({
	        'id': i.toString(),
	        'type': 'fill',
	        'source': data[i].county.name,
	        'layout': {},
	        'paint': {
	            'fill-color': data[i].color,
	            'fill-opacity': 0.8
	        }
	    });
	}
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