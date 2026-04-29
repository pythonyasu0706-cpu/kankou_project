// js/map_course.js
// window.initMap = function () {
//     console.log("① initMap呼ばれた");

//     const mapElement = document.getElementById("map");
//     console.log("② map要素:", mapElement);

//     console.log("③ google:", google);

//     const spots = [
//         { name: "大濠公園", lat: 33.5902, lng: 130.4017 },
//         { name: "福岡城跡", lat: 33.5840, lng: 130.3830 },
//         { name: "福岡タワー", lat: 33.5933, lng: 130.3519 }
//     ];

//     const map = new google.Map(mapElement, {
//         center: spots[0],
//         zoom: 13,
//     });

//     const infoWindow = new google.maps.InfoWindow();

//     spots.forEach((spot, index) => {
//         const marker = new google.maps.Marker({
//             position: spot,
//             map: map,
//             label: String(index + 1)
//         });

//         marker.addListener("click", () => {
//             infoWindow.setContent(spot.name);
//             infoWindow.open(map, marker);
//         });
//     });
// };




// js/map_course.js
let map;
let directionsService;
let directionsRenderer;
let isRouteVisible = true;

function initMap() {
    // 1. 初期化
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({
        suppressMarkers: false, // デフォルトのA, Bマーカーを表示するか
    });

    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: { lat: 33.5902, lng: 130.4017 },
    });

    directionsRenderer.setMap(map);

    // 2. ルートを計算して表示する実行関数
    calculateAndDisplayRoute();
}

function calculateAndDisplayRoute() {
    // 経由地の設定
    const waypoints = [
        { location: { lat: 33.5840, lng: 130.3830 }, stopover: true }, // 福岡城跡
    ];

    directionsService.route({
        origin: { lat: 33.5902, lng: 130.4017 },      // 出発：大濠公園
        destination: { lat: 33.5933, lng: 130.3519 }, // 到着：福岡タワー
        waypoints: waypoints,
        travelMode: google.maps.TravelMode.WALKING,    // 徒歩モード
    }, (response, status) => {
        if (status === "OK") {
            directionsRenderer.setDirections(response);
        } else {
            window.alert("ルートの取得に失敗しました: " + status);
        }
    });
}

// ボタンなどで呼び出す関数
function toggleRoute() {
    if (isRouteVisible) {
        directionsRenderer.setMap(null);
    } else {
        directionsRenderer.setMap(map);
    }
    isRouteVisible = !isRouteVisible;
}






// let map;
// let directionsRenderer;
// let isRouteVisible = true; // ルートが表示されているかの状態管理

// function initMap() {
//   // 1. マップの初期化
//     map = new google.maps.Map(document.getElementById("map"), {
//     zoom: 14,
//     center: { lat: 33.5902, lng: 130.4017 }, // 福岡近辺
//     });

//   // 2. ルート表示用レンダラーの準備
//     directionsRenderer = new google.maps.DirectionsRenderer();

//   // 最初にルートを表示設定にする（まだデータがないので画面には出ない）
//     directionsRenderer.setMap(map);

//   // （ここで本来はDirectionsServiceを使ってルートを取得する処理が入ります）
// }

// // 3. ルートの出し入れを制御する関数
// function toggleRoute() {
//     if (isRouteVisible) {
//     // 地図から切り離す（引っ込める）
//     directionsRenderer.setMap(null);
//     isRouteVisible = false;
//     } else {
//     // 地図に再接続する（出す）
//     directionsRenderer.setMap(map);
//     isRouteVisible = true;
//     }
// }