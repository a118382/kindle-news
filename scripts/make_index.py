#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 converted_ebooks/ 里的电子书重命名成 ASCII 安全文件名，
并生成 index.json / index.html 供 Kindle 端拉取。

输出文件名格式: YYYY-MM-DD-news-NN.<ext>
（Kindle 5.x 的 curl/wget 不擅长处理 URL 里的中文和空格，所以文件名必须是纯 ASCII）
"""
import json
import os
import glob
import datetime
import re

OUT = os.environ.get('output', 'converted_ebooks')
EXT = os.environ.get('ext', 'azw3').lower()

today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
stamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

sources = sorted(glob.glob(os.path.join(OUT, '*.' + EXT)))
files = []

for idx, src in enumerate(sources, 1):
    title = os.path.splitext(os.path.basename(src))[0]
    safe = '%s-news-%02d.%s' % (today, idx, EXT)
    dst = os.path.join(OUT, safe)
    if src != dst:
        os.replace(src, dst)
    files.append({
        'name': safe,
        'title': title,
        'size': os.path.getsize(dst),
        'date': today,
    })

meta = {
    'updated': stamp,
    'count': len(files),
    'files': files,
}

with open(os.path.join(OUT, 'index.json'), 'w', encoding='utf-8') as fh:
    json.dump(meta, fh, ensure_ascii=False, indent=2)

rows = []
for f in files:
    rows.append(
        '<li><a href="%s">%s</a> <span class="m">(%s / %.1f MB)</span></li>'
        % (f['name'], f['title'], f['date'], f['size'] / 1048576.0)
    )

html = (
    '<!DOCTYPE html><html><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Kindle News</title>'
    '<style>body{font-family:-apple-system,"PingFang SC",sans-serif;'
    'max-width:640px;margin:40px auto;padding:0 16px;line-height:1.6}'
    '.m{color:#888;font-size:.85em}</style></head><body>'
    '<h1>Kindle News</h1>'
    '<p>生成时间: %s (UTC) &middot; 共 %d 本</p>'
    '<ul>%s</ul>'
    '<p><a href="index.json">index.json</a></p>'
    '</body></html>'
) % (stamp, len(files), ''.join(rows))

with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8') as fh:
    fh.write(html)

print('index.json: %d file(s)' % len(files))
for f in files:
    print('  %s  <-  %s' % (f['name'], f['title']))
