from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17.5), (17.5, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/ep01_{i}.png" for i in (1, 2, 3)]
TEX = [r"\bar{T} \pm 2\sigma = 1500 \pm 2 \times 10 = [1480,\ 1520]",
       r"\mathrm{slope} = \frac{1515 - 1500}{3\,\mathrm{h}} = +5\ ^{\circ}\mathrm{C/h}",
       r"t_{\mathrm{alarm}} = \frac{1520 - 1515}{5} = 1\,\mathrm{h}"]

def cut1(t):   # 타이틀: 시리즈명만 "AX 현장"으로 바꾼 title_cut
    s = title_cut(t, "EP.01 · 용광로가 배우다")
    s[2] = punch("AX 현장", 540, 520, 150, fill="#fff", scale=back(prog(t, .1, .5)))
    return s

def cut2(t):   # 문제: 고로 상황판 + 명장 정년 D-30
    s = [bg("#E4ECF6")]
    s.append(punch("명장이 떠난다", 540, 170, 108, fill=BLUE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    c = back(prog(t, .4, .5))
    card = (f'<rect x="-380" y="-260" width="760" height="520" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>'
            f'<rect x="-380" y="-260" width="760" height="110" rx="24" fill="{ORANGE}"/><rect x="-380" y="-180" width="760" height="30" fill="{ORANGE}"/>'
            + label("고로 상황판", 0, -205, 50, "#fff", 900)
            + label("노 내부 온도", -330, -70, 42, NAVY, 700, "start") + label("1,500℃ ?", 330, -70, 46, RED, 900, "end")
            + label("직접 측정", -330, 40, 42, NAVY, 700, "start") + label("불가 (블랙박스)", 330, 40, 42, NAVY, 900, "end")
            + label("명장 정년퇴직", -330, 150, 42, NAVY, 700, "start") + label("D-30", 330, 150, 46, RED, 900, "end"))
    inner.append(f'<g transform="translate(540,660) scale({c})">{card}</g>')
    if t > 2.0: inner.append(punch("D-30?!", 840, 990, 90, fill=YELLOW, scale=back(prog(t, 2.0, .4)), rot=-8))
    inner.append(penguin(540, 1290, .7, "shock" if t > 2.3 else "worry", sweat=prog(t, 2.3, .4)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["명장님 퇴직하시면 용광로 컨디션은", "이제 누가 읽어요?!"], 540, 1700, 960, 230, tail=(-0.3, -1), scale=back(prog(t, 3.1, .45)), size=50))
    return s

def cut3(t):   # 반전
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.4))
    s.append(bubble(["열어 볼 수 없다면,", "둘러싼 신호를 전부 읽으면 돼."], 540, 330, 1000, 250, tail=(0, 1), scale=back(prog(t, .7, .45)), size=50))
    if t > 3.4: s.append(punch("감 → 데이터!", 540, 1650, 140, fill=YELLOW, scale=back(prog(t, 3.4, .45)), rot=-5))
    return s

def cut4(t):   # 해설: 추정 온도 추세 → 칩 → 수식 3줄 → 빨간 요약 → 말풍선
    s = [bg(CREAM)]
    s.append(punch("감을 숫자로", 540, 150, 100, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t,.3,.5))}">' + label("센서로 추정한 노 내부 온도 · 1시간 간격 (예시)", 540, 275, 38, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1150" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    X = lambda h: 200 + h * 170          # 0h → 200, 4h → 880
    Y = lambda T: 880 - (T - 1470) * 7.5  # 1470℃ → 880, 1530℃ → 430
    a = ease_out(prog(t, .5, .6))        # 평상범위 띠
    s.append(f'<g opacity="{a:.2f}"><rect x="{X(0)-30}" y="{Y(1520)}" width="{X(4)-X(0)+60}" height="{Y(1480)-Y(1520)}" fill="{GREEN}" opacity=".14"/>'
             f'<line x1="{X(0)-30}" y1="{Y(1520)}" x2="{X(4)+30}" y2="{Y(1520)}" stroke="{RED}" stroke-width="5" stroke-dasharray="16 12"/>'
             + label("상한 1,520", X(0) - 40, Y(1520) - 34, 32, RED, 800, "start")
             + label("평상범위", X(4) + 20, Y(1500), 32, GREEN, 800, "end")
             + label("하한 1,480", X(0) - 40, Y(1480) + 34, 32, GREEN, 800, "start") + "</g>")
    s.append(f'<line x1="{X(0)-30}" y1="{Y(1470)}" x2="{X(4)+30}" y2="{Y(1470)}" stroke="{NAVY}" stroke-width="5"/>')
    for h in range(5): s.append(label(f"{h}h", X(h), Y(1470) + 36, 30, GREY, 700))
    pts = [1500, 1505, 1510, 1515]
    for i, T in enumerate(pts):          # 점이 하나씩 찍힌다
        p = ease_out(prog(t, 1.2 + .5 * i, .4))
        if p <= 0: continue
        if i: s.append(f'<line x1="{X(i-1)}" y1="{Y(pts[i-1])}" x2="{X(i-1) + (X(i)-X(i-1))*p:.0f}" y2="{Y(pts[i-1]) + (Y(T)-Y(pts[i-1]))*p:.0f}" stroke="{NAVY}" stroke-width="8"/>')
        s.append(f'<circle cx="{X(i)}" cy="{Y(T)}" r="{16*p:.0f}" fill="{ORANGE}" stroke="{NAVY}" stroke-width="5"/>')
        s.append(f'<g opacity="{p:.2f}">' + label(f"{T:,}", X(i), Y(T) + 44, 30, NAVY, 800) + "</g>")
    p = ease_out(prog(t, 3.4, .6))       # 추세 연장 → 4h에 상한 도달
    if p > 0:
        s.append(f'<line x1="{X(3)}" y1="{Y(1515)}" x2="{X(3) + (X(4)-X(3))*p:.0f}" y2="{Y(1515) + (Y(1520)-Y(1515))*p:.0f}" stroke="{RED}" stroke-width="8" stroke-dasharray="14 10"/>')
        if p >= 1: s.append(f'<circle cx="{X(4)}" cy="{Y(1520)}" r="22" fill="#fff" stroke="{RED}" stroke-width="7"/>')
    s.append(chip("추세 +5℃/h → 1시간 뒤 상한", 540, 1000, RED, back(prog(t, 4.4, .45)), w=760, size=40))
    for i, y in enumerate((1060, 1160, 1260)):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 5.6 + .8 * i, .5)), scale=.5))
    s.append(f'<g opacity="{ease_out(prog(t, 8.4, .5))}">' + label("범위 안이어도, 추세가 1시간 먼저 말한다", 540, 1410, 44, RED, 900) + "</g>")
    s.append(owl(180, 1730, .45, point=True))
    s.append(bubble(["명장이 \"불꽃이 이상해\" 하던 순간,", "그게 바로 이 추세 신호야."], 650, 1690, 760, 220, tail=(-1.6, 1), scale=back(prog(t, 9.4, .45)), size=42))
    return s

def cut5(t):   # 후속 질문 + 실무 답 + 체크 칩
    s = [bg("#CFE6F2")]
    inner = chip("2019 WEF 등대공장 · 국내 최초", 540, 650, GOLD, back(prog(t, 2.4, .45)), w=760, size=36)
    inner += penguin(310, 1120, .85, "happy" if t > 3.6 else "worry", flap=prog(t, 3.6, 1.0))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: 센서 · 추세 · 예외 판단", 540, 1480, NAVY, back(prog(t, 4.4, .45)), w=880, size=36)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 AI가 명장님을", "대체하는 건가요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=50))
    if t > 1.6: s.append(bubble(["아니, 일상 조정은 AI가 맡고", "명장은 예외 판단으로 옮겨 갔어."], 540, 1720, 1000, 230, tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6: s.append(punch("역할 이동!", 330, 790, 100, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s

def cut6(t): return next_cut(t, BLUE, "노이즈 vs 추세", "튀는 값 하나에 알람을 울릴까?", topic_size=150)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "eq":
        for tex, p in zip(TEX, EQ): latex_png(tex, p)
    else:
        run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "output/ic_webtoon_ep01.mp4",
            [2.8, 9.9, 17.0, 30.5, 37.5, 41.0])
