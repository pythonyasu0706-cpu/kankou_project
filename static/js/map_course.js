// js/map_course.js
let map; // GoogleMap本体を入れる変数
let directionsService; // ルート検索をする
let directionsRenderer; //計算したルートをちっずに描く
let isRouteVisible = true; //ルートが表示されているかどうかの状態管理

const ORIGIN = { lat: 33.5902, lng: 130.435112 } //福岡空港食事処
const DEST = { lat: 33.58444, lng: 130.45167 } //福岡空港展望台

const SPOTS = [
    { name: "福岡空港 食事処" },
    { name: "シーサイドももち" },
    { name: "福岡タワー" },
    { name: "天神カフェ" },
    { name: "福岡空港 展望台" }
];


// マーカー系 init-mapで呼ぶ
function createMarker(
    big,
    small,
    className,
    position,
    map,
    index = null,
    offsetX = 0,
    offsetY = 0
) {
    const el = document.createElement("div");
    el.className = `gm-marker ${className}`;

    if (index !== null) {
        el.setAttribute("data-index", index);
    }

    el.innerHTML = `
        <div class="gm-marker-ttl">${big}</div>
        <div class="gm-marker-sub">${small}</div>
    `;

    const wrapper = document.createElement("div");
    wrapper.className = "gm-marker-wrapper";

    wrapper.style.transform = `
        translate(-50%, -100%)
        translate(${offsetX}px, ${offsetY}px)
    `;

    wrapper.appendChild(el);

    const marker = new google.maps.marker.AdvancedMarkerElement({
        map: map,
        position: position,
        content: wrapper,
        zIndex: 1
    });

    wrapper.addEventListener("mouseenter", () => {
        marker.zIndex = 9999;
    });

    wrapper.addEventListener("mouseleave", () => {
        marker.zIndex = 1;
    });

    return marker;
}

function initMap() {
    // 1. 初期化
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({
        suppressMarkers: true, // createMarkerを呼ぶ
        preserveViewport: true,
        // 経路の線
        polylineOptions: {
            strokeColor: "#0ABAB5",
            strokeWeight: 6,          // 太さ
            strokeOpacity: 0.9        // 濃さ
        }
    });

    map = new google.maps.Map(document.getElementById("map"), {
        mapId: "7ad44ab02a1965f77cb6882b",
    });

    // ルート描画をこの地図に出す id=map
    directionsRenderer.setMap(map);

    // 2. ルートを計算して表示する実行関数
    calculateAndDisplayRoute();
}

// ルート計算用関数スタート
function calculateAndDisplayRoute() {
    // 経由地の設定 stopover:trueでちゃんと立ち寄る
    const waypoints = [
        { location: { lat: 33.595704, lng: 130.350751 }, stopover: true }, // 経由地1 シーサイドももち
        { location: { lat: 33.5932846, lng: 130.35151 }, stopover: true }, // 経由地2 福岡タワー
        { location: { lat: 33.59194, lng: 130.39472 }, stopover: true }, // 経由地3 天神大人の隠れ家カフェ
    ];

    // ルートの計算スタート
    directionsService.route({
        origin: ORIGIN,      // 出発：福岡空港
        destination: DEST, // 到着：福岡空港
        waypoints: waypoints, // 経由地をセット
        travelMode: google.maps.TravelMode.WALKING,    // 公共交通機関モード
    }, (response, status) => {

        if (status === "OK") {
            // ルートを地図に描画
            directionsRenderer.setDirections(response);

            const route = response.routes[0];
            const legs = route.legs;

            const points = [
                legs[0].start_location, // 1. 福岡空港食事処
                ...legs.map(leg => leg.end_location) // 経由地 + ゴール
            ]

            // これでマーカーが画面に収まる自動ズーム
            const bounds = new google.maps.LatLngBounds();
            points.forEach(point => {
                bounds.extend(point);
            });
            map.fitBounds(bounds, {
                top: 10,
                right: 70,
                bottom: 10,
                left: 10
            });

            // 
            const placedMarkers = [];

            points.forEach((point, index) => {

                let className = "is-waypoint";
                if (index === 0) className = "is-origin";
                if (index === points.length - 1) className = "is-dest";

                // ずらし量
                let offsetX = 0;
                let offsetY = 0;

                // すでに置いたマーカーと比較
                placedMarkers.forEach(prev => {
                    const dx = point.lat() - prev.lat;
                    const dy = point.lng() - prev.lng;

                    const distance = Math.sqrt(dx * dx + dy * dy);

                    // 近すぎたらずらす（しきい値は調整OK）
                    if (distance < 0.01) {
                        offsetX += 40;
                        offsetY += -60;
                    }
                });

                const marker = createMarker(
                    SPOTS[index]?.name || `スポット ${index + 1}`,
                    "",
                    `${className} ${className}-${index + 1}`,
                    point,
                    map,
                    index + 1,
                    offsetX,
                    offsetY
                );

                // DOMにtransform追加（ここがミソ）
                // marker.content.style.transform = `
                //     translate(-50%, -100%)
                //     translate(${offsetX}px, ${offsetY}px)
                // `;

                // 記録
                placedMarkers.push({
                    lat: point.lat(),
                    lng: point.lng()
                });
            });

        } else { // エラーの場合
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