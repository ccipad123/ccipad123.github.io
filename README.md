# 陈辰 · Academic Homepage

陈辰的独立学术主页，采用 [academic-homepage 的 layout2](https://luost.me/academic-homepage/index_layout2) 布局，包含 Home、Publications、Projects、Experience 四个页面。

源码仓库：[ccipad123/chen-chen-homepage](https://github.com/ccipad123/chen-chen-homepage)。网站使用 GitHub Pages 托管，正式地址为 [陈辰的学术主页](https://ccipad123.github.io/)。原来的 `/chen-chen-homepage/` 地址继续可用。仓库可从任意电脑或编辑器维护，与 ChatGPT 账号相互独立。

## 内容更新

- sources/profile.json：教育日期、研究方向、关键词介绍链接、导师官方主页、志愿服务与证书链接、蓝信封访谈、ORCID
- sources/awards.json：获奖名称与年月
- sources/projects.json：科研项目、编号、角色和结题结果
- sources/publications.json：论文书目、稳定的 BibTeX 引用键及出版社
- sources/hybrid_loss_final_20261019.json：混合截断损失论文正式 PDF 与 2027/334/134683 书目核对
- sources/citation_audit_20261018.json：六篇论文的 Google Scholar 详情、Crossref 与原 PDF 核对及差异处理
- sources/publication_details.json：论文介绍、出版方链接、PDF 文件与校验信息
- sources/corresponding_authors.json：通讯作者标记及依据
- sources/reviewer_service.json：审稿期刊及顺序
- sources/journals.json：期刊图片及明确年份的 JIF
- build.py：页面结构及简介正文
- docs/style.css：手工维护的排版覆盖层与灰色链接主题；build.py 不覆盖此文件
- docs/app.js：导航、年份筛选、引用复制与证书弹窗；build.py 不覆盖此文件
- docs/assets/papers/：用户提供的七篇论文 PDF 原件；[Paper] 直接打开对应文件
- docs/assets/bibtex/：build.py 按书目生成的单篇 .bib 引用，首页和论文页均可下载
- docs/assets/certificates/：用户授权点击展示的三张原始证书
- docs/assets/portrait.png：现有头像，同时用于浏览器标签图标和 apple-touch-icon
- site_config.json：网站正式网址

修改源文件后运行 python3 build.py，再用 python3 -m http.server 8767 --bind 127.0.0.1 --directory docs 本地预览。

构建仅使用 Python 标准库，无需额外安装。docs/ 是生成后的静态网站，必须与源文件一起提交；保留 .nojekyll。

## 发布

两处使用同一份提交和 `/docs` 发布目录：

- 源码仓库 `ccipad123/chen-chen-homepage`：`main` 分支，兼容原来的长网址。
- 根站仓库 `ccipad123/ccipad123.github.io`：`academic-homepage` 分支，正式短网址 `https://ccipad123.github.io/`。原 `master` 分支保存旧主页源码，不覆盖。

本地 `origin` 指向源码仓库，`root-site` 指向根站仓库。修改、构建、验证并提交后，将同一提交推送到两处：

```sh
git push root-site HEAD:academic-homepage
git push origin main
```

新电脑若尚未配置根站 remote，先运行 `git remote add root-site https://github.com/ccipad123/ccipad123.github.io.git`。发布后核对两站 Pages build 的提交和实际公开页面。根站 Pages source 应为 `academic-homepage` / `/docs`；如需恢复旧主页，可切回原 `master` / `/`，源码仍保留。

## 旧版主页归档

[旧版主页](https://ccipad123.github.io/old/) 位于 `docs/old/`，保留原来的「無限進步」、Research、Awards、Links 及其他已有页面。它来自根站仓库 `master` 的固定提交 `664a95180e229918dc39ccd5c64dfad6f9047f2a`；旧版文字与历史联系方式仅保留在归档内。

构建使用 GitHub Pages 现有 Jekyll 运行环境，工作流在 `sources/legacy_homepage_build.yml`，构建与导入来源在 `sources/legacy_site.json`。该工作流只生成 artifact，不部署根站。下载对应 artifact ZIP 后，运行 `python3 import_legacy.py /path/to/archive.zip` 导入；导入器将同站链接/资源迁移到 `/old/`，使用已有头像替代原模板缺失的图标。已有 `docs/old` 时须先归档，导入器不会覆盖它。

日常 `python3 build.py` 不重建或删除 `docs/old/`；静态归档随其他文件同步发布到两个仓库。根站的原 `master` 分支继续保留。

## 内容与署名

七篇论文使用已核对的作者顺序和 DOI。混合截断损失论文已更新为用户提供的 28 页正式排版 PDF，书目为 Expert Systems with Applications 334 (2027) 134683，在线日期仍为 12 Oct. 2026。最新依据见 sources/hybrid_loss_final_20261019.json；2026-10-16 与 2026-10-18 的核对文件保留为历史记录。为兼容既有引用，保留稳定键 yang2026robust，year 字段为 2027，volume 为 334。该篇 Paper 链接使用 pdf_version 刷新缓存。[Paper] 直接打开用户提供的论文 PDF 原件（首页、完整论文页及 News 均一致）；[DOI] 保留出版方永久链接。每篇 DOI 旁的 [BibTeX ↓] 下载单篇 .bib，首页精选和完整论文页均有可展开的“查看引用”及复制按钮，完整论文页另有全部 BibTeX 下载。引用格式参考用户提供的 Google Scholar 示例：如 chen2025multi，作者按“姓, 名”并以 and 分隔，补充 publisher；保留 DOI、缺卷号论文的在线日期，以及 L₀/₁ 的 LaTeX 数学写法。2026-10-18 已逐篇打开本人 Google Scholar 的另外六篇详情核对作者顺序、年份、卷期和文章号，记录见 sources/citation_audit_20261018.json。Mathematics 补充期号 4；深度多视图论文 Scholar 仍为 2025 在线版无卷号，正式期刊版沿用 2026/298/129406；混合截断损失 Scholar 仍是 arXiv 预印本，当时网站沿用 ESWA 2026/134683且暂不填卷号；该篇现已由上述2026-10-19正式版记录更新。已核对的是字段，不声称下载过六篇 Scholar 原始 BibTeX 导出。单篇、全部及页面内引用共用生成函数，下载 URL 带版本号避免旧缓存。PDF 文件、页数、SHA256 与原始文件名记录于 sources/publication_details.json；仅复制原件，不由 PDF 生成或声称提供论文 LaTeX 全文源码。# Corresponding author 表示通讯作者，标记不加入 BibTeX 姓名。科研项目与荣誉按本人确认资料填写。

Energies 图片是 18(17) 的官方期刊封面；封面故事并非本文作者的风速预测论文。封面印刷指标与当前明确年份的 JIF 标签分开保留。

## 模板与资源许可

布局源于 [luost26/academic-homepage](https://github.com/luost26/academic-homepage)，固定上游提交 2fb6806256f4331cf8eb4de5dac6869fc5064d84。保留原始 CSS，改用 Python 生成页面。academic-homepage、Bootstrap、字体和图标许可证位于 docs/licenses/。

校徽、期刊封面和头像仅用于本学术主页展示，相应权利属于各自权利人，不受模板的 MIT 许可覆盖。公开邮箱仅为 chenc2025@stu.pku.edu.cn。
