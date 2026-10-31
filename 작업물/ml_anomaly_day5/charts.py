"""analyze_ml.py 결과로 matplotlib 차트 4장을 만든다."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker
import numpy as np
import pandas as pd
from analyze_ml import METHODS, NBASE, VOTE_TH, F

plt.rcParams.update({"font.family": "Malgun Gothic", "axes.unicode_minus": False, "mathtext.fontset": "dejavusans", "font.size": 11,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#888",
                     "axes.labelcolor": "#333", "xtick.color": "#555", "ytick.color": "#555"})
INK, MUTED, GRID = "#1B2A4A", "#6B7280", "#E5E7EB"
STATUS = {"정상": "#9CA3AF", "관찰": "#E0A800", "점검 권고(단발 튐)": "#F05A28",
          "이상(지속)": "#D7263D", "정비 필요 시점": "#7A0019"}
LINE = "#2F5D8A"
PLAIN = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}".replace("-", "-"))
res = pd.read_csv("결과_시점별_판정.csv", encoding="utf-8-sig")
EQS = ["설비A", "설비B"]
EQNAME = {e: res[res["설비명"] == e]["설비"].iloc[0] for e in EQS}
NOTE = "실습용 가상 데이터 · 기준 구간 08:00~11:40 · 탐지 결과는 고장 확정이 아니며 담당자 검토·승인 후 조치"


def legend_handles():
    return [mpatches.Patch(color=c, label=k) for k, c in STATUS.items()]


# 01 시계열 + 판정 ---------------------------------------------------------------
fig, axes = plt.subplots(3, 2, figsize=(16, 10), sharex=True)
for c, eq in enumerate(EQS):
    g = res[res["설비명"] == eq].reset_index(drop=True)
    x = np.arange(len(g))
    for r, col in enumerate(F):
        ax = axes[r, c]
        b = g[col].iloc[:NBASE]
        mu, sd = b.mean(), b.std()
        ax.axvspan(-0.5, NBASE - 0.5, color="#F3F4F6", zorder=0)
        ax.fill_between(x, mu - 3 * sd, mu + 3 * sd, color="#DBEAFE", alpha=.7, lw=0, label="기준 평균 ± 3σ")
        ax.plot(x, g[col], color=LINE, lw=2, zorder=2)
        ax.scatter(x, g[col], s=[90 if s != "정상" else 30 for s in g["판정"]],
                   c=[STATUS[s] for s in g["판정"]], edgecolor="white", lw=1.5, zorder=3)
        m = g.index[g["정비필요시점"] == "◆"]
        for i in m:
            ax.axvline(i, color=STATUS["정비 필요 시점"], lw=2, ls="--", zorder=1)
            if r == 0:
                ax.annotate(f"정비 필요 시점 {g.loc[i, '시각']}", (i, ax.get_ylim()[1]), xytext=(6, -14),
                            textcoords="offset points", color=STATUS["정비 필요 시점"], fontweight="bold")
        sp = g.index[g["판정"] == "점검 권고(단발 튐)"]
        for i in sp:
            if col == "진동(mm/s)":
                ax.annotate(f"단발 튐 {g.loc[i, '시각']} ({g.loc[i, col]})", (i, g.loc[i, col]), xytext=(12, -4),
                            textcoords="offset points", color=STATUS["점검 권고(단발 튐)"], fontweight="bold")
        ax.set_ylabel(col)
        ax.grid(axis="y", color=GRID)
        if r == 0:
            ax.set_title(EQNAME[eq], fontsize=14, color=INK, fontweight="bold", loc="left")
            ax.text(NBASE / 2 - .5, ax.get_ylim()[1], "기준(학습) 구간", ha="center", va="top", color=MUTED, fontsize=10)
    axes[2, c].set_xticks(x[::2], g["시각"][::2], rotation=45)
fig.legend(handles=legend_handles() + [mpatches.Patch(color="#DBEAFE", label="기준 평균 ± 3σ")],
           loc="upper center", ncol=6, frameon=False, bbox_to_anchor=(.5, .955))
fig.suptitle("6가지 이상치 탐지 기법의 다수결 판정 — 설비B는 13:20이 정비 필요 시점", fontsize=18, color=INK, fontweight="bold", y=.995)
fig.text(.5, .005, NOTE, ha="center", color=MUTED, fontsize=10)
fig.tight_layout(rect=(0, .02, 1, .93))
fig.savefig("01_시계열_판정.png", dpi=130)
plt.close(fig)

# 02 기법 × 시간 탐지 히트맵 + 득표 ------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(17, 8.5), gridspec_kw={"height_ratios": [6, 2.2], "hspace": .5, "wspace": .08})
for c, eq in enumerate(EQS):
    g = res[res["설비명"] == eq].reset_index(drop=True)
    M = np.array([g[f"탐지_{k}"].values for k, *_ in METHODS])
    ax = axes[0, c]
    ax.imshow(M, cmap=matplotlib.colors.ListedColormap(["#F3F4F6", "#D7263D"]), aspect="auto", vmin=0, vmax=1)
    ax.set_xticks(np.arange(len(g)) + .5, minor=True); ax.set_yticks(np.arange(6) + .5, minor=True)
    ax.grid(which="minor", color="white", lw=2); ax.tick_params(which="minor", length=0)
    ax.set_yticks(range(6), [m[1] for m in METHODS] if c == 0 else [""] * 6)
    ax.set_xticks(range(len(g)), g["시각"], rotation=90, fontsize=9)
    ax.axvline(NBASE - .5, color=INK, lw=1.5, ls=":")
    ax.set_title(EQNAME[eq], loc="left", fontsize=14, color=INK, fontweight="bold", pad=10)
    for s in ax.spines.values(): s.set_visible(False)
    ax2 = axes[1, c]
    ax2.bar(range(len(g)), g["득표(6)"], color=[STATUS[s] for s in g["판정"]], width=.75)
    ax2.axhline(VOTE_TH - .5, color=INK, lw=1, ls="--")
    ax2.text(-.4, VOTE_TH - .3, f"{VOTE_TH}표 이상 = 이상 확정", ha="left", va="bottom", fontsize=9, color=INK)
    ax2.set_ylim(0, 6.5); ax2.set_yticks([0, 2, 4, 6]); ax2.set_xlim(-.5, len(g) - .5)
    ax2.set_xticks(range(len(g))[::2], g["시각"][::2], rotation=90, fontsize=9)
    ax2.set_ylabel("득표(6기법)" if c == 0 else "")
    for i in g.index[g["정비필요시점"] == "◆"]:
        ax2.annotate("◆ 정비 필요", (i, g.loc[i, "득표(6)"]), xytext=(0, 4), textcoords="offset points",
                     ha="center", color=STATUS["정비 필요 시점"], fontweight="bold", fontsize=10)
fig.legend(handles=[mpatches.Patch(color="#D7263D", label="해당 기법이 이상으로 탐지"), mpatches.Patch(color="#F3F4F6", label="미탐지")] + legend_handles(),
           loc="upper center", ncol=7, frameon=False, bbox_to_anchor=(.5, .965), fontsize=10)
fig.suptitle("기법마다 민감도가 다르다 — 그래서 6표 중 4표 다수결로 판정", fontsize=18, color=INK, fontweight="bold", y=1.02)
fig.text(.5, .01, NOTE + " · 점선 왼쪽 = 기준 구간", ha="center", color=MUTED, fontsize=10)
fig.savefig("02_기법별_탐지_히트맵.png", dpi=130, bbox_inches="tight")
plt.close(fig)

# 03 설비B 점수 곡선 (기법별 임계값 대비) -------------------------------------------
g = res[res["설비명"] == "설비B"].reset_index(drop=True)
x = np.arange(len(g))
curves = [("Z-점수", g["Z최대"], 3), ("마할라노비스 거리", g["마할라노비스"], 3.368),
          ("LOF", g["LOF점수"], 1.5), ("CUSUM", g["CUSUM"], 5)]
fig, axes = plt.subplots(1, 4, figsize=(17, 4.6), sharex=True)
mi = int(g.index[g["정비필요시점"] == "◆"][0])
for ax, (name, y, th) in zip(axes, curves):
    ax.plot(x, y, color=LINE, lw=2)
    ax.axhline(th, color="#D7263D", lw=1.2, ls="--")
    ax.text(0, th, f" 임계값 {th:g}", va="bottom", color="#D7263D", fontsize=9)
    ax.fill_between(x, th, y, where=y > th, color="#FCA5A5", alpha=.6, lw=0)
    ax.axvline(mi, color=STATUS["정비 필요 시점"], lw=1.5, ls=":")
    first = int(np.argmax(y.values > th)) if (y > th).any() else None
    if first is not None:
        ax.scatter([first], [y[first]], color="#D7263D", s=60, zorder=3, edgecolor="white")
        ax.annotate(f"첫 탐지 {g.loc[first, '시각']}", (first, y[first]), xytext=(-8, 18), textcoords="offset points",
                    ha="right", color=INK, fontsize=10, fontweight="bold")
    ax.set_yscale("log" if name != "CUSUM" else "linear"); ax.yaxis.set_major_formatter(PLAIN); ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); ax.set_title(name, loc="left", color=INK, fontweight="bold")
    ax.set_xticks(x[::4], g["시각"][::4], rotation=45); ax.grid(axis="y", color=GRID)
fig.suptitle("설비B(차체 용접로봇 감속기) — 기법별 이상 점수가 임계값을 넘는 순간 (CUSUM 외 로그 눈금)", fontsize=16, color=INK, fontweight="bold")
fig.text(.5, .01, NOTE + " · 점선 세로줄 = 정비 필요 시점 13:20", ha="center", color=MUTED, fontsize=10)
fig.tight_layout(rect=(0, .09, 1, .95))
fig.savefig("03_설비B_점수곡선.png", dpi=130)
plt.close(fig)

# 04 특징 공간 산점도 (z 온도 vs z 진동) --------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))
for ax, eq in zip(axes, EQS):
    g = res[res["설비명"] == eq].reset_index(drop=True)
    t = np.linspace(0, 2 * np.pi, 100)
    ax.fill(3 * np.cos(t), 3 * np.sin(t), color="#DBEAFE", alpha=.8, lw=0, label="정상 영역(약 ±3σ)")
    ax.plot(g["z_온도"], g["z_진동"], color="#CBD5E1", lw=1, zorder=1)
    ax.scatter(g["z_온도"], g["z_진동"], c=[STATUS[s] for s in g["판정"]], s=70, edgecolor="white", lw=1.5, zorder=3)
    for i, r in g.iterrows():
        if r["판정"] != "정상" and (i % 2 == 0 or r["정비필요시점"] == "◆" or r["판정"] == "점검 권고(단발 튐)" or i == len(g) - 1):
            ax.annotate(r["시각"], (r["z_온도"], r["z_진동"]), xytext=(6, 4), textcoords="offset points", fontsize=9, color=INK)
    ax.set_xscale("symlog", linthresh=3); ax.set_yscale("symlog", linthresh=3)
    ax.set_xticks([-3, 0, 3, 10, 30]); ax.set_yticks([-3, 0, 3, 10, 30])
    ax.xaxis.set_major_formatter(PLAIN); ax.yaxis.set_major_formatter(PLAIN)
    ax.axhline(0, color=GRID); ax.axvline(0, color=GRID)
    ax.set_xlabel("온도 z (기준 대비 표준편차 배수)"); ax.set_ylabel("진동 z")
    ax.set_title(EQNAME[eq], loc="left", color=INK, fontweight="bold", fontsize=14)
axes[0].text(.03, .97, "한 점만 위로 튀고\n바로 돌아옴 → 단발 튐", transform=axes[0].transAxes, va="top", color=STATUS["점검 권고(단발 튐)"], fontweight="bold")
axes[1].text(.03, .97, "정상 영역을 벗어나\n오른쪽 위로 계속 이동 → 지속 추세", transform=axes[1].transAxes, va="top", color=STATUS["이상(지속)"], fontweight="bold")
fig.legend(handles=legend_handles() + [mpatches.Patch(color="#DBEAFE", label="정상 영역(약 ±3σ)")], loc="upper center", ncol=6, frameon=False, bbox_to_anchor=(.5, .93))
fig.suptitle("특징 공간에서 본 이상치 — 튐(점)과 추세(궤적)는 모양이 다르다", fontsize=17, color=INK, fontweight="bold")
fig.text(.5, .01, NOTE + " · 축은 ±3 밖에서 로그 눈금", ha="center", color=MUTED, fontsize=10)
fig.tight_layout(rect=(0, .03, 1, .88))
fig.savefig("04_특징공간_궤적.png", dpi=130)
plt.close(fig)
print("ok")
