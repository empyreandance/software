#!/usr/bin/env python3
"""Build index.html from apps-page-src.html by inlining icons/ and shots/ as data URIs.
Galleries whose shot files are missing are dropped gracefully."""
import base64, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
src = open('apps-page-src.html').read()
for m in set(re.findall(r'\{\{SHOT:([\w-]+)\}\}', src)):
    if not os.path.exists(f'shots/{m}.jpg'):
        src = re.sub(r'  \w+: \[[^\]]*\{\{SHOT:' + m + r'\}\}[^\]]*\n  \],\n', '', src, flags=re.S)
icon = lambda m: 'data:image/png;base64,' + base64.b64encode(open(f'icons/{m.group(1)}-web.png', 'rb').read()).decode()
shot = lambda m: 'data:image/jpeg;base64,' + base64.b64encode(open(f'shots/{m.group(1)}.jpg', 'rb').read()).decode()
out = re.sub(r'\{\{ICON:([\w-]+)\}\}', icon, src)
out = re.sub(r'\{\{SHOT:([\w-]+)\}\}', shot, out)
assert not re.findall(r'\{\{[A-Z]+:[\w-]+\}\}', out)
open('index.html', 'w').write(out)
print('built index.html:', os.path.getsize('index.html'), 'bytes')
