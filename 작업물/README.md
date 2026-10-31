# 실습 작업물 소스

공개 페이지: https://hwangdoohwa.github.io/auto-ax-project-1029/#works

| 폴더 | 내용 | 결과물 |
|---|---|---|
| `sensor_app/` | 설비센서 이상 후보 탐지기 원본(`app_src.html`)과 빌드 스크립트 | [웹앱](https://hwangdoohwa.github.io/auto-ax-project-1029/sensor-app/) |
| `sensor_analysis_day5/` | 설비별 평균·표준편차·평상 범위(평균 ± 2σ) 계산과 matplotlib 차트 | [시계열](https://hwangdoohwa.github.io/auto-ax-project-1029/day5/sensor_timeseries.png) · [z-점수](https://hwangdoohwa.github.io/auto-ax-project-1029/day5/sensor_zscore.png) |
| `infographic_day5/` | 예지보전 인포그래픽 2장 생성 코드와 검증 메모 | [도입사례 5건](https://hwangdoohwa.github.io/auto-ax-project-1029/day5/case5.png) · [센서 50건](https://hwangdoohwa.github.io/auto-ax-project-1029/day5/sensor_story.png) |
| `webtoon/` | 웹툰 숏폼 EP.01 「용광로가 배우다」·특별편 렌더 코드와 대본 | [영상 보기](https://hwangdoohwa.github.io/auto-ax-project-1029/#videos) |
| `homepage/` | 소개 홈페이지 원본과 Pages용 빌드 스크립트 | [홈페이지](https://hwangdoohwa.github.io/auto-ax-project-1029/) |

## 다시 만들 때 필요한 것

- 스크립트는 과정 실습 데이터 `Day5_설비센서_50건_가상.csv`, `Day5_예지보전_도입사례_실데이터.csv`를 한 단계 위 폴더에서 읽습니다. 원자료는 이 저장소에 넣지 않았습니다.
- 웹툰 렌더 코드는 별도 스킬의 `webtoon_lib.py`(캐릭터·말풍선·렌더 함수)가 같은 폴더에 있어야 돌아갑니다. 이 라이브러리는 포함하지 않았습니다.
- Python 패키지: numpy, pillow, matplotlib, cairosvg(Windows는 GTK3 런타임 필요), ffmpeg.
- 센서 데이터는 실습용 가상 데이터이며, 이상 후보는 고장 확정이 아닙니다. 담당자 검토·승인 후 조치합니다.
