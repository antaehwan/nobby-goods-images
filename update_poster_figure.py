"""카탈로그 피드의 카드스티커(큰칩·작은칩)·떡메모지 image_link를 포스터 인물판 대표 이미지로 바꾼다 (11/15).
사용: python3 update_poster_figure.py 174,130
- 새 그림은 main/p2_<스토어번호>.png 로 저장(메타는 같은 주소를 다시 받지 않으므로 새 이름). 투명 부분은 베이지(246,236,214).
- 피드(catalog_add_1027*.csv)에 있는 행만 image_link를 바꾼다. 피드에 없는 상품(Commerce Manager 직접 등록분)은 목록만 출력.
"""
import csv, io, os, sys
from PIL import Image
R = os.path.dirname(os.path.abspath(__file__))
G = "/Users/antaehwan/Library/CloudStorage/OneDrive-개인/03. SI/00. 노비팀/05. 굿즈샵/"
SRC = G + "03. 제작 원본/03. 스토어 이미지_포스터인물/"
RAW = "https://raw.githubusercontent.com/antaehwan/nobby-goods-images/main/main/p2_%s.png"
KIND = {"카드스티커 큰칩": "카드스티커_%s", "카드스티커 작은칩": "카드스티커_스몰칩_%s", "떡메모지": "떡메모지_%s"}
nums = [x.zfill(3) for x in sys.argv[1].split(",")]
rows = list(csv.DictReader(open(G + "02. 스토어 관리/03. 상품 번호표_1027.csv", encoding="utf-8-sig")))
want = {}
for r in rows:
    if r["표어 호수"].zfill(3) in nums and r["종류"] in KIND:
        want[r["스토어 상품번호"]] = SRC + KIND[r["종류"]] % r["표어 호수"].zfill(3) + "/대표.png"
found = set()
for fn in sorted(f for f in os.listdir(R) if f.startswith("catalog_add_") and f.endswith(".csv")):
    p = os.path.join(R, fn); raw = open(p, "rb").read(); bom = raw.startswith(b"\xef\xbb\xbf"); nl = "\r\n" if b"\r\n" in raw else "\n"; text = raw.decode("utf-8-sig")
    rd = list(csv.reader(io.StringIO(text))); head = rd[0]; ii = head.index("image_link"); changed = 0
    for row in rd[1:]:
        if row and row[0] in want:
            im = Image.open(want[row[0]]).convert("RGBA"); bg = Image.new("RGB", im.size, (246, 236, 214)); bg.paste(im, mask=im.split()[3])
            bg.save(os.path.join(R, "main", "p2_%s.png" % row[0])); row[ii] = RAW % row[0]; changed += 1; found.add(row[0])
    if changed:
        out = io.StringIO(); w = csv.writer(out, lineterminator=nl); w.writerows(rd); open(p, "wb").write((b"\xef\xbb\xbf" if bom else b"") + out.getvalue().encode("utf-8"))
        print(fn, "바꿈", changed)
miss = [k for k in want if k not in found]
print("피드에 없음(커머스 관리자에서 직접 바꿔야 함):", miss)
