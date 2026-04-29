import ezdxf
import TkEasyGUI as eg
from shapely.geometry import LineString
from shapely.ops import polygonize, unary_union, snap, linemerge
import subprocess
import traceback
import datetime
import os
import json
import sys
from openpyxl import Workbook
import math

# =========================
# bulge → 円弧を点列に変換
# =========================
def bulge_to_points(p1, p2, bulge, segment_len=100):

    if bulge == 0:
        return [p1, p2]

    theta = 4 * math.atan(bulge)

    chord = math.hypot(
        p2[0]-p1[0],
        p2[1]-p1[1]
    )

    radius = chord / (2 * math.sin(theta/2))

    # 円弧長に応じて分割数決定
    arc_length = abs(radius * theta)

    div = max(
        4,
        int(arc_length / segment_len)
    )

    # 中点
    mx = (p1[0]+p2[0]) / 2
    my = (p1[1]+p2[1]) / 2

    dx = p2[0]-p1[0]
    dy = p2[1]-p1[1]

    q = math.sqrt(
        radius**2 - (chord/2)**2
    )

    # 中心座標
    cx = mx - q*dy/chord * (-1 if bulge>0 else 1)
    cy = my + q*dx/chord * (-1 if bulge>0 else 1)

    start_angle = math.atan2(
        p1[1]-cy,
        p1[0]-cx
    )

    end_angle = math.atan2(
        p2[1]-cy,
        p2[0]-cx
    )

    if bulge > 0 and end_angle < start_angle:
        end_angle += 2*math.pi

    if bulge < 0 and end_angle > start_angle:
        end_angle -= 2*math.pi

    pts = []

    for i in range(div+1):

        t = start_angle + (
            end_angle-start_angle
        ) * i/div

        x = r(cx + radius*math.cos(t))
        y = r(cy + radius*math.sin(t))

        pts.append((x,y))

    return pts

# =========================
# exe対応
# =========================
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.getcwd()

SETTING_FILE = os.path.join(base_dir, "config.json")
LOG_FILE = os.path.join(base_dir, "error_log.txt")

def load_setting():
    if not os.path.exists(SETTING_FILE):
        return {}
    with open(SETTING_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_setting(settings):
    with open(SETTING_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

try:

    # =========================
    # 設定読み込み
    # =========================
    settings = load_setting()

    use_oda = settings.get("use_oda", True)

    try:
        DIGIT = int(settings.get("digit", 3))
    except:
        DIGIT = 3

    # =========================
    # ODAパス
    # =========================
    def find_oda_converter():

        base_dirs = [
            r"C:\Program Files\ODA",
            r"C:\Program Files (x86)\ODA",
        ]

        for base in base_dirs:

            if not os.path.exists(base):
                continue

            for name in os.listdir(base):

                path = os.path.join(
                    base,
                    name,
                    "ODAFileConverter.exe"
                )

                if os.path.exists(path):
                    return path

        return None

    ODA_PATH = find_oda_converter()

    if use_oda and ODA_PATH is None:

        eg.popup_error("ODA File Converterが見つかりません")
        exit()

    # =========================
    # DXF選択
    # =========================
    file = eg.popup_get_file(
        "DXF選択",
        file_types=[("DXF", "*.dxf")]
    )

    if not file:
        exit()

    base_dir = os.path.dirname(file)

    convert_dir = os.path.join(
        base_dir,
        "converted"
    )

    os.makedirs(convert_dir, exist_ok=True)

    # =========================
    # ODA変換
    # =========================
    if use_oda:

        eg.popup("DXF変換中...")

        subprocess.run([

            ODA_PATH,
            base_dir,
            convert_dir,
            "ACAD2000",
            "DXF",
            "0",
            "1"

        ], check=True)

        target_file = os.path.join(
            convert_dir,
            os.path.basename(file)
        )

    else:

        target_file = file

    # =========================
    # DXF読み込み
    # =========================
    doc = ezdxf.readfile(target_file)

    msp = doc.modelspace()

    # =========================
    # 丸め
    # =========================
    def r(v):
        return round(v * 1000) / 1000

    # =========================
    # レイヤ取得
    # =========================
    layers = sorted({

        e.dxf.layer

        for e in msp

        if hasattr(e.dxf, "layer")

    })


    # =========================
    # グループ分け
    # =========================
    layer_groups = {}

    for l in layers:

        if "-" in l:

            g = l.split("-")[0]

            layer_groups.setdefault(g, []).append(l)

        else:

            layer_groups.setdefault("未分類", []).append(l)


    # グループ順
    sorted_groups = sorted(layer_groups.items())


    # =========================
    # GUI作成
    # =========================
    layout = [

        [

            eg.Button("全選択"),
            eg.Button("全解除"),

            eg.Button("OK"),
            eg.Button("キャンセル")

        ]

    ]


    for g, lst in sorted_groups:

        layout.append([

            eg.Text(
                f"■ グループ{g}",
                font=("Meiryo", 10, "bold")
            )

        ])

        for l in sorted(lst):

            layout.append([

                eg.Checkbox(
                    l,
                    key=l,
                    default=True
                )

            ])


    window = eg.Window(

        "レイヤ選択",

        layout,

        size=(350, 500),

        resizable=True

    )


    # =========================
    # イベント
    # =========================
    while True:

        event, values = window.read()

        if event in (None, "キャンセル"):

            window.close()

            exit()

        if event == "全選択":

            for g, lst in sorted_groups:

                for l in lst:

                    window[l].update(True)


        if event == "全解除":

            for g, lst in sorted_groups:

                for l in lst:

                    window[l].update(False)

        # if event == "全選択":

        #     for k in values:

        #         window[k].update(True)


        # if event == "全解除":

        #     for k in values:

        #         window[k].update(False)


        if event == "OK":

            break


    window.close()


    # =========================
    # 選択レイヤ
    # =========================
    TARGET_LAYERS = [

        k

        for k,v in values.items()

        if v

    ]

    if not TARGET_LAYERS:

        eg.popup_error("レイヤが選択されていません")

        exit()


    # print("選択レイヤ")

    # for l in TARGET_LAYERS:

    #     print(l)

    # =========================
    # モード
    # =========================
    mode = int(

        eg.popup_get_text(

            "処理モード\n1:個別\n2:外周"

        )

    )

    # =========================
    # 線種
    # =========================
    linetypes=set()

    for l in msp.query("LINE"):

        if TARGET_LAYERS and l.dxf.layer not in TARGET_LAYERS:
            continue

        lt=l.dxf.linetype

        if lt.upper()=="BYLAYER":

            lt=doc.layers.get(l.dxf.layer).dxf.linetype

        linetypes.add(

            lt.upper()

        )

    linetypes=sorted(linetypes)

    lt_choice=eg.popup_get_text(

        "線種番号（0=全体）\n"+

        "\n".join(

            f"{i+1}:{lt}"

            for i,lt in enumerate(linetypes)

        )

    )

    if lt_choice is None:
        exit()

    lt_choice=int(lt_choice)

    TARGET_LINETYPE=None if lt_choice==0 else linetypes[lt_choice-1]

    # =========================
    # 小数桁
    # =========================
    digit_input = eg.popup_get_text("小数点以下桁数（未入力=3）")
    DIGIT = 3 if not digit_input else int(digit_input)

    # =========================
    # 曲線含む図形を格納するリスト
    # =========================
    curve_lines = []

    # =========================
    # LINE取得
    # =========================
    lines=[]

    for l in msp.query("LINE"):

        if TARGET_LAYERS and l.dxf.layer not in TARGET_LAYERS:
            continue

        lt=l.dxf.linetype

        if lt.upper()=="BYLAYER":
            lt=doc.layers.get(l.dxf.layer).dxf.linetype

        if TARGET_LINETYPE and lt.upper()!=TARGET_LINETYPE:
            continue

        p1=(r(l.dxf.start.x),r(l.dxf.start.y))
        p2=(r(l.dxf.end.x),r(l.dxf.end.y))

        lines.append(LineString([p1,p2]))

# =========================
# ARC → 長さベース分割
# =========================

    for a in msp.query("ARC"):

        if TARGET_LAYERS and a.dxf.layer not in TARGET_LAYERS:
            continue

        cx = a.dxf.center.x
        cy = a.dxf.center.y

        radius = a.dxf.radius

        start = math.radians(
            a.dxf.start_angle
        )

        end = math.radians(
            a.dxf.end_angle
        )

        theta = abs(end-start)

        arc_length = radius * theta

        segment_len = 100

        div = max(

            6,

            int(arc_length / segment_len)

        )

        pts=[]

        for i in range(div+1):

            t = start + (

                end-start

            ) * i/div

            x = r(
                cx + radius*math.cos(t)
            )

            y = r(
                cy + radius*math.sin(t)
            )

            pts.append((x,y))

        line = LineString(pts)

        lines.append(line)

        curve_lines.append(line)
    
    # =========================
    # CIRCLE → 長さベース分割
    # =========================

    for c in msp.query("CIRCLE"):

        if TARGET_LAYERS and c.dxf.layer not in TARGET_LAYERS:
            continue

        cx = c.dxf.center.x
        cy = c.dxf.center.y

        radius = c.dxf.radius

        circumference = 2 * math.pi * radius

        segment_len = 100

        div = max(

            12,

            int(

                circumference /

                segment_len

            )

        )

        pts=[]

        for i in range(div):

            t = 2*math.pi * i/div

            x = r(
                cx + radius*math.cos(t)
            )

            y = r(
                cy + radius*math.sin(t)
            )

            pts.append((x,y))

        pts.append(pts[0])

        line = LineString(pts)

        lines.append(line)

        curve_lines.append(line)

    # =========================
    # LWPOLYLINE（bulge対応）
    # =========================
    for pl in msp.query("LWPOLYLINE"):

        if TARGET_LAYERS and pl.dxf.layer not in TARGET_LAYERS:
            continue

        pts = []

        points = list(
            pl.get_points("xyb")
        )

        for i in range(len(points)-1):

            x1,y1,b1 = points[i]
            x2,y2,b2 = points[i+1]

            p1 = (r(x1), r(y1))
            p2 = (r(x2), r(y2))

            arc_pts = bulge_to_points(
                p1,
                p2,
                b1
            )

            pts.extend(arc_pts[:-1])

        # 閉じる場合
        if pl.closed:

            x1,y1,b1 = points[-1]
            x2,y2,b2 = points[0]

            p1 = (r(x1), r(y1))
            p2 = (r(x2), r(y2))

            arc_pts = bulge_to_points(
                p1,
                p2,
                b1
            )

            pts.extend(arc_pts)

        line = LineString(pts)

        lines.append(line)

        # 円弧含む可能性
        if any(p[2] != 0 for p in points):

            curve_lines.append(line)


    # =========================
    # POLYLINE（旧形式 bulge対応）
    # =========================
    for pl in msp.query("POLYLINE"):

        if TARGET_LAYERS and pl.dxf.layer not in TARGET_LAYERS:
            continue

        pts = []

        verts = list(pl.vertices)

        for i in range(len(verts)-1):

            v1 = verts[i]
            v2 = verts[i+1]

            p1 = (
                r(v1.dxf.location.x),
                r(v1.dxf.location.y)
            )

            p2 = (
                r(v2.dxf.location.x),
                r(v2.dxf.location.y)
            )

            bulge = getattr(
                v1.dxf,
                "bulge",
                0
            )

            arc_pts = bulge_to_points(
                p1,
                p2,
                bulge
            )

            pts.extend(arc_pts[:-1])

        if pl.is_closed:

            v1 = verts[-1]
            v2 = verts[0]

            p1 = (
                r(v1.dxf.location.x),
                r(v1.dxf.location.y)
            )

            p2 = (
                r(v2.dxf.location.x),
                r(v2.dxf.location.y)
            )

            bulge = getattr(
                v1.dxf,
                "bulge",
                0
            )

            arc_pts = bulge_to_points(
                p1,
                p2,
                bulge
            )

            pts.extend(arc_pts)

        line = LineString(pts)

        lines.append(line)
        
    # =========================
    # 近接チェック
    # =========================
    from math import hypot

    threshold=0.02
    close_points=[]

    points=[]

    for l in lines:

        c=list(l.coords)

        points.append(c[0])
        points.append(c[-1])

    for i in range(len(points)):

        for j in range(i+1,len(points)):

            d=hypot(
                points[i][0]-points[j][0],
                points[i][1]-points[j][1]
            )

            if 0<d<threshold:

                close_points.append((points[i],points[j],d))

    # =========================
    # 面生成
    # =========================
    merged=unary_union(lines)

    merged=linemerge(merged)

    merged=snap(merged,merged,0.01)

    polygons=list(polygonize(merged))

    # =========================
    # モード
    # =========================
    if mode==1:

        polys=polygons

    else:

        outer=unary_union(polygons)

        polys=[outer] if outer.geom_type=="Polygon" else list(outer.geoms)

    # =========================
    # 外周描画
    # =========================
    for poly in polys:

        msp.add_lwpolyline(
            list(poly.exterior.coords),
            close=True,
            dxfattribs={"color":1}
        )
    
    # =========================
    # DXF用 Unicode変換
    # =========================
    def to_dxf_unicode(s):
        return "".join(
            f"\\U+{ord(c):04X}" if ord(c) > 127 else c
            for c in s
        )

    # =========================
    # Excel用 丸数字
    # =========================
    def excel_circled_number(i):

        circled_1_20 = [
        "①","②","③","④","⑤","⑥","⑦","⑧","⑨","⑩",
        "⑪","⑫","⑬","⑭","⑮","⑯","⑰","⑱","⑲","⑳"
        ]

        circled_21_35 = [
        "㉑","㉒","㉓","㉔","㉕","㉖","㉗","㉘","㉙","㉚",
        "㉛","㉜","㉝","㉞","㉟"
        ]

        if i <= 20:
            return circled_1_20[i-1]

        elif i <= 35:
            return circled_21_35[i-21]

        else:
            return f"({i})"


    # =========================
    # CAD用 丸数字（円＋数字）
    # =========================
    def draw_circled_number(msp, x, y, i):
        circle_r = 250
        text_h   = 350



        # 円
        msp.add_circle(
            center=(x, y),
            radius=circle_r,
            dxfattribs={
                "linetype": "CONTINUOUS",
                "color": 256
            }
        )

        # 数字
        txt = str(i)

        w = len(txt) * text_h * 0.6

        msp.add_text(
            txt,
            dxfattribs={"height":text_h}
        ).set_placement(
            (x - w/2, y - text_h/2)
        )

    # =========================
    # 曲線を含む図形か判定
    # =========================
    def has_curve_shape(poly):

        coords = list(poly.exterior.coords)

        angles = []

        for i in range(len(coords)-2):

            x1,y1 = coords[i]
            x2,y2 = coords[i+1]
            x3,y3 = coords[i+2]

            dx1 = x2-x1
            dy1 = y2-y1

            dx2 = x3-x2
            dy2 = y3-y2

            a1 = math.atan2(dy1,dx1)
            a2 = math.atan2(dy2,dx2)

            diff = abs(a1-a2)

            angles.append(diff)

        small_changes = sum(1 for a in angles if a < 0.2)

        return small_changes > 3

    # =========================
    # 個別面積
    # =========================
    excel_rows = []

    for i, poly in enumerate(polys, start=1):

        has_curve = has_curve_shape(poly)

        area = poly.area / 1_000_000

        minx, miny, maxx, maxy = poly.bounds
        width_m = (maxx - minx) / 1000
        height_m = (maxy - miny) / 1000

        mark_excel = excel_circled_number(i)

        # 左上（番号＋面積）

        txt_area = f"{area:.{DIGIT}f}㎡"

        # 丸番号（左上）      
        text_h = 400
        circle_r = 250

        # 面積文字
        msp.add_text(
            txt_area,
            dxfattribs={"height": text_h}
        ).set_placement((minx + 600, maxy))

        # 丸番号（文字の左）
        draw_circled_number(
            msp,
            minx + circle_r,
            maxy + text_h/2,
            i
        )

        # 中央（番号のみ）
        c = poly.centroid

        draw_circled_number(
            msp,
            c.x,
            c.y,
            i
        )

        # Excel用データ
        if mode == 1:

            if has_curve:

                excel_rows.append([
                    mark_excel,
                    round(area, DIGIT),
                    "",
                    "",
                    ""
                ])

            else:

                excel_rows.append([
                    mark_excel,
                    round(area, DIGIT),
                    round(width_m, DIGIT),
                    round(height_m, DIGIT),
                    f"{round(width_m, DIGIT)} × {round(height_m, DIGIT)}"
                ])

        else:

            excel_rows.append([
                mark_excel,
                round(area, DIGIT),
            ])
    # =========================
    # 合計（右下外）
    # =========================
    clusters=unary_union(polygons)

    cluster_list=[clusters] if clusters.geom_type=="Polygon" else list(clusters.geoms)

    for cluster in cluster_list:

        inside=[p for p in polygons if p.intersects(cluster)]

        sum_area=sum(p.area for p in inside)

        diff=(sum_area-cluster.area)/1_000_000

        if abs(diff)<1e-6:
            diff=0

        total=sum_area/1_000_000

        minx,miny,maxx,maxy=cluster.bounds

        minx,miny,maxx,maxy = cluster.bounds

        # 下側中央
        x = (minx + maxx) / 2
        y = miny - 800

        h1=700
        h2=300

        t1=f"{total:.{DIGIT}f}㎡"
        t2=f"{diff:+.{DIGIT}f}㎡"

        w1=len(t1)*h1*0.6
        w2=len(t2)*h2*0.6

        # 合計面積(中央)
        msp.add_text(t1,dxfattribs={"height":h1}).set_placement(
            (x-w1/2, y)
        )
        # 誤差(中央の下)
        msp.add_text(t2,dxfattribs={"height":h2}).set_placement(
            (x-w2/2, y - 200)
        )

    # =========================
    # 保存
    # =========================
    save_path = eg.popup_get_file(
        "保存先",
        save_as=True,
        default_extension=".dxf"
    )

    if save_path:

        doc.saveas(save_path)

        # =========================
        # Excel出力
        # =========================
        excel_path = save_path.replace(".dxf", ".xlsx")

        wb = Workbook()
        ws = wb.active

        if mode == 1:
            ws.append(["番号","面積(㎡)","W(m)","H(m)","W×H"])
        else:
            ws.append(["番号","面積(㎡)"])

        for r in excel_rows:
            ws.append(r)

        wb.save(excel_path)

        eg.popup(
            f"保存しました\n\nDXF:\n{save_path}\n\nExcel:\n{excel_path}"
        )


except Exception:

    error_msg=traceback.format_exc()

    with open(LOG_FILE,"a",encoding="utf-8") as f:

        f.write("=================================\n")
        f.write(str(datetime.datetime.now())+"\n")
        f.write(error_msg+"\n")

    eg.popup_error(
        "エラーが発生しました\nログを確認してください"
    )

#完成したらターミナルにてexe化
#まずはpyinstallerをインストールしてください
# pip install pyinstaller
#ターミナルのカレントディレクトリをこのファイルのある場所に移動してから以下のコマンドを実行してください
#例）cd jw_to_python_vol8
# pyinstaller --onefile --noconsole test0324.py