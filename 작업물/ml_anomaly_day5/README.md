# 머신러닝 이상치 탐지 6기법 · 정비 필요 시점

데이터: `Day5_설비센서_50건_가상.csv`(실습용 가상 데이터, 설비 2대 × 25건). 설비별 오전 08:00~11:40, 12건을 정상 기준으로 학습했습니다.

## 결과

| 설비 | 판정 | 정비 필요 시점 | 근거 |
|---|---|---|---|
| 설비B 차체 용접로봇 감속기 | 정비 필요 | **13:20** | 12:20에 첫 관찰(3표) → 13:00부터 4표 이상 연속 → 일시 튐이 아닌 지속 추세, 주원인 온도 |
| 설비A 프레스 메인모터 | 점검 권고(단발 튐) | 해당 없음 | 12:40 진동 3.5 한 번만 5표, 바로 정상 복귀 |

- [예지보전 보고서 PDF](예지보전_보고서.pdf) — 현황 진단 · 이상 패턴과 원인 추정 · 정비 권고 시점 · 개선안(점검 주기 · 임계값). 추정한 부분은 "(추정)"으로 표시
- [구글 시트](https://docs.google.com/spreadsheets/d/1WIAS0qqYMprRdzTr3ZxAuTdqk356TdoK8fY6MPpJ5S0/edit) · [공개 페이지](https://hwangdoohwa.github.io/auto-ax-project-1029/#works)

## 기법과 판정 규칙

| 기법 | 계열 | 임계값 |
|---|---|---|
| Z-점수 | 통계(단변량) | \|z\| > 3 |
| 마할라노비스 거리 | 통계(다변량) | > 3.37 (χ² 3자유도 99%) |
| Isolation Forest | 트리 앙상블(비지도) | 50건 중 하위 20% |
| LOF | 밀도 기반(준지도) | LOF 점수 > 1.5 |
| One-Class SVM | 경계 학습(준지도) | nu=0.05, γ=0.02 경계 밖 |
| CUSUM | 누적합(추세) | 누적합 > 5 (k=1, \|z\| ≤ 4로 자름) |

득표 0~1 정상 · 2~3 관찰 · 4표 이상 1회 = 점검 권고(단발 튐) · 4표 이상 2회 연속 = 두 번째 시점이 정비 필요 시점.

One-Class SVM은 학습 표본이 12건뿐이라 과민합니다(설비A 정상 구간도 11건 탐지). 그래서 한 기법만으로 판정하지 않고 다수결로 묶었습니다.

탐지 결과는 고장 확정이 아닙니다. 설비를 자동으로 멈추지 않고, 담당자 검토·승인 뒤 비가동 시간에 정비 일정을 잡습니다.

## 다시 돌리기

```bash
pip install numpy pandas scipy scikit-learn matplotlib cairosvg openpyxl
python analyze_ml.py        # 결과 CSV 3개 (원자료 CSV를 한 단계 위 폴더에 둠)
python charts.py            # matplotlib 차트 4장
python make_infographic.py  # SVG·PNG 인포그래픽 (cairosvg, Windows는 GTK3 런타임)
python make_sheet_csv.py    # 구글 시트 업로드용 CSV
python make_sheet.py        # 탭 4개 xlsx
```
