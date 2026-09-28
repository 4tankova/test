from pathlib import Path
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
if not path.exists():
    raise SystemExit(f"Не знайдено файл: {path}")

html = path.read_text(encoding="utf-8")

head_block = """    <link rel="manifest" href="./manifest.webmanifest">
    <meta name="theme-color" content="#007bff">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="Емо-тест">
    <link rel="apple-touch-icon" href="./icon-192.png">
"""

sw_block = """
    <script>
      if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
          navigator.serviceWorker.register('./sw.js', { scope: './' })
            .catch(error => console.error('Service Worker registration failed:', error));
        });
      }
    </script>
"""

# Remove external Google Fonts dependency for true offline use
lines = html.splitlines()
lines = [line for line in lines if "fonts.googleapis.com" not in line]
html = "\n".join(lines)

# Replace Inter-only font with a system stack
html = html.replace(
    "font-family: 'Inter', sans-serif;",
    "font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;"
)

if 'rel="manifest"' not in html:
    html = html.replace("</head>", head_block + "</head>")

if "navigator.serviceWorker.register" not in html:
    html = html.replace("</body>", sw_block + "\n</body>")

backup = path.with_suffix(path.suffix + ".bak")
backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
path.write_text(html + ("\n" if not html.endswith("\n") else ""), encoding="utf-8")

print(f"Готово: {path}")
print(f"Резервна копія: {backup}")
