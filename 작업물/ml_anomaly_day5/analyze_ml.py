"""Day5 설비센서 50건(실습용 가상 데이터) — 머신러닝 이상치 탐지 6기법 + 정비 필요 시점 판정.

기준 구간: 설비별 오전 08:00~11:40 (12건)을 '정상'으로 보고 학습한다.
판정 규칙
  - 6기법 중 4표 이상 = 이상 확정 지점
  - 이상 확정이 2회 연속  → 두 번째 시점이 '정비 필요 시점' (지속 추세)
  - 이상 확정이 1회로 끝남 → '점검 권고(단발 튐)'
  - 2~3표 → '관찰', 0~1표 → '정상'
탐지 결과는 고장 확정이 아니다. 담당자 검토·승인 후 정비 일정을 잡는다(자동 정지 금지).
"""
import json
import numpy as np
import pandas as pd
from scipy.stats import chi2
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM

SRC = "../Day5_설비센서_50건_가상.csv"
F = ["진동(mm/s)", "온도(℃)", "압력(bar)"]
NBASE = 12
MD_TH = float(np.sqrt(chi2.ppf(0.99, 3)))  # 3.37
CUSUM_K, CUSUM_H, CLIP = 1.0, 5.0, 4.0
VOTE_TH = 4

METHODS = [
    # key, 이름, 계열, 원리, 임계값
    ("z", "Z-점수", "통계(단변량)", "오전 평균에서 몇 σ 떨어졌나 (변수별 최댓값)", "|z| > 3"),
    ("md", "마할라노비스 거리", "통계(다변량)", "세 변수의 상관까지 반영한 거리", f"> {MD_TH:.2f} (χ² 3자유도 99%)"),
    ("iso", "Isolation Forest", "트리 앙상블(비지도)", "무작위 분할로 빨리 고립되는 점이 이상", "전체 50건 중 하위 20%"),
    ("lof", "LOF", "밀도 기반(준지도)", "이웃 5개보다 주변 밀도가 낮으면 이상", "LOF 점수 > 1.5"),
    ("ocsvm", "One-Class SVM", "경계 학습(준지도)", "정상 데이터를 감싸는 경계 밖이면 이상", "nu=0.05, γ=0.02 경계 밖"),
    ("cusum", "CUSUM", "누적합(추세)", "기준 대비 작은 편차를 누적해 서서히 오르는 추세 포착", f"누적합 > {CUSUM_H:g} (k={CUSUM_K:g}, |z|≤{CLIP:g})"),
]


def load():
    df = pd.read_csv(SRC, encoding="utf-8-sig")
    df["시각"] = df["시간"].str[11:16]
    df["설비명"] = df["설비"].str.extract(r"^(설비[AB])")[0]
    return df


def analyze():
    df = load()
    groups = [g.reset_index(drop=True) for _, g in df.groupby("설비", sort=False)]
    Zs = []
    for g in groups:
        b = g.iloc[:NBASE]
        Zs.append(((g[F] - b[F].mean()) / b[F].std()).values)
    # Isolation Forest: 두 설비 50건을 함께 비지도 학습
    Zall = np.vstack(Zs)
    iso = IsolationForest(n_estimators=500, contamination=0.2, random_state=0).fit(Zall)
    iso_score = -iso.score_samples(Zall)  # 클수록 이상
    iso_th = -iso.offset_
    rows = []
    for k, g in enumerate(groups):
        Z, Zb = Zs[k], Zs[k][:NBASE]
        zmax = np.abs(Z).max(1)
        inv = np.linalg.inv(np.cov(Zb.T))
        md = np.sqrt(np.einsum("ij,jk,ik->i", Z, inv, Z))
        lof = LocalOutlierFactor(n_neighbors=5, novelty=True).fit(Zb)
        lof_score = -lof.score_samples(Z)
        oc = OneClassSVM(nu=0.05, gamma=0.02).fit(Zb)
        oc_score = -oc.decision_function(Z)  # > 0 이면 경계 밖
        sp, sn, cus = np.zeros(3), np.zeros(3), []
        for z in np.clip(Z, -CLIP, CLIP):
            sp = np.maximum(0, sp + z - CUSUM_K)
            sn = np.maximum(0, sn - z - CUSUM_K)
            cus.append(max(sp.max(), sn.max()))
        cus = np.array(cus)
        flags = {
            "z": zmax > 3, "md": md > MD_TH, "iso": iso_score[k * 25:(k + 1) * 25] > iso_th,
            "lof": lof_score > 1.5, "ocsvm": oc_score > 0, "cusum": cus > CUSUM_H,
        }
        votes = sum(f.astype(int) for f in flags.values())
        hit = votes >= VOTE_TH
        status = np.where(votes >= 2, "관찰", "정상").astype(object)
        maint_idx = None
        for i in range(len(g)):
            if hit[i]:
                persist = (i > 0 and hit[i - 1]) or (i + 1 < len(g) and hit[i + 1])
                status[i] = "이상(지속)" if persist else "점검 권고(단발 튐)"
                if maint_idx is None and i > 0 and hit[i - 1]:
                    maint_idx = i
        is_maint = np.zeros(len(g), bool)
        if maint_idx is not None:
            status[maint_idx] = "정비 필요 시점"
            is_maint[maint_idx] = True
        # 어떤 변수가 원인인가
        cause = [F[int(np.argmax(np.abs(z)))].split("(")[0] if v >= 2 else "" for z, v in zip(Z, votes)]
        for i in range(len(g)):
            r = {"시간": g.loc[i, "시간"], "시각": g.loc[i, "시각"], "설비": g.loc[i, "설비"], "설비명": g.loc[i, "설비명"],
                 "구간": "기준(오전)" if i < NBASE else "판정",
                 **{c: g.loc[i, c] for c in F},
                 **{f"z_{c.split('(')[0]}": round(float(Z[i, j]), 2) for j, c in enumerate(F)},
                 "Z최대": round(float(zmax[i]), 2), "마할라노비스": round(float(md[i]), 2),
                 "IF점수": round(float(iso_score[k * 25 + i]), 3), "LOF점수": round(float(lof_score[i]), 2),
                 "OCSVM점수": round(float(oc_score[i]), 3), "CUSUM": round(float(cus[i]), 2)}
            for key, *_ in METHODS:
                r[f"탐지_{key}"] = int(flags[key][i])
            r.update({"득표(6)": int(votes[i]), "판정": status[i], "주원인": cause[i], "정비필요시점": "◆" if is_maint[i] else ""})
            rows.append(r)
    return pd.DataFrame(rows)


def summarize(res):
    out = []
    for key, name, fam, idea, th in METHODS:
        d = {"기법": name, "계열": fam, "원리": idea, "임계값": th}
        for eq in ["설비A", "설비B"]:
            s = res[(res["설비명"] == eq) & (res[f"탐지_{key}"] == 1)]
            d[f"{eq} 탐지 건수"] = len(s)
            d[f"{eq} 첫 탐지"] = s["시각"].iloc[0] if len(s) else "-"
        out.append(d)
    return pd.DataFrame(out)


def decisions(res):
    out = []
    for eq, g in res.groupby("설비명"):
        m = g[g["정비필요시점"] == "◆"]
        spikes = g[g["판정"] == "점검 권고(단발 튐)"]
        watch = g[g["판정"] == "관찰"]
        if len(m):
            r = m.iloc[0]
            first = g[g["득표(6)"] >= VOTE_TH]["시각"].iloc[0]
            out.append({"설비": r["설비"], "판정": "정비 필요", "정비 필요 시점": r["시각"],
                        "근거": f"{first}부터 6기법 중 {VOTE_TH}표 이상이 연속 → 일시 튐이 아닌 지속 추세",
                        "주원인": r["주원인"], "첫 관찰 신호": watch["시각"].iloc[0] if len(watch) else "-",
                        "다음 조치": "담당자 검토·승인 후 다음 비가동 시간에 감속기 점검(윤활·베어링) 일정 확정"})
        elif len(spikes):
            r = spikes.iloc[0]
            out.append({"설비": r["설비"], "판정": "점검 권고(단발 튐)", "정비 필요 시점": "해당 없음",
                        "근거": f"{r['시각']} {r['주원인']} 1회만 {int(r['득표(6)'])}표, 직후 정상 복귀",
                        "주원인": r["주원인"], "첫 관찰 신호": r["시각"],
                        "다음 조치": "센서 접촉·순간 충격 여부 확인, 같은 패턴 반복 시 정비 검토"})
        else:
            out.append({"설비": g["설비"].iloc[0], "판정": "정상", "정비 필요 시점": "해당 없음", "근거": "-",
                        "주원인": "-", "첫 관찰 신호": "-", "다음 조치": "-"})
    return pd.DataFrame(out)


if __name__ == "__main__":
    res = analyze()
    summ = summarize(res)
    dec = decisions(res)
    res.to_csv("결과_시점별_판정.csv", index=False, encoding="utf-8-sig")
    summ.to_csv("결과_기법별_요약.csv", index=False, encoding="utf-8-sig")
    dec.to_csv("결과_정비판정.csv", index=False, encoding="utf-8-sig")
    json.dump({"methods": METHODS, "vote_th": VOTE_TH}, open("meta.json", "w", encoding="utf-8"), ensure_ascii=False)
    pd.set_option("display.width", 250)
    print(res[["설비명", "시각", "Z최대", "마할라노비스", "득표(6)", "판정", "주원인", "정비필요시점"]].to_string())
    print(summ.drop(columns=["원리"]).to_string())
    print(dec.to_string())
    # 검증: 기대 결과
    assert dec.set_index("설비").filter(like="설비B", axis=0)["정비 필요 시점"].iloc[0] == "13:20"
    assert (res[(res["설비명"] == "설비A")]["정비필요시점"] == "").all()
