# Kindle News

Calibre 定时抓新闻 → 生成 `azw3` → 发布到 GitHub Pages → Kindle 上 KUAL 一键拉取。

改造自 [bookfere/Calibre-News-Delivery](https://github.com/bookfere/Calibre-News-Delivery)，
把原来的 **SMTP 邮件推送**换成 **GitHub Pages + KUAL 拉取**。

## 为什么改

| 原方案 | 问题 |
|---|---|
| 输出 `epub` | Kindle 5.12.2.2 原生不认 EPUB，只吃 azw3 / mobi / pdf / txt |
| SMTP → `@kindle.com` | 国行（kindle.cn）账号的 Send to Kindle **已于 2024-06-30 关停** |
| Artifacts 下载 | 每次要点网页，太麻烦 |

## 目录结构

```
.github/workflows/calibre-news.yml   每天 UTC 22:00（北京 06:00）跑一次
scripts/make_index.py                重命名成 ASCII 文件名 + 生成 index.json
recipe_list.txt                      Calibre 内置 recipe 名单，一行一个
zhnews.recipe                        自定义中文源（改 feeds 换源）
```

## 用法

1. **开一次 Actions**：仓库 → Actions → Calibre News Delivery → Run workflow。
2. **开 Pages**：Settings → Pages → Source 选 `gh-pages` 分支 → Save。
   （第一次跑完 workflow 后 `gh-pages` 分支才会出现）
3. **Kindle 端**：KUAL → Kindle News → 拉取今日新闻。

## 换内容源

- 用 Calibre 内置的：往 `recipe_list.txt` 加一行 recipe 名（`ebook-convert --list-recipes` 可查全部）。
- 自定义的：往仓库根目录扔 `xxx.recipe`。
- 中文源直接改 `zhnews.recipe` 里的 `feeds`。

## 改定时

`.github/workflows/calibre-news.yml` 里的 `cron`，UTC 时间。
北京时间减 8 小时，例如北京 07:00 → `0 23 * * *`。
