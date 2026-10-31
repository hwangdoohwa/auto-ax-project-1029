"""머신러닝 이상치 탐지 6기법 · 정비 필요 시점 SVG 인포그래픽 (1920x1080, SVG + PNG).
Day5 인포그래픽(infographic_day5/make_infographic.py)과 같은 틀을 쓴다."""
import csv, cairosvg
from xml.sax.saxutils import escape

W, H = 1920, 1080
FONT = "Noto Sans KR"
NAVY, INK, GREY, LINE = "#0E1F3E", "#1B2A4A", "#5F6B80", "#DDE3EC"
STATUS = {"정상": "#C7CDD6", "관찰": "#E0A800", "점검 권고(단발 튐)": "#F05A28",
          "이상(지속)": "#D7263D", "정비 필요 시점": "#7A0019"}
res = list(csv.DictReader(open("결과_시점별_판정.csv", encoding="utf-8-sig")))
summ = list(csv.DictReader(open("결과_기법별_요약.csv", encoding="utf-8-sig")))


def t(x, y, s, size=22, fill=INK, w=500, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{w}" '
            f'fill="{fill}" text-anchor="{anchor}">{escape(str(s))}</text>')


def tag(x, y, s, color, wd=None):
    wd = wd or 26 + len(s) * 19
    return (f'<rect x="{x}" y="{y}" width="{wd}" height="40" rx="4" fill="{color}"/>' + t(x + wd / 2, y + 28, s, 19, "#fff", 700, "middle"))


def panel(x, y, w, h, r=28):
    return (f'<rect x="{x+4}" y="{y+8}" width="{w}" height="{h}" rx="{r}" fill="#000" opacity=".06"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#fff" stroke="{LINE}" stroke-width="3"/>')


def strip(eq, x, y, cw=42, ch=56):
    """25개 시점을 판정 색 칸으로 그린 타임라인."""
    rows = [r for r in res if r["설비명"] == eq]
    out = ""
    for i, r in enumerate(rows):
        cx = x + i * cw
        out += f'<rect x="{cx}" y="{y}" width="{cw-4}" height="{ch}" rx="6" fill="{STATUS[r["판정"]]}"/>'
        out += t(cx + (cw - 4) / 2, y + ch / 2 + 9, r["득표(6)"], 22, "#fff" if r["판정"] != "정상" else "#6B7280", 800, "middle")
        if i % 3 == 0:
            out += t(cx + (cw - 4) / 2, y + ch + 28, r["시각"], 16, GREY, 500, "middle")
    # 기준 구간 표시
    out += f'<rect x="{x}" y="{y-16}" width="{12*cw-4}" height="6" rx="3" fill="#9DB4D6"/>'
    out += t(x, y - 24, "기준(학습) 08:00~11:40", 16, "#5B7BA8", 700)
    return out, rows


def build():
    b = ""
    # 상단 문구
    b += t(60, 196, "6가지 기법이 각자 표를 던지고, 4표 이상이 2번 연속이면 ‘정비 필요 시점’", 34, INK, 800)
    b += tag(1588, 162, "실습용 가상 데이터", "#5F6B80", 272)

    # 왼쪽: 기법 카드 6개
    b += panel(60, 236, 640, 770)
    b += t(96, 290, "탐지 기법 6가지", 28, INK, 800)
    b += t(664, 290, "첫 탐지  A / B", 18, GREY, 700, "end")
    for i, s in enumerate(summ):
        y = 318 + i * 106
        b += f'<rect x="92" y="{y}" width="576" height="92" rx="14" fill="#F4F6FA"/>'
        b += f'<circle cx="132" cy="{y+46}" r="24" fill="{NAVY}"/>' + t(132, y + 54, i + 1, 22, "#fff", 800, "middle")
        b += t(172, y + 42, s["기법"], 25, INK, 800)
        b += t(172, y + 72, s["계열"], 18, GREY, 500)
        a, bb = s["설비A 첫 탐지"], s["설비B 첫 탐지"]
        b += t(652, y + 44, f"{a} / {bb}", 22, INK, 700, "end")
        b += t(652, y + 72, f"탐지 {s['설비A 탐지 건수']}건 / {s['설비B 탐지 건수']}건", 16, GREY, 500, "end")
    b += t(96, 978, "One-Class SVM은 표본 12건으로 학습해 과민 → 혼자서는 판정 못 함", 17, "#B45309", 700)

    # 오른쪽 위: 설비B 타임라인
    b += panel(740, 236, 1120, 330)
    b += t(776, 290, "설비B 차체 용접로봇 감속기", 28, INK, 800)
    b += tag(1610, 258, "정비 필요 13:20", STATUS["정비 필요 시점"], 214)
    sb, rowsB = strip("설비B", 776, 352)
    b += sb
    iB = next(i for i, r in enumerate(rowsB) if r["정비필요시점"] == "◆")
    iW = next(i for i, r in enumerate(rowsB) if r["판정"] == "관찰")
    iH = next(i for i, r in enumerate(rowsB) if int(r["득표(6)"]) >= 4)
    def callout(i, text, color, dy):
        cx = 776 + i * 42 + 19
        return (f'<line x1="{cx}" y1="410" x2="{cx}" y2="{410+dy}" stroke="{color}" stroke-width="3"/>'
                f'<circle cx="{cx}" cy="{410+dy}" r="6" fill="{color}"/>' + t(cx - 14, 410 + dy + 7, text, 19, color, 800, "end"))
    b += callout(iW, f"{rowsB[iW]['시각']} 첫 관찰(3표)", "#B7791F", 62)
    b += callout(iH, f"{rowsB[iH]['시각']} 4표", STATUS["이상(지속)"], 98)
    b += callout(iB, f"{rowsB[iB]['시각']} 2회 연속 → 정비 필요 시점 · 원인 온도", STATUS["정비 필요 시점"], 134)

    # 오른쪽 중간: 설비A 타임라인
    b += panel(740, 594, 1120, 210)
    b += t(776, 646, "설비A 프레스 메인모터", 28, INK, 800)
    b += tag(1580, 616, "점검 권고(단발 튐)", STATUS["점검 권고(단발 튐)"], 244)
    sa, rowsA = strip("설비A", 776, 704, ch=46)
    b += sa
    iS = next(i for i, r in enumerate(rowsA) if r["판정"] == "점검 권고(단발 튐)")
    b += t(776 + iS * 42 + 36, 694, f"↙ {rowsA[iS]['시각']} 진동 {rowsA[iS]['진동(mm/s)']} · 1회만 5표 → 바로 정상 복귀", 18, STATUS["점검 권고(단발 튐)"], 800)

    # 오른쪽 아래: 판정 규칙 + 사람 승인 흐름
    b += panel(740, 832, 1120, 174)
    rules = [("0~1표", "정상", STATUS["정상"]), ("2~3표", "관찰", STATUS["관찰"]),
             ("4표 1회", "점검 권고", STATUS["점검 권고(단발 튐)"]), ("4표 2연속", "정비 필요 시점", STATUS["정비 필요 시점"])]
    for i, (k, v, c) in enumerate(rules):
        x = 776 + i * 186
        b += f'<rect x="{x}" y="862" width="172" height="58" rx="10" fill="{c}"/>'
        b += t(x + 86, 886, k, 17, "#fff" if c != STATUS["정상"] else INK, 700, "middle")
        b += t(x + 86, 910, v, 19, "#fff" if c != STATUS["정상"] else INK, 800, "middle")
    flow = ["탐지", "담당자 검토", "승인", "비가동 시간 정비"]
    x0 = 1530
    for i, f in enumerate(flow):
        y = 852 + i * 38
        b += f'<rect x="{x0}" y="{y}" width="300" height="32" rx="8" fill="{"#E8EEF7" if i != 2 else "#1E7F4F"}"/>'
        b += t(x0 + 150, y + 23, f"{i+1}. {f}", 17, INK if i != 2 else "#fff", 700, "middle")
    b += t(776, 958, "칸 안 숫자 = 6기법 중 이상이라고 본 표 수", 17, GREY, 500)
    b += t(776, 986, "탐지 ≠ 고장 확정 · 설비 자동 정지 금지 · 사람이 승인한 뒤 정비 일정 확정", 18, "#B91C1C", 800)

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#F7F9FC"/>'
           f'<rect width="{W}" height="132" fill="{NAVY}"/><rect width="18" height="132" fill="#7A0019"/>'
           + t(60, 88, "03 ·  머신러닝으로 찾은 정비 필요 시점", 54, "#fff", 800)
           + t(1860, 112, "AUTOMOTIVE INDUSTRY × AI TRANSFORMATION · DAY 5 예지보전", 16, "#C9D3E3", 500, "end")
           + b + f'<rect x="60" y="1032" width="1800" height="3" fill="{LINE}"/>'
           + t(66, 1064, "자동차 산업 AX · Day5 설비센서 50건(실습용 가상 데이터) · 기준 구간 = 설비별 오전 12건", 17, GREY)
           + t(1854, 1064, "03", 17, GREY, 500, "end") + "</svg>")
    open("05_인포그래픽_정비필요시점.svg", "w", encoding="utf-8").write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to="05_인포그래픽_정비필요시점.png")
    print("ok")


if __name__ == "__main__":
    build()
