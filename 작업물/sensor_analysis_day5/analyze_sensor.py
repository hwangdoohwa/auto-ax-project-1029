"""Day5 설비센서 50건(가상): 설비별 평균·표준편차·평상 범위(평균 ± 2σ)와 이상 후보 표시 + 시각화."""
import csv, statistics as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SRC = "../Day5_설비센서_50건_가상.csv"
VARS = [("진동(mm/s)", "진동", "mm/s"), ("온도(℃)", "온도", "℃"), ("압력(bar)", "압력", "bar")]
plt.rcParams.update({"font.family": "Malgun Gothic", "axes.unicode_minus": False})

rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
eqs = list(dict.fromkeys(r["설비"] for r in rows))          # 파일 순서 유지
stats = {}
for e in eqs:
    d = [r for r in rows if r["설비"] == e]
    for k, name, unit in VARS:
        v = [float(r[k]) for r in d]
        m, s = st.mean(v), st.stdev(v)                     # 표본 표준편차(n-1)
        stats[e, k] = (m, s, m - 2 * s, m + 2 * s)

# 1) 표: 시간 / 진동 / 온도 / 압력 + 이상 후보
out = []
for r in rows:
    flags = []
    for k, name, unit in VARS:
        m, s, lo, hi = stats[r["설비"], k]; x = float(r[k])
        if not lo <= x <= hi: flags.append(f"{name} {'↑' if x > hi else '↓'}")
    out.append({"설비": r["설비"], "시간": r["시간"][11:], "진동(mm/s)": r["진동(mm/s)"], "온도(℃)": r["온도(℃)"],
                "압력(bar)": r["압력(bar)"], "판정": "이상 후보 (" + ", ".join(flags) + ")" if flags else "정상"})
with open("센서표_이상후보.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
with open("통계_평상범위.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["설비", "변수", "평균", "표준편차", "평상 하한(평균-2σ)", "평상 상한(평균+2σ)", "이상 후보 수"])
    for e in eqs:
        for k, name, unit in VARS:
            m, s, lo, hi = stats[e, k]
            n = sum(1 for r in rows if r["설비"] == e and not lo <= float(r[k]) <= hi)
            w.writerow([e, k, f"{m:.2f}", f"{s:.2f}", f"{lo:.2f}", f"{hi:.2f}", n])

# 2) 시계열 + 평상 범위 띠 (3변수 × 2설비)
fig, axes = plt.subplots(3, 2, figsize=(15, 11), sharex=True)
for ci, e in enumerate(eqs):
    d = [r for r in rows if r["설비"] == e]; tx = [r["시간"][11:] for r in d]; xi = np.arange(len(d))
    for ri, (k, name, unit) in enumerate(VARS):
        ax = axes[ri, ci]; v = np.array([float(r[k]) for r in d]); m, s, lo, hi = stats[e, k]
        ax.axhspan(lo, hi, color="#2E8B57", alpha=.13, label="평상 범위 (평균 ± 2σ)")
        ax.axhline(m, color="#2E8B57", lw=1, ls="--", label=f"평균 {m:.2f}")
        ax.plot(xi, v, "-o", color="#1B2A4A", ms=4, lw=1.5)
        bad = (v < lo) | (v > hi)
        ax.scatter(xi[bad], v[bad], s=90, color="#D23B3B", zorder=3, label="이상 후보")
        for i in np.where(bad)[0]: ax.annotate(f"{tx[i]}\n{v[i]:g}", (i, v[i]), textcoords="offset points", xytext=(0, 9), ha="center", fontsize=8, color="#D23B3B")
        ax.set_ylabel(f"{name} ({unit})"); ax.grid(alpha=.3)
        ax.set_title(f"{e} · {name}  —  평상 {lo:.2f} ~ {hi:.2f}", fontsize=11, loc="left")
        if ri == 0 and ci == 0: ax.legend(loc="upper left", fontsize=8)
    for ax in axes[-1]: ax.set_xticks(xi[::3]); ax.set_xticklabels(tx[::3], rotation=0)
fig.suptitle("Day5 설비센서 50건 (실습용 가상 데이터) · 설비별 평상 범위와 이상 후보", fontsize=15, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, .96]); fig.savefig("01_시계열_평상범위.png", dpi=130); plt.close(fig)

# 3) z-점수 히트맵: 평균에서 몇 σ 떨어졌나 (|z|>2 = 이상 후보)
fig, axes = plt.subplots(2, 1, figsize=(15, 6.6), gridspec_kw={"hspace": .55})
for ax, e in zip(axes, eqs):
    d = [r for r in rows if r["설비"] == e]
    z = np.array([[(float(r[k]) - stats[e, k][0]) / stats[e, k][1] for r in d] for k, *_ in VARS])
    im = ax.imshow(z, cmap="RdBu_r", vmin=-4, vmax=4, aspect="auto")
    for (i, j), val in np.ndenumerate(z):
        ax.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=7.5,
                color="white" if abs(val) > 2.5 else "#1B2A4A", fontweight="bold" if abs(val) > 2 else "normal")
        if abs(val) > 2: ax.add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, fill=False, ec="#000", lw=1.6))
    ax.set_yticks(range(3)); ax.set_yticklabels([n for _, n, _ in VARS])
    ax.set_xticks(range(len(d))); ax.set_xticklabels([r["시간"][11:] for r in d], fontsize=7.5, rotation=90)
    ax.set_title(f"{e} · z-점수 (테두리 = |z| > 2, 이상 후보)", fontsize=11, loc="left")
fig.colorbar(im, ax=axes, shrink=.8, label="z = (값 - 평균) / σ")
fig.suptitle("평균에서 몇 표준편차 떨어졌나 (실습용 가상 데이터)", fontsize=14, fontweight="bold")
fig.savefig("02_z점수_히트맵.png", dpi=130, bbox_inches="tight"); plt.close(fig)

for e in eqs:
    for k, *_ in VARS: print(e, k, *(f"{x:.2f}" for x in stats[e, k]))
for o in out:
    if o["판정"] != "정상": print(o["설비"], o["시간"], o["진동(mm/s)"], o["온도(℃)"], o["압력(bar)"], o["판정"])
