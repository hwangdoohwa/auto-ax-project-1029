"""웹앱용 data.json: 시점별 점수(임계값은 앱에서 조정) + 기준 통계."""
import json, numpy as np, pandas as pd, sys
sys.path.insert(0, "..")
from sklearn.ensemble import IsolationForest
import analyze_ml as A
A.SRC = "../../Day5_설비센서_50건_가상.csv"
res = pd.read_csv("../결과_시점별_판정.csv", encoding="utf-8-sig")
df = A.load()
Zs = []
for _, g in df.groupby("설비", sort=False):
    b = g.iloc[:A.NBASE]; Zs.append(((g[A.F] - b[A.F].mean()) / b[A.F].std()).values)
iso = IsolationForest(n_estimators=500, contamination=0.2, random_state=0).fit(np.vstack(Zs))
out = {"iso_th": round(float(-iso.offset_), 4), "md_th": round(A.MD_TH, 3), "equip": []}
for eq, g in res.groupby("설비명", sort=True):
    g = g.reset_index(drop=True); b = g.iloc[:A.NBASE]
    out["equip"].append({
        "key": eq, "name": g["설비"].iloc[0],
        "base": {c: [round(b[c].mean(), 3), round(b[c].std(), 3)] for c in A.F},
        "rows": [{"t": r["시각"], "v": r["진동(mm/s)"], "T": r["온도(℃)"], "p": r["압력(bar)"],
                  "zv": r["z_진동"], "zt": r["z_온도"], "zp": r["z_압력"],
                  "z": r["Z최대"], "md": r["마할라노비스"], "iso": r["IF점수"], "lof": r["LOF점수"],
                  "oc": r["OCSVM점수"], "cus": r["CUSUM"]} for _, r in g.iterrows()]})
json.dump(out, open("data.json", "w", encoding="utf-8"), ensure_ascii=False)
print(out["iso_th"], out["md_th"], len(out["equip"][0]["rows"]))
