import os
import re

# === 경로 설정 (상대경로 기준) ===
base_dir = os.path.dirname(__file__)
report_dir = os.path.join(base_dir, "report_pcd")
os.chdir(base_dir)

# === report_pcd 폴더 내 리포트 파일 수집 ===
html_files = sorted(
    [f for f in os.listdir(report_dir)
     if f.startswith("report_pcd_") and f.endswith(".html")],
    reverse=True
)

if not html_files:
    print("⚠️ report_pcd 폴더에 HTML 리포트가 없습니다.")
    raise SystemExit

latest_files = html_files
latest_default = latest_files[0]

# === YYYYMMDD만 버튼 라벨로 추출 ===
def yyyymmdd(name: str) -> str:
    m = re.search(r"(\d{8})", name)
    return m.group(1) if m else name

# === archive.html 생성 ===
archive_html = """<html>
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex, nofollow">
<title>Report Archive</title>
<style>
  .shell { font-family: Arial, sans-serif; margin: 20px; }
  .shell ul { line-height: 1.8; }
  .shell h1 { font-size: 20px; margin: 0 0 10px 0; }
  .shell a { color: #007bff; text-decoration: none; }
  .shell a:hover { text-decoration: underline; }
</style>
</head>
<body class="shell">
<h1>리포트 목록</h1>
<ul>
"""
for f in html_files:
    archive_html += f'  <li><a href="report_pcd/{f}">{f}</a></li>\n'
archive_html += """</ul>
</body>
</html>
"""

with open("archive.html", "w", encoding="utf-8") as f:
    f.write(archive_html)
print("✅ archive.html 생성 완료")

# === index.html 생성 (iframe 반응형) ===
buttons_html = "".join(
    [f"<button onclick=\"showReport('report_pcd/{f}')\">{yyyymmdd(f)}</button>"
     for f in latest_files]
)

index_html = f"""<html>
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex, nofollow">
<title>리포트 전체</title>
<style>
  html, body {{
    height: 100%;
    margin: 0;
  }}
  .shell {{
    font-family: Arial, sans-serif;
    background:#f9fafc;
    height: 100%;
    display: flex;
    flex-direction: column;
  }}
  .header-line {{
    display:flex; justify-content:space-between; align-items:center;
    padding: 10px 20px; background:#fff; border-bottom:1px solid #ddd;
  }}
  .header-line h1 {{ font-size:20px; margin:0; color:#222; }}
  .header-line a {{ font-size:14px; text-decoration:none; color:#007bff; }}
  .header-line a:hover {{ text-decoration:underline; }}
  .btns {{
    flex-shrink: 0;
    padding: 10px 20px;
    background:#fff;
    border-bottom:1px solid #ddd;
  }}
  .btns button {{
    margin:4px; padding:6px 10px; border-radius:5px;
    border:1px solid #bbb; background:#fff; cursor:pointer; font-size:13px;
  }}
  .btns button:hover {{ background:#f0f0f0; }}
  .btns button.active {{ background:#007bff; color:#fff; border-color:#007bff; }}
  #reportFrame {{
    flex: 1;
    width:100%;
    border: none;
  }}
</style>
<script>
function resizeFrame() {{
  const frame = document.getElementById('reportFrame');
  frame.style.height = window.innerHeight - 
    (document.querySelector('.header-line').offsetHeight +
     document.querySelector('.btns').offsetHeight + 10) + 'px';
}}
window.addEventListener('resize', resizeFrame);

function showReport(url) {{
  var btns = document.querySelectorAll('.btns button');
  for (var i=0;i<btns.length;i++) btns[i].classList.remove('active');
  for (var i=0;i<btns.length;i++) if (btns[i].getAttribute('onclick').includes(url)) btns[i].classList.add('active');
  document.getElementById('reportFrame').src = url;
  document.getElementById('fallbackLink').href = url;
  resizeFrame();
}}
window.onload = function() {{
  showReport('report_pcd/{latest_default}');
}};
</script>
</head>
<body class="shell">
  <div class="header-line">
    <h1>리포트 전체</h1>
    <a href="archive.html">리포트 목록</a>
  </div>

  <div class="btns">{buttons_html}</div>

  <iframe id="reportFrame" src="" frameborder="0"></iframe>
  <p style="margin:8px 20px;">
    열리지 않으면 <a id="fallbackLink" href="report_pcd/{latest_default}" target="_blank">새 탭으로 열기</a>
  </p>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print(f"✅ index.html 생성 완료 (전체 {len(latest_files)}개 + 창 크기 자동 맞춤)")
