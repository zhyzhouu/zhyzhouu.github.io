# 主页维护

- `publications/`：每篇论文一个 JSON 文件，包含标题、作者、会议、荣誉、摘要、BibTeX、链接、图片和 TL;DR。
- `publications/order.json`：论文显示顺序；最新论文的 ID 放到最前面。
- `templates/index.html`：个人介绍、页面结构及交互逻辑。
- `templates/thumbnails.json`：原有占位缩略图，一般无需修改。
- `build.py`：静态页面生成程序，仅需 Python 3，无额外依赖。
- `index.html`：生成结果，不要直接编辑。
- `assets/`：个人照片和论文图片。
- `styles.css`、`academic.css`：样式。

## 修改或添加论文

编辑对应的 JSON。新增时复制已有论文文件，修改文件名和 `id`（两者必须一致），再将 ID 加入 `order.json`。

`tldr` 留空字符串则不显示；`distinction` 留空不显示荣誉；`code` 留空保留禁用按钮。

论文文件统一采用“年份后两位 + 会议或期刊 - 简称”的格式，例如 `24CVPR-AMED.json`、`26ECCV-TORS.json`，对应 `id` 为 `24CVPR-AMED`、`26ECCV-TORS`。注意大小写一致。文件名不决定显示顺序，顺序仍由 order.json 控制。

论文图片统一放在 `assets/papers/`，建议与 JSON 同名，例如 `assets/papers/24CVPR-AMED.png`。不要求每篇建立子目录；如果某篇后续有多张图片、视频或海报，可以改用 `assets/papers/24CVPR-AMED/teaser.png`。

在论文 JSON 中填写：

```json
"image": "assets/papers/24CVPR-AMED.png",
"imageAlt": "AMED-Solver sampling trajectories"
```

图片可使用 PNG、JPG、WebP 或 SVG，路径和文件名的大小写需与实际文件一致。图片保持原始比例完整显示，展开摘要或引用不会拉伸图片。image 留空沿用占位图；准备好图片后再填写路径，避免生成时提示文件不存在。

JSON 内容无需 HTML。BibTeX 的换行用 `\n`，字符串内双引号用 `\"`；可参考已有文件。

修改完成后，在项目目录运行：

```sh
python3 build.py
python3 build.py --check
```

然后刷新或直接打开 index.html。无需本地服务器，兼容 GitHub Pages。

## 个人介绍和布局

## 作者主页链接

在根目录的 `coauthors.json` 统一维护姓名与主页的对应关系，例如：

```json
{
  "Zhenyu Zhou": "https://scholar.google.com/citations?user=PR0YPk4AAAAJ",
  "New Author": "https://example.com/",
  "Author Without Homepage": ""
}
```

论文 JSON 的 authors 仍然只填写姓名。姓名会自动匹配链接（忽略大小写和姓名两端空格）；未收录或链接留空的作者显示普通文字。新增、更新链接后运行 `python3 build.py` 即可更新所有论文，无需逐篇修改。Zhenyu Zhou 的姓名继续加粗。

## 页面模板

编辑 templates/index.html，保留 `{{PUBLICATIONS}}`，再重新生成。

## 发布

需要发布时，将数据、模板、生成的 index.html、样式和图片一起提交并推送。生成程序本身不会提交或发布。

本文件替代旧 ACADEMIC-MAINTENANCE.md 中关于直接编辑 index.html 的说明。
