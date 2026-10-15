# 陈辰 · Academic Homepage

陈辰的独立学术主页，采用 [academic-homepage 的 layout2](https://luost.me/academic-homepage/index_layout2) 布局，包含 Home、Publications、Projects、Experience 四个页面。

源码仓库：[ccipad123/chen-chen-homepage](https://github.com/ccipad123/chen-chen-homepage)。网站使用 GitHub Pages 托管，发布后地址为 [陈辰的学术主页](https://ccipad123.github.io/chen-chen-homepage/)。仓库可从任意电脑或编辑器维护，与 ChatGPT 账号相互独立。

## 内容更新

- sources/profile.json：教育日期、研究方向、ORCID
- sources/awards.json：获奖名称与年月
- sources/projects.json：科研项目、编号、角色和结题结果
- sources/publications.json：论文书目
- sources/publication_details.json：论文介绍和 Paper 链接
- sources/corresponding_authors.json：通讯作者标记及依据
- sources/reviewer_service.json：审稿期刊及顺序
- sources/journals.json：期刊图片及明确年份的 JIF
- build.py：页面结构及简介正文
- site_config.json：网站正式网址

修改源文件后运行 python3 build.py，再用 python3 -m http.server 8767 --bind 127.0.0.1 --directory docs 本地预览。

构建仅使用 Python 标准库，无需额外安装。docs/ 是生成后的静态网站，必须与源文件一起提交。发布源设置为 main 分支的 /docs；保留 .nojekyll。提交并推送后触发 GitHub Pages 更新。

## 内容与署名

六篇论文作者顺序和 DOI 基于已核对书目。[Paper] 指向出版方文章页，[DOI] 保留永久链接，BibTeX 可下载。# Corresponding author 表示通讯作者，标记不加入 BibTeX 姓名。科研项目与荣誉按本人确认资料填写。

Energies 图片是 18(17) 的官方期刊封面；封面故事并非本文作者的风速预测论文。封面印刷指标与当前明确年份的 JIF 标签分开保留。

## 模板与资源许可

布局源于 [luost26/academic-homepage](https://github.com/luost26/academic-homepage)，固定上游提交 2fb6806256f4331cf8eb4de5dac6869fc5064d84。保留原始 CSS，改用 Python 生成页面。academic-homepage、Bootstrap、字体和图标许可证位于 docs/licenses/。

校徽、期刊封面和头像仅用于本学术主页展示，相应权利属于各自权利人，不受模板的 MIT 许可覆盖。公开邮箱仅为 chenc2025@stu.pku.edu.cn。
