"""Day5 예지보전 인포그래픽 2장 (auto-ax-infographic 스타일 10 · 02), 1920x1080 PNG."""
import csv, statistics as st, cairosvg
from xml.sax.saxutils import escape

W, H = 1920, 1080
FONT = "Noto Sans KR"
NAVY, INK, GREY, LINE = "#0E1F3E", "#1B2A4A", "#5F6B80", "#DDE3EC"
ORANGE, GOLD, RED, GREEN, BLUE = "#E8743B", "#D4961E", "#D23B3B", "#2E8B57", "#2F6FB0"
SENSOR = "../Day5_설비센서_50건_가상.csv"
CASES = "../Day5_예지보전_도입사례_실데이터.csv"

def t(x, y, s, size=22, fill=INK, w=500, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{w}" '
            f'fill="{fill}" text-anchor="{anchor}">{escape(str(s))}</text>')

def tag(x, y, s, color, wd=None):
    wd = wd or 26 + len(s) * 19
    return (f'<rect x="{x+3}" y="{y+4}" width="{wd}" height="40" rx="4" fill="#000" opacity=".12"/>'
            f'<rect x="{x}" y="{y}" width="{wd}" height="40" rx="4" fill="{color}"/>' + t(x + wd / 2, y + 28, s, 19, "#fff", 700, "middle"))

def chip(x, y, s, fill="#EEF2F8", ink=INK):
    wd = 22 + sum(19 if ord(c) > 0x3000 else 11 for c in s)
    return (f'<rect x="{x}" y="{y}" width="{wd}" height="34" rx="17" fill="{fill}"/>' + t(x + wd / 2, y + 24, s, 17, ink, 700, "middle")), wd

def panel(x, y, w, h):
    return (f'<rect x="{x+4}" y="{y+8}" width="{w}" height="{h}" rx="56" fill="#000" opacity=".06"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="56" fill="#fff" stroke="{LINE}" stroke-width="3"/>')

def frame(no, title, accent, body, page):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#F7F9FC"/>'
            f'<rect width="{W}" height="132" fill="{NAVY}"/><rect width="18" height="132" fill="{accent}"/>'
            + t(60, 88, f"{no} ·  {title}", 54, "#fff", 800)
            + t(1860, 112, "AUTOMOTIVE INDUSTRY × AI TRANSFORMATION · DAY 5 예지보전", 16, "#C9D3E3", 500, "end")
            + body
            + f'<rect x="60" y="1032" width="1800" height="3" fill="{LINE}"/>'
            + t(66, 1064, "자동차 산업 AX · Day5 예지보전 실습", 17, GREY) + t(1854, 1064, page, 17, GREY, 500, "end") + "</svg>")

# ---------------- 1) 도입사례 5건: 10 · 개선 사례·KPI형 ----------------
def slide_cases():
    rows = list(csv.DictReader(open(CASES, encoding="utf-8-sig")))
    assert len(rows) == 6 and rows[4]["기업"].startswith("포스코(포항제철소 냉연")   # 수치 미공개 1건은 제외
    show = [  # CSV 값을 줄여 쓴 표기 (수치는 원문 그대로)
        ("현대자동차", "생산라인 산업용 로봇 · 마키나락스 · 2026", ["모터 부하", "진동", "전류"], "로봇 고장 징후",
         ("고장 약 5일 전 감지", RED), "정확도 90% 이상 · 8년 현장 검증"),
        ("BMW 레겐스부르크", "차량 조립 컨베이어 · 2023", ["추가 센서 없음", "전력 소비", "이동 이상", "바코드 판독"], "컨베이어 결함",
         ("조립 중단 연 500분+ 회피", RED), "주요 조립라인 약 80% 감시"),
        ("익명 글로벌 OEM", "Siemens Senseye · 설비 1만 대+ · 2025", ["진동", "토크", "온도", "사이클타임"], "고장 · 성능 저하",
         ("비계획 정지 −12%", RED), "도입 12주 만 · SCADA·MES·CMMS 연동"),
        ("포스코 포항 선재공장", "냉각장치 · 유압실린더 · 2026", ["PIMS 설비 데이터", "센서 종류 미명시"], "설비 이상 · 수명",
         ("돌발정비 약 −50%", RED), "8월 기준 · 전년 동기 대비"),
        ("GM", "FANUC · Cisco ZDT · 로봇 수천 대 · 2017", ["로봇 운전 데이터", "센서 종류 미명시"], "로봇 잠재 고장",
         ("수치 미공개", GREY), "비계획 정지 '대폭 감소'로만 서술"),
    ]
    b = [panel(60, 170, 1230, 840), tag(100, 196, "도입사례 5건 · 실데이터", GOLD, 270)]
    cols = [(100, "기업 · 설비"), (470, "사용 센서 · 데이터"), (860, "예측 대상"), (1040, "보고된 효과")]
    b += [t(x, 282, s, 19, GREY, 700) for x, s in cols]
    b.append(f'<rect x="100" y="296" width="1150" height="2" fill="{INK}"/>')
    y0, rh = 306, 118
    for i, (co, eq, sensors, target, (eff, ec), sub) in enumerate(show):
        y = y0 + i * rh
        if i: b.append(f'<rect x="100" y="{y}" width="1150" height="1" fill="{LINE}"/>')
        b += [t(100, y + 46, co, 25, INK, 800), t(100, y + 80, eq, 16, GREY, 500)]
        cx, cy = 470, y + 18
        for s in sensors:
            muted = s in ("추가 센서 없음", "센서 종류 미명시")
            c, wd = chip(cx, cy, s, "#FDF1E3" if muted else "#EEF2F8", "#9A5B12" if muted else INK)
            if cx + wd > 845: cx, cy = 470, cy + 42; c, wd = chip(cx, cy, s, "#FDF1E3" if muted else "#EEF2F8", "#9A5B12" if muted else INK)
            b.append(c); cx += wd + 8
        b.append(t(860, y + 46, target, 20, INK, 700))
        b += [t(1040, y + 46, eff, 21, ec, 800), t(1040, y + 80, sub, 16, GREY, 500)]
    b.append(f'<rect x="100" y="{y0+5*rh+14}" width="1150" height="52" rx="6" fill="#FFF4E5"/>')
    b.append(t(675, y0 + 5 * rh + 48, "효과는 보고된 수치 그대로 · 측정 방식이 달라 사례끼리 직접 비교하지 않는다", 19, INK, 700, "middle"))

    b += [panel(1320, 170, 540, 840), tag(1360, 196, "자동차 AX 적용", GOLD, 190)]
    b.append(t(1360, 300, "센서보다 먼저 볼 것", 38, INK, 800))
    pts = [("1", "새 센서가 꼭 필요하진 않다", "BMW · GM은 기존 제어·운전 데이터로 예측"),
           ("2", "신호를 묶어서 본다", "현대차 3종, 익명 OEM 4종을 함께 분석"),
           ("3", "효과 지표가 제각각이다", "사전 감지일 · 회피 분 · 정지·정비 감소율")]
    for i, (n, h, d) in enumerate(pts):
        y = 360 + i * 120
        b.append(f'<circle cx="1378" cy="{y+12}" r="20" fill="{GOLD}"/>' + t(1378, y + 20, n, 22, "#fff", 800, "middle"))
        b += [t(1412, y + 22, h, 24, INK, 800), t(1412, y + 58, d, 18, GREY, 500)]
    b.append(f'<rect x="1350" y="745" width="480" height="210" rx="18" fill="#EAF0F8"/>')
    b += [t(1380, 792, "실습 미션", 22, GOLD, 800),
          t(1380, 836, "우리 라인 설비 1대를 골라", 21, INK, 500),
          t(1380, 870, "쓸 수 있는 신호와 효과 지표를", 21, INK, 500),
          t(1380, 904, "표의 한 줄처럼 적어 보기", 21, INK, 500),
          t(1380, 940, "출처: Day5_예지보전_도입사례_실데이터.csv (6건 중 5건)", 14, GREY, 500)]
    return frame("10", "예지보전 도입사례 5건 · 개선 사례·KPI형", GOLD, "".join(b), "1 / 2")

# ---------------- 2) 설비센서 50건: 02 · 데이터 스토리형 ----------------
def slide_sensor():
    rows = list(csv.DictReader(open(SENSOR, encoding="utf-8-sig")))
    assert len(rows) == 50 and all(r["비고"] == "실습용 가상 데이터" for r in rows)
    eqs = sorted({r["설비"] for r in rows})
    ser = {e: [r for r in rows if r["설비"] == e] for e in eqs}
    keys = [("진동(mm/s)", "진동 (mm/s)", 0.5, 4.0, [1, 2, 3]), ("온도(℃)", "온도 (℃)", 48, 68, [50, 55, 60, 65])]
    stats, first3 = {}, {}
    for e in eqs:
        for k, *_ in keys:
            v = [float(r[k]) for r in ser[e]]; base = v[:12]
            m, s = st.mean(base), st.stdev(base); stats[e, k] = (m, s)
            out = [abs(x - m) > 3 * s for x in v]
            first3[e, k] = next((ser[e][i]["시간"][11:] for i in range(2, 25) if all(out[i-2:i+1])), None)
    for e in eqs:   # 압력은 두 설비 모두 3σ 이내 → 차트 생략 근거
        v = [float(r["압력(bar)"]) for r in ser[e]]; m, s = st.mean(v[:12]), st.stdev(v[:12])
        assert all(abs(x - m) <= 3 * s for x in v)
    assert first3[eqs[1], "온도(℃)"] == "13:40" and first3[eqs[1], "진동(mm/s)"] == "15:40" and first3[eqs[0], "진동(mm/s)"] is None

    b = [panel(60, 170, 1230, 840), tag(100, 196, "실습용 가상 데이터", RED, 210),
         t(330, 224, "설비센서 50건 · 2026-09-15 08:00~16:00 · 20분 간격 · 설비 2대 × 25회", 18, GREY, 600)]
    CW, CH = 500, 215
    ann = {(0, 0): ("12:40 한 번만 3.5 → 다음 값 1.0", RED), (0, 1): ("기준 범위 안에서 안정", GREEN),
           (1, 0): ("15:00부터 계속 상승 → 2.9", RED), (1, 1): ("13:00부터 계속 상승 → 65.1", RED)}
    names = ["설비A · 프레스 메인모터", "설비B · 차체 용접로봇 감속기"]
    for ri, e in enumerate(eqs):
        b.append(t(110, 290 + ri * 335, names[ri], 23, INK, 800))
        for ci, (k, lab, lo, hi, ticks) in enumerate(keys):
            x0, y0 = 170 + ci * 570, 340 + ri * 335
            X = lambda i: x0 + i * CW / 24
            Y = lambda v: y0 + CH - (v - lo) / (hi - lo) * CH
            m, s = stats[e, k]
            b.append(f'<rect x="{x0}" y="{Y(m+3*s):.1f}" width="{CW}" height="{Y(m-3*s)-Y(m+3*s):.1f}" fill="{GREEN}" opacity=".16"/>')
            for tv in ticks:
                b.append(f'<line x1="{x0}" y1="{Y(tv):.1f}" x2="{x0+CW}" y2="{Y(tv):.1f}" stroke="{LINE}" stroke-width="1"/>' + t(x0 - 10, Y(tv) + 6, tv, 15, GREY, 500, "end"))
            b.append(f'<line x1="{x0}" y1="{y0+CH}" x2="{x0+CW}" y2="{y0+CH}" stroke="{INK}" stroke-width="2"/>')
            for i, hh in [(0, "08시"), (6, "10시"), (12, "12시"), (18, "14시"), (24, "16시")]:
                b.append(t(X(i), y0 + CH + 26, hh, 15, GREY, 500, "middle"))
            v = [float(r[k]) for r in ser[e]]
            b.append('<polyline fill="none" stroke="#7A879C" stroke-width="3" points="' + " ".join(f"{X(i):.1f},{Y(x):.1f}" for i, x in enumerate(v)) + '"/>')
            for i, x in enumerate(v):
                bad = abs(x - m) > 3 * s
                b.append(f'<circle cx="{X(i):.1f}" cy="{Y(x):.1f}" r="{7 if bad else 4}" fill="{RED if bad else INK}"/>')
            b.append(t(x0, y0 - 12, lab, 18, GREY, 700))
            a, ac = ann[ri, ci]
            b.append(t(x0 + CW, y0 - 12, a, 17, ac, 800, "end"))
    b.append(f'<rect x="100" y="936" width="1150" height="50" rx="6" fill="#EEF5EF"/>')
    b.append(t(675, 969, "초록 띠 = 08:00~11:40 평균 ± 3σ · 빨간 점 = 띠 밖 · 압력은 두 설비 모두 띠 안이라 생략", 18, INK, 700, "middle"))

    b += [panel(1320, 170, 540, 840), tag(1360, 196, "판단과 대응", ORANGE, 160)]
    b.append(t(1360, 296, "튄 값 vs 추세", 40, INK, 800))
    b += [t(1360, 352, "설비A: 한 번 튄 값", 23, INK, 800), t(1360, 386, "노이즈 가능성 → 재측정·센서 점검", 19, GREY, 500),
          t(1360, 436, "설비B: 계속 오르는 추세", 23, RED, 800), t(1360, 470, "온도가 진동보다 약 2시간 먼저 보임", 19, GREY, 500)]
    steps = ["이상치 탐지", "오류·운영 맥락 확인", "담당자 검토·승인", "정비 조치·기록"]
    for i, s in enumerate(steps):
        y = 515 + i * 58
        last = i == 2
        b.append(f'<rect x="1360" y="{y}" width="460" height="44" rx="8" fill="{"#FDEDE4" if last else "#F1F4F9"}" stroke="{ORANGE if last else LINE}" stroke-width="2"/>'
                 + t(1590, y + 30, s, 19, INK, 700, "middle"))
        if i < 3: b.append(t(1590, y + 56, "↓", 14, GREY, 700, "middle"))
    b.append(t(1590, 762, "탐지 결과로 설비를 자동 정지하지 않는다", 16, ORANGE, 800, "middle"))
    b.append(f'<rect x="1350" y="785" width="480" height="190" rx="18" fill="#EAF0F8"/>')
    b += [t(1380, 830, "실습 미션", 22, ORANGE, 800),
          t(1380, 872, "'띠 밖 3회 연속'을 알람 기준으로", 20, INK, 500),
          t(1380, 904, "하면 설비B는 몇 시에 울릴까?", 20, INK, 500),
          t(1380, 948, f"정답 · 온도 {first3[eqs[1], '온도(℃)']} · 진동 {first3[eqs[1], '진동(mm/s)']} · 설비A 없음", 16, GREY, 700)]
    return frame("02", "설비센서 50건 · 데이터 스토리형", ORANGE, "".join(b), "2 / 2")

if __name__ == "__main__":
    for name, svg in [("01_예지보전_도입사례5건.png", slide_cases()), ("02_설비센서50건_튐vs추세.png", slide_sensor())]:
        cairosvg.svg2png(bytestring=svg.encode(), write_to=name); print(name)
