from webtoon_lib import *

CUTS = [(0, 4), (4, 10.5), (10.5, 17.5), (17.5, 31), (31, 38), (38, 41.5)]
DUR = 41.5
EQ = [f"eq/ep02_{i}.png" for i in (1, 2, 3)]
TEX = [r"2300 \times 5\,\mathrm{min} \times 0.7 = 8050\,\mathrm{min}",
       r"\frac{8050}{60}\,\mathrm{h} \times 20000 \times 12 = 32200000",
       r"\mathrm{rate} = 0\% \ \Rightarrow\ 0"]

def cut1(t):   # 타이틀: 시리즈명 "AX 현장"
    s = title_cut(t, "특별편 · 1~4일차 복습 자료실", chip_w=860)
    s[2] = punch("AX 현장", 540, 520, 150, fill="#fff", scale=back(prog(t, .1, .5)))
    return s

def cut2(t):   # 문제: 쌓인 4일치 강의
    s = [bg("#E4ECF6")]
    s.append(punch("복습할 게 산더미", 540, 170, 100, fill=BLUE, scale=back(prog(t, 0, .5))))
    inner = ['<rect x="80" y="320" width="920" height="1180" fill="#2B3A5C"/><rect x="80" y="320" width="920" height="1180" fill="url(#dotsW)"/>']
    c = back(prog(t, .4, .5))
    rows = [("강의", "1~4일차"), ("기준 슬라이드", "31장"), ("강의 전사문", "9개 · 5,214구간"), ("실습 프롬프트", "수십 개")]
    card = (f'<rect x="-380" y="-280" width="760" height="560" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>'
            f'<rect x="-380" y="-280" width="760" height="110" rx="24" fill="{ORANGE}"/><rect x="-380" y="-200" width="760" height="30" fill="{ORANGE}"/>'
            + label("내 복습 목록", 0, -225, 50, "#fff", 900))
    for i, (k, v) in enumerate(rows):
        y = -100 + i * 100
        card += label(k, -330, y, 42, NAVY, 700, "start") + label(v, 330, y, 44, RED if i == 2 else NAVY, 900, "end")
    inner.append(f'<g transform="translate(540,670) scale({c})">{card}</g>')
    if t > 2.0: inner.append(punch("4일치?!", 840, 1000, 90, fill=YELLOW, scale=back(prog(t, 2.0, .4)), rot=-8))
    inner.append(penguin(540, 1290, .7, "shock" if t > 2.3 else "worry", sweat=prog(t, 2.3, .4)))
    s.append(panel_frame(80, 320, 920, 1180, "".join(inner), scale=back(prog(t, .05, .45))))
    s.append(bubble(["4일치 강의를", "언제 다 다시 보죠?!"], 540, 1700, 900, 230, tail=(-0.3, -1), scale=back(prog(t, 3.1, .45)), size=52))
    return s

def cut3(t):   # 반전: 저장소 하나에 정리
    s = [bg(NAVY, "dotsW")]
    s.append(owl(540, 1120 + (1 - ease_out(prog(t, 0, .5))) * 300, 1.25, blink=(1.6 < t < 1.75), point=t > 3.4))
    s.append(bubble(["저장소 하나에 다 모아 뒀어.", "31장을 95장으로 펼쳐서."], 540, 330, 1000, 250, tail=(0, 1), scale=back(prog(t, .7, .45)), size=50))
    if t > 3.4: s.append(punch("31 → 95장!", 540, 1650, 150, fill=YELLOW, scale=back(prog(t, 3.4, .45)), rot=-5))
    return s

def cut4(t):   # 해설: 복습실습실 절감액 탭 손계산
    s = [bg(CREAM)]
    s.append(punch("절감액 손계산", 540, 150, 100, fill=ORANGE, scale=back(prog(t, 0, .45))))
    s.append(f'<g opacity="{ease_out(prog(t,.3,.5))}">' + label("복습실습실 절감액 탭 · 기본 입력값 (가정)", 540, 275, 38, NAVY, 700) + "</g>")
    s.append(f'<rect x="50" y="330" width="980" height="1150" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="8"/>')
    s.append(f'<g opacity="{ease_out(prog(t,.5,.5))}">' + label("월 2,300건 · 건당 5분 · 자동화 70% · 시간당 20,000원", 540, 400, 36, GREY, 700) + "</g>")
    k = 760 / 11500                      # 11,500분 → 760px
    bars = [("월 처리 시간", 11500, NAVY, "11,500분", .9), ("자동화로 줄이는 시간 (70%)", 8050, GREEN, "8,050분", 1.8)]
    for i, (name, v, col, txt, a) in enumerate(bars):
        y = 500 + i * 170; p = ease_out(prog(t, a, .6))
        s.append(f'<g opacity="{min(1, p*3):.2f}">' + label(name, 160, y, 36, NAVY, 800, "start") + "</g>")
        s.append(f'<rect x="160" y="{y+34}" width="{v*k*p:.0f}" height="84" rx="12" fill="{col}"/>')
        if p > .6: s.append(label(txt, 160 + v * k / 2, y + 76, 40, "#fff", 900))
    s.append(chip("연 32,200,000원 (가정 환산)", 540, 870, RED, back(prog(t, 3.2, .45)), w=760, size=40))
    for i, y in enumerate((940, 1050, 1160)):
        s.append(eq_img(EQ[i], 540, y, ease_out(prog(t, 4.6 + .9 * i, .5)), scale=.5))
    s.append(f'<g opacity="{ease_out(prog(t, 7.8, .5))}">' + label("실제 절감 실적이 아니라, 가정이 만든 숫자", 540, 1330, 44, RED, 900) + "</g>")
    s.append(f'<g opacity="{ease_out(prog(t, 8.3, .5))}">' + label("비율을 0으로 바꾸면 0원이 된다", 540, 1400, 38, NAVY, 700) + "</g>")
    s.append(owl(180, 1730, .45, point=True))
    s.append(bubble(["입력값을 바꿔 보면서", "가정이 결과를 바꾸는 걸 봐."], 650, 1690, 740, 220, tail=(-1.6, 1), scale=back(prog(t, 9.2, .45)), size=46))
    return s

def cut5(t):   # 후속: 어디서 받나
    s = [bg("#CFE6F2")]
    inner = chip("github.com/hwangdoohwa", 540, 650, NAVY, back(prog(t, 2.4, .45)), w=760, size=38)
    inner += penguin(310, 1120, .85, "happy" if t > 3.6 else "worry", flap=prog(t, 3.6, 1.0))
    inner += owl(780, 1150, .74, blink=(1.2 < t < 1.35))
    inner += chip("체크: PDF · 프롬프트 70 · 실습실", 540, 1480, GOLD, back(prog(t, 4.4, .45)), w=880, size=36)
    s.append(panel_frame(60, 560, 960, 1000, inner, fill="#F7F3EA", scale=back(prog(t, 0, .4))))
    s.append(bubble(["그럼 자료는", "어디서 받아요?"], 400, 320, 620, 220, tail=(-0.3, 1), scale=back(prog(t, .4, .4)), size=52))
    if t > 1.6: s.append(bubble(["README에서 PDF·PPTX 받고,", "실습은 복습실습실.html로 해."], 540, 1720, 1000, 230, tail=(0.5, -1), scale=back(prog(t, 1.6, .4)), size=46))
    if t > 3.6: s.append(punch("바로 복습!", 330, 790, 100, fill="#fff", scale=back(prog(t, 3.6, .4)), rot=-10))
    return s

def cut6(t): return next_cut(t, GREEN, "5~6일차", "남은 이틀은 어떻게 정리할까?", topic_size=200)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "eq":
        for tex, p in zip(TEX, EQ): latex_png(tex, p)
    else:
        run([cut1, cut2, cut3, cut4, cut5, cut6], CUTS, DUR, "output/ic_webtoon_ep02.mp4",
            [2.8, 9.9, 17.0, 30.5, 37.5, 41.0])
