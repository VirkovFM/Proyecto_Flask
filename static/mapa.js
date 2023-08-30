


var map = L.map('map').fitWorld();

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: zoom,
    attribution: '© OpenStreetMap'
}).addTo(map);
