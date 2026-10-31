"""app_src.html + data.json → 배포용 index.html (홈페이지 deploy/pdm-report/)."""
import os
src = open("app_src.html", encoding="utf-8").read()
data = open("data.json", encoding="utf-8").read()
assert "/*DATA*/null" in src
html = src.replace("/*DATA*/null", data)
out = "../../webtoon_github/deploy/pdm-report"
os.makedirs(out, exist_ok=True)
open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
print("ok", len(html))
