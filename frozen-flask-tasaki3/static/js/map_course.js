// js/map_course.js
window.initMap = function () {
    console.log("① initMap呼ばれた");

    const mapElement = document.getElementById("map");
    console.log("② map要素:", mapElement);

    console.log("③ google:", google);

    const spots = [
        { name: "大濠公園", lat: 33.5902, lng: 130.4017 },
        { name: "福岡城跡", lat: 33.5840, lng: 130.3830 },
        { name: "福岡タワー", lat: 33.5933, lng: 130.3519 }
    ];

    const map = new google.maps.Map(mapElement, {
        center: spots[0],
        zoom: 13,
    });

    const infoWindow = new google.maps.InfoWindow();

    spots.forEach((spot, index) => {
        const marker = new google.maps.Marker({
            position: spot,
            map: map,
            label: String(index + 1)
        });

        marker.addListener("click", () => {
            infoWindow.setContent(spot.name);
            infoWindow.open(map, marker);
        });
    });
};