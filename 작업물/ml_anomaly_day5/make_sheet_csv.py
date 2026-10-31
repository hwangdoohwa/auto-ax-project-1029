"""구글 시트 업로드용 한 장짜리 CSV (요약 → 기법 → 50건 순)."""
import csv, pandas as pd
res = pd.read_csv("결과_시점별_판정.csv", encoding="utf-8-sig")
summ = pd.read_csv("결과_기법별_요약.csv", encoding="utf-8-sig")
dec = pd.read_csv("결과_정비판정.csv", encoding="utf-8-sig")
rows = [["[1] 정비 판정 — 실습용 가상 데이터 · 탐지는 고장 확정이 아님 · 자동 정지 금지 · 담당자 검토·승인 후 정비"]]
rows += [list(dec.columns)] + dec.astype(str).values.tolist() + [[]]
rows += [["[2] 판정 규칙: 기준 구간 08:00~11:40(설비별 12건)으로 학습 · 6기법 득표 0~1 정상 / 2~3 관찰 / 4+ 1회 점검 권고(단발 튐) / 4+ 2회 연속 → 두 번째 시점 = 정비 필요 시점"]]
rows += [[]]
rows += [["[3] 기법별 요약"]] + [list(summ.columns)] + summ.astype(str).values.tolist() + [[]]
cols = ["시간", "설비명", "진동(mm/s)", "온도(℃)", "압력(bar)", "Z최대", "마할라노비스", "IF점수", "LOF점수", "OCSVM점수", "CUSUM",
        "탐지_z", "탐지_md", "탐지_iso", "탐지_lof", "탐지_ocsvm", "탐지_cusum", "득표(6)", "판정", "주원인", "정비필요시점"]
hdr = ["시간", "설비", "진동(mm/s)", "온도(℃)", "압력(bar)", "Z최대", "마할라노비스", "IF점수", "LOF점수", "OCSVM점수", "CUSUM",
       "Z", "MD", "IF", "LOF", "OCSVM", "CUSUM탐지", "득표(6)", "판정", "주원인", "정비필요시점"]
rows += [["[4] 시점별 판정 50건 (탐지 1 = 이상)"], hdr]
rows += res[cols].fillna("").astype(str).values.tolist()
with open("구글시트_업로드.csv", "w", encoding="utf-8", newline="") as f:
    csv.writer(f, lineterminator="\n").writerows(rows)
