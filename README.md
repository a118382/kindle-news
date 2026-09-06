# Kindle News

Calibre 定时抓新闻 → 生成 `azw3` → 两条投递通道可选：

- **GitHub Pages + KUAL 拉取**（默认，国行/美区都可用）
- **邮件推送到 `@kindle.com`**（美区账号的 Send to Kindle 邮件通道仍可用）

改造自 [bookfere/Calibre-News-Delivery](https://github.com/bookfere/Calibre-News-Delivery)。

## 为什么改

| 原方案 | 问题 / 处理 |
|---|---|
| 输出 `epub` | Kindle 5.12.2.2 原生不认 EPUB，改成 `azw3` |
| SMTP → `@kindle.cn` | 国行 Send to Kindle **已于 2024-06-30 关停** → 默认走 Pages 拉取 |
| SMTP → `@kindle.com` | 美区仍可用，已作为可选通道加回（见下） |
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
2. **开 Pages**（拉取通道需要）：Settings → Pages → Source 选 `gh-pages` 分支 → Save。
   （第一次跑完 workflow 后 `gh-pages` 分支才会出现）
3. **Kindle 端**（拉取通道）：KUAL → Kindle News → 拉取今日新闻。

## 邮件推送通道（美区账号可选）

在 **仓库 Settings → Secrets and variables → Actions → New repository secret** 填以下 6 个：

| Secret | 含义 | 例子 |
|---|---|---|
| `FROM` | 发件邮箱，**必须已在亚马逊「批准的电邮列表」里**（2025-04-02 起只认完整邮箱，不再认域名） | `you@gmail.com` |
| `TO` | 你的 Kindle 接收邮箱 | `xxx@kindle.com` |
| `SMTP` | `FROM` 对应邮箱的 SMTP 服务器 | `smtp.gmail.com` |
| `PORT` | SMTP 端口（STARTTLS 用 587） | `587` |
| `ENCRYPT` | 加密方式 | `tls` 或 `ssl` |
| `SECRET` | `FROM` 的密码 / 应用专用密码（Gmail 需开 2FA + 应用密码） | `xxxx xxxx xxxx xxxx` |

6 个都填了才会发邮件；缺任何一个（或只缺 `SECRET`）自动跳过，不影响 Pages。

> 注意：亚马逊只允许从「批准的电邮列表」里的地址投递，先去亚马逊后台把 `FROM` 加进去，否则邮件会被拒收。
> 另外老设备注册美区后，国内连 amazon.com 收推送可能不稳定，邮件发出 ≠ 设备一定收到，需实测。

## 换内容源

- 用 Calibre 内置的：往 `recipe_list.txt` 加一行 recipe 名（`ebook-convert --list-recipes` 可查全部）。
- 自定义的：往仓库根目录扔 `xxx.recipe`。
- 中文源直接改 `zhnews.recipe` 里的 `feeds`。

## 改定时

`.github/workflows/calibre-news.yml` 里的 `cron`，UTC 时间。
北京时间减 8 小时，例如北京 07:00 → `0 23 * * *`。
