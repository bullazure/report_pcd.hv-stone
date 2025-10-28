import os

base_dir = r"C:\report_pcd"
os.chdir(base_dir)

# 최신 리포트 파일 찾기
html_files = sorted(
    [f for f in os.listdir(base_dir) if f.startswith("report_pcd_") and f.endswith(".html")],
    reverse=True
)
if not html_files:
    print("⚠️ HTML 파일이 없습니다.")
    exit()

latest_file = html_files[0]

# === archive.html 생성 ===
archive_html = """<html>
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex, nofollow">
<title>Report Archive</title>
<style>
  body {{ font-family: Arial, sans-serif; }}
  ul {{ line-height: 1.8; }}
</style>
</head>
<body>
<h1 style="font-size:20px;">리포트 목록</h1>
<ul>
"""
for f in html_files:
    archive_html += f'  <li><a href="{f}">{f}</a></li>\n'
archive_html += """</ul>
</body>
</html>
"""

with open("archive.html", "w", encoding="utf-8") as f:
    f.write(archive_html)
print("✅ archive.html 생성 완료")

# === 최신 리포트 파일 내용 읽기 ===
with open(latest_file, "r", encoding="utf-8") as f:
    latest_content = f.read()

# === index.html 생성 (본문 직접 삽입) ===
index_html = f"""<html>
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex, nofollow">
<title>Latest Report (report_pcd)</title>
<style>
  body {{ font-family: Arial, sans-serif; }}
  .header-line {{
      display: flex;
      justify-content: space-between;
      align-items: center;
  }}
  h21 {{ font-size: 20px; margin: 5; }}
  a {{ font-size: 16px; text-decoration: none; color: #007bff; }}
  hr21 {{ margin: 8px 0; }}
</style>
</head>
<body>
<div class="header-line">
  <h21>최신 리포트</h21>
  <a href="archive.html">리포트 목록</a>
</div>
<hr21>
{latest_content}
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print(f"✅ index.html 생성 완료 (최신 파일 본문 삽입됨: {latest_file})")
