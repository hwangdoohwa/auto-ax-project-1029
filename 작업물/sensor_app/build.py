import json, os
src = open("app_src.html", encoding="utf-8").read()
csv = open("../Day5_설비센서_50건_가상.csv", encoding="utf-8-sig").read()
src = src.replace('/*SAMPLE*/""', json.dumps(csv, ensure_ascii=False))
head, body = src.split("<!--BODY-->")
open("artifact.html", "w", encoding="utf-8", newline="\n").write(head + body)
os.makedirs("deploy", exist_ok=True)
std = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       + head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '') + '</head>\n<body>' + body + '</body>\n</html>\n')
open("deploy/index.html", "w", encoding="utf-8", newline="\n").write(std)
print("ok", len(std))
