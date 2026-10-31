"""site/index.html(아티팩트용) → deploy/index.html(GitHub Pages용 단독 문서)"""
src = open("site/index.html", encoding="utf-8").read()
head, body = src.split("<!--BODY-->")
head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
out = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       + head + "</head>\n<body>" + body + "</body>\n</html>\n")
open("deploy/index.html", "w", encoding="utf-8", newline="\n").write(out)
print("ok", len(out))
