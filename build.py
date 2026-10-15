"""Render Chen Chen's academic-homepage adaptation using Python's standard library.

Layout and original global.css: luost26/academic-homepage (MIT, see licenses).
Publications are generated from the retained, Crossref-verified source records.
No build-time network access or third-party Python packages are required.
"""
from pathlib import Path
from datetime import date
import html
import json

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'docs'
SITE = json.loads((ROOT / 'site_config.json').read_text())
ORIGIN = SITE['site_url'].rstrip('/')
from urllib.parse import urlsplit
BASE_PATH = urlsplit(ORIGIN).path.rstrip('/') + '/'
SCHOLAR = 'https://scholar.google.com/citations?user=6bYDKs4AAAAJ&hl=zh-CN'
ORCID = 'https://orcid.org/0009-0006-6694-580X'
REVISION = '20261016-volunteer-service'
PROFILE = json.loads((ROOT / 'sources/profile.json').read_text())
PUBLICATIONS = json.loads((ROOT / 'sources/publications.json').read_text())
PUBLICATIONS.sort(key=lambda p: tuple(p['published']['date-parts'][0]), reverse=True)
ESC = html.escape

JOURNALS = json.loads((ROOT / 'sources/journals.json').read_text())
PUBLICATION_DETAILS = json.loads((ROOT / 'sources/publication_details.json').read_text())
CORRESPONDING = json.loads((ROOT / 'sources/corresponding_authors.json').read_text())['papers']
SUMMARIES = {doi: item['summary'] for doi, item in PUBLICATION_DETAILS.items()}

AWARDS = [(item['display_date'], item['title'], ' · '.join(item[key] for key in ('level', 'category') if item.get(key))) for item in json.loads((ROOT / 'sources/awards.json').read_text())]
PROJECTS = json.loads((ROOT / 'sources/projects.json').read_text())['projects']
TEACHING = [
    ('Feb. 2025 – Jul. 2025', '概率论与数理统计 B'),
    ('Dec. 2024 – Jan. 2025', '统计软件（双语）'),
    ('Sep. 2024 – Jan. 2025', '统计计算语言'),
]
REVIEWER_SERVICE = json.loads((ROOT / 'sources/reviewer_service.json').read_text())
REVIEWER_JOURNALS = REVIEWER_SERVICE['journals']
REVIEWER_PUBLISHER_RANK = {name: rank for rank, name in enumerate(REVIEWER_SERVICE['publisher_order'])}

def math_text(text, base=''):
    formula = f'<img class="inline-math" src="{base}assets/math/l01.svg" alt="L₀/₁" data-tex="L_{{0/1}}">'
    return ESC(text).replace('L0/1', formula)



def plain_title(p):
    if p['doi'] == '10.1016/j.inffus.2024.102733':
        return 'Multi-view support vector machine classifier via L0/1 soft-margin loss with structural information'
    return p['title']



def bibtex(p):
    year = p['published']['date-parts'][0][0]
    title = plain_title(p).replace('L0/1', r'{$L_{0/1}$}')
    return ('@article{' + p['authors'][0].split()[-1] + str(year) + '_' + p['article'] + ',\n'
            + '\n'.join('  ' + key + ' = {' + value + '},' for key, value in [
                ('title', title), ('author', ' and '.join(p['authors'])),
                ('journal', p['journal']), ('year', str(year)),
                *([('volume', p['volume'])] if p.get('volume') else []),
                *([('number', p['issue'])] if p.get('issue') else []),
                ('pages', p['article']), ('doi', p['doi']),
                *([('note', 'Available online ' + p['published_online'])]
                  if p.get('published_online') and not p.get('volume') else [])]) + '\n}')



def external(url, label, cls=''):
    return f'<a class="{cls}" href="{ESC(url, quote=True)}" target="_blank" rel="noopener noreferrer">{label}</a>'





def icon(name):
    return f'<i class="{name}" aria-hidden="true"></i>'


def bilingual_term(chinese, english, url=None):
    translation = external(url, ESC(english)) if url else ESC(english)
    return f'<span class="research-term"><strong>{ESC(chinese)}</strong><span class="term-translation">（{translation}）</span></span>'


def research_term(name):
    term = PROFILE['keyword_resources'][name]
    return bilingual_term(term['zh'], name, term['url'])


def advisor_link():
    advisor = PROFILE['advisor']
    return external(advisor['homepage'], ESC(advisor['name'])) + ESC(advisor['title'])


def reviewer_service():
    rows = []
    for journal in sorted(REVIEWER_JOURNALS, key=lambda j: (REVIEWER_PUBLISHER_RANK.get(j['publisher'], len(REVIEWER_PUBLISHER_RANK)), j['name'].casefold())):
        metric = external(journal['metric_source'], f'{journal["jif"]:.1f}', 'review-metric') if journal['jif'] is not None else '<span class="text-muted" aria-label="尚未公布 2025 JIF">—</span>'
        rows.append(f'<tr><th scope="row" class="review-name">{external(journal["url"], ESC(journal["name"]))}</th><td class="review-publisher" data-label="出版方">{ESC(journal["publisher"])}</td><td class="review-impact" data-label="2025 JIF">{metric}</td></tr>')
    return f'''<section class="my-3 bg-white shadow-sm rounded-xl" id="peer-review">
    <h2 class="h6 p-3 mb-0 border-bottom">{icon('fas fa-pen-to-square')} Peer Review <small class="text-muted">期刊审稿</small></h2>
    <div class="px-3 pb-2"><table class="reviewer-table" aria-label="审稿期刊与期刊信息"><thead><tr><th scope="col">期刊</th><th scope="col">出版方</th><th scope="col">2025 JIF</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>'''


def paper(p, full=False):
    base = '../' if full else ''
    year = p['published']['date-parts'][0][0]
    journal = JOURNALS[p['journal']]
    title = math_text(plain_title(p), base)
    correspondents = CORRESPONDING[p['doi']]['authors']
    names = ', '.join(('<strong>Chen Chen</strong>' if n == 'Chen Chen' else ESC(n)) + ('<sup class="corresponding-marker" title="Corresponding author" aria-label="Corresponding author">#</sup>' if n in correspondents else '') for n in p['authors'])
    cover_path = base + 'assets/journals/' + journal['cover']
    cover_background = BASE_PATH + 'assets/journals/' + journal['cover']
    cover_alt = journal.get('cover_alt', p['journal'] + ' 期刊封面')
    cover = f'<img class="journal-cover-image w-100 rounded-sm" src="{cover_path}" width="{journal["cover_width"]}" height="{journal["cover_height"]}" alt="{ESC(cover_alt)}" loading="lazy" decoding="async">'
    metric = external(journal['source_url'], f'{journal["jif_year"]} JIF · {journal["jif"]:.1f}', 'journal-metric')
    volume_issue = ESC(p.get('volume', '')) + (f'({ESC(p["issue"])})' if p.get('issue') else '')
    bibliographic_line = f'{year}, ' + (volume_issue + ': ' if volume_issue else '') + ESC(p['article'])
    if p.get('published_online') and not p.get('volume'):
        online = date.fromisoformat(p['published_online'])
        month = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.'][online.month - 1]
        bibliographic_line += f' · Available online {online.day} {month} {online.year}'
    citation = ''
    if full:
        citation = f'<details class="bibtex"><summary>BibTeX</summary><div class="citation-box"><pre><code>{ESC(bibtex(p))}</code></pre><button class="btn btn-sm btn-outline-secondary copy-citation" type="button">复制引用</button><span class="copy-status small ml-2" role="status"></span></div></details>'
    return f'''<article class="publication row no-gutters border-bottom" data-year="{year}" style="--paper-cover:url('{cover_background}')">
    <div class="col-md-3 col-xl-2 p-md-3 d-none d-md-block journal-cover-column">{external(journal.get('cover_url', journal['journal_url']), cover, 'journal-cover-link')}</div>
    <div class="col-md-9 col-xl-10 p-3 pl-md-0 publication-body">
    <h3 class="h5 mt-0 mb-1 font-weight-normal paper-title">{external('https://doi.org/'+p['doi'], title, 'text-body')}</h3>
    <p class="mt-0 mb-0 small authors">{names}</p>
    <p class="mt-0 mb-0 small journal-line"><i>{ESC(p['journal'])}</i> {bibliographic_line} {metric}</p>
    <p class="mt-0 mb-0 small text-muted paper-summary">{math_text(SUMMARIES[p['doi']], base)}</p>
    <div class="small paper-links">{external(PUBLICATION_DETAILS[p['doi']]['paper_url'], '[Paper]', 'paper-link')}{external('https://doi.org/'+p['doi'], '[DOI]')}{citation}</div></div></article>'''


def profile_card():
    return f'''<div class="row"><div class="col"><section class="card border-0 shadow-sm bg-white profile-card" aria-labelledby="profile-name"><div class="card-body p-5">
    <div class="row"><div class="col">
    <div class="figure float-right ml-4 mb-4 d-none d-md-block"><img src="assets/portrait.png" class="figure-img img-fluid img-thumbnail profile-portrait" width="603" height="603" alt="陈辰的个人主页头像"></div>
    <div class="d-flex"><h1 class="h1 font-weight-normal profile-name" id="profile-name">陈辰 <small>Chen Chen</small></h1><div class="ml-auto d-md-none pl-2"><a href="assets/portrait.png" target="_blank" rel="noopener"><img src="assets/portrait.png" class="rounded-circle profile-portrait-mobile" width="48" height="48" alt="陈辰的个人主页头像"></a></div></div>
    <div class="text-profile-position">直博生 · PhD Student<br><img src="assets/universities/pku.png" alt="北京大学校徽" class="inline-badge">北京大学第一临床医学院</div>
    <div class="text-profile-bio mt-3"><p>我目前在北京大学第一临床医学院攻读博士，导师为{advisor_link()}。主要从事{bilingual_term('空间转录组', 'Spatial Transcriptomics')}<strong>算法设计</strong>，研究兴趣涉及{research_term('Computational Pathology')}与{research_term('Bioinformatics')}。</p>
    <p>本科就读于北京林业大学数学与应用数学专业，研究主要围绕{research_term('Machine Learning')}、{research_term('Pattern Recognition')}与{research_term('Optimization')}展开。</p>
    <p>我的研究聚焦于{research_term('Multi-view Learning')}领域，主要涉及{research_term('Support Vector Machines')}和{research_term('Safe Screening')}，关注不同视图的共有信息与互补信息，以及数据结构、损失函数对分类模型的影响；相关工作也涉及<strong>非凸优化</strong>与<strong>工作集求解</strong>。论文发表于 <strong>Information Fusion</strong>、<strong>Expert Systems with Applications</strong> 等期刊。</p>
    <p>欢迎交流！</p></div>
    </div></div><hr><div class="row"><div class="col contact-links">
    <a class="pr-3" href="mailto:chenc2025@stu.pku.edu.cn">{icon('fas fa-at')} <span class="email-text">chenc2025@stu.pku.edu.cn</span></a>
    {external(SCHOLAR, icon('fab fa-google-scholar')+' Google Scholar','pr-3 no-break')}
    {external(ORCID, icon('fab fa-orcid')+' ORCID','pr-3 no-break')}
    </div></div></div></section></div></div>'''


def education_period(key):
    months = ('Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.')
    def month_year(value):
        year, month = value.split('-')
        return f'{months[int(month)-1]} {year}'
    period = PROFILE['education'][key]
    return month_year(period['start']) + ' – ' + (month_year(period['end']) if period['end'] else 'present')


def education(base=''):
    return f'''<ul class="list-unstyled mb-1 education-list">
    <li class="media mb-2"><img src="{base}assets/universities/pku.png" width="18" height="18" alt="北京大学校徽" class="mr-1 mt-1 education-emblem"><div class="media-body"><div>北京大学</div><div class="small">第一临床医学院</div><div class="small d-flex"><div>直博生 · PhD Student</div><div class="mt-auto ml-auto no-break pl-2"><em>{education_period('pku')}</em></div></div></div></li>
    <li class="media mb-1"><img src="{base}assets/universities/bjfu.png" width="18" height="18" alt="北京林业大学校徽" class="mr-1 mt-1 education-emblem"><div class="media-body"><div>北京林业大学</div><div class="small d-flex"><div>数学与应用数学</div><div class="mt-auto ml-auto no-break pl-2"><em>{education_period('bjfu')}</em></div></div></div></li></ul>'''


def dated_list(items):
    rows = []
    for item in items:
        date, text = item[:2]
        note = f'<small class="d-block text-muted">{ESC(item[2])}</small>' if len(item) > 2 and item[2] else ''
        rows.append(f'<li><div class="d-flex"><div>{ESC(text)}{note}</div><div class="ml-auto mt-auto no-break pl-3"><em>{ESC(date)}</em></div></div></li>')
    return '<ul class="list small pl-3 mb-1 dated-list">' + ''.join(rows) + '</ul>'


def education_honors(base=''):
    return f'''<div class="row mt-3"><div class="col"><section class="card border-0 shadow-sm bg-white"><div class="card-body p-4"><div class="row education-honors">
    <div class="col-lg-6"><div class="mx-2 my-1"><h2 class="h6">Education <small class="text-muted">教育经历</small></h2>{education(base)}</div></div>
    <div class="col-lg-6" id="honors"><div class="mx-2 my-1"><h2 class="h6">Honors &amp; Awards <small class="text-muted">获奖与荣誉</small></h2>{dated_list(AWARDS)}</div></div>
    </div></div></section></div></div>'''


def news_card():
    return f'''<section class="my-3 bg-white shadow-sm rounded-xl" id="news"><h2 class="h6 p-3 mb-0 border-bottom">{icon('fas fa-rss')} News</h2><div class="px-3 pb-1 small">
    <div class="media py-1"><div class="mr-3 text-muted my-1">2026</div><div class="media-body"><div class="my-1 d-flex"><div>论文在线发表于 <i>Expert Systems with Applications</i>，研究基于混合截断损失的鲁棒稀疏支持向量机。 {external('https://doi.org/10.1016/j.eswa.2026.134683','[Paper]')}</div><div class="ml-auto mt-auto text-muted no-break pl-3"><i>Oct.</i></div></div>
    <div class="my-1 d-flex"><div>合作论文发表于 <i>Expert Systems with Applications</i>，研究跨输出知识迁移的深度多视图学习。 {external('https://doi.org/10.1016/j.eswa.2025.129406','[Paper]')}</div><div class="ml-auto mt-auto text-muted no-break pl-3"><i>Mar.</i></div></div></div></div>
    <div class="media py-1 border-top"><div class="mr-3 text-muted my-1">2025</div><div class="media-body"><div class="my-1 d-flex"><div>合作论文发表于 <i>Energies</i>，研究融合湍流强度与多种气象特征的 Transformer 风速预测模型。 {external('https://doi.org/10.3390/en18174571','[Paper]')}</div><div class="ml-auto mt-auto text-muted no-break pl-3"><i>Aug.</i></div></div>
    <div class="my-1 d-flex"><div>合作论文发表于 <i>Computers and Electronics in Agriculture</i>，研究森林生物量碳储量估计。 {external('https://doi.org/10.1016/j.compag.2025.110020','[Paper]')}</div><div class="ml-auto mt-auto text-muted no-break pl-3"><i>May</i></div></div></div></div></div></section>'''


def home():
    selected = [next(p for p in PUBLICATIONS if p['doi'] == doi) for doi in ['10.1016/j.eswa.2026.134683','10.1016/j.inffus.2024.102733','10.1016/j.eswa.2024.125814','10.1016/j.eswa.2025.129406','10.1016/j.compag.2025.110020']]
    return profile_card() + education_honors() + news_card() + f'''<section class="my-3 p-0 bg-white shadow-sm rounded-xl" aria-labelledby="selected-title">
    <h2 class="h6 border-bottom p-3 mb-0" id="selected-title">{icon('fas fa-star')} Selected Publications <a href="publications/index.html">(view all {icon('fas fa-angle-double-right')})</a></h2>
    <p class="small text-muted px-3 pt-2 mb-2 correspondence-key"># Corresponding author</p>{''.join(paper(p) for p in selected)}<div class="h6 d-block p-3 mt-0 mb-0 text-right"><a href="publications/index.html">All publications {icon('fas fa-angle-double-right')}</a></div></section>''' + reviewer_service()


def publications():
    years = sorted({p['published']['date-parts'][0][0] for p in PUBLICATIONS}, reverse=True)
    groups = ''.join(f'<section class="publication-year" data-year-group="{year}"><h2 class="pt-4" id="year-{year}">{year}</h2><div class="my-0 p-0 bg-white shadow-sm rounded-xl">' + ''.join(paper(p, True) for p in PUBLICATIONS if p['published']['date-parts'][0][0] == year) + '</div></section>' for year in years)
    return f'''<h1 class="sr-only">Publications · 学术论文</h1><div class="row"><div class="col-12 col-lg-10">
    <div class="publication-tools small"><div class="btn-group btn-group-sm" role="group" aria-label="按论文年份筛选"><button class="btn btn-outline-primary active" type="button" data-filter="all" aria-pressed="true">全部</button>{''.join(f'<button class="btn btn-outline-primary" type="button" data-filter="{year}" aria-pressed="false">{year}</button>' for year in years)}</div><span class="text-muted" id="filter-status" role="status">显示 {len(PUBLICATIONS)} 篇论文</span><a href="../assets/chen-chen-publications.bib" download>下载全部 BibTeX ↓</a></div><p class="small text-muted mt-3 mb-0 correspondence-key"># Corresponding author</p>{groups}
    <p class="small mt-3 mb-0">{external(SCHOLAR,'Google Scholar →')}</p></div><div class="col-2 d-none d-lg-block"><nav class="nav nav-pills flex-column sticky-top year-nav" aria-label="论文年份">{''.join(f'<a class="nav-link d-block" href="#year-{year}">{year}</a>' for year in years)}</nav></div></div>'''


def experience():
    volunteering = PROFILE['volunteering']
    service_items = [(item['display_date'], item['title']) for item in volunteering['events']]
    service_items.append(('Sep. 2023 – Aug. 2024', '本科新生学业辅导员'))
    return f'''<h1 class="h3 font-weight-normal mb-3">Experience <small class="text-muted">学习与经历</small></h1>{education_honors('../')}
    <section class="my-3 bg-white shadow-sm rounded-xl" id="research"><h2 class="h6 p-3 mb-0 border-bottom">Research <small class="text-muted">研究经历</small></h2><div class="p-4 research-content">
    <section class="research-section" aria-labelledby="phd-research"><h3 class="h6" id="phd-research">博士阶段 · 空间转录组算法设计</h3><p>目前在北京大学第一临床医学院攻读博士，导师为{advisor_link()}。主要从事{bilingual_term('空间转录组', 'Spatial Transcriptomics')}算法设计，研究兴趣涉及{research_term('Computational Pathology')}与{research_term('Bioinformatics')}。</p><p>空间转录组数据同时记录分子表达和组织中的空间位置；我关注如何将这两类信息共同纳入模型，分析表达差异及其空间分布。</p></section>
    <section class="research-section" aria-labelledby="undergraduate-research"><h3 class="h6" id="undergraduate-research">本科阶段 · 机器学习、模式识别与最优化理论</h3><p class="small text-muted research-subtitle">Machine Learning · Pattern Recognition · Optimization</p><p>{research_term('Multi-view Learning')}关注从不同角度描述同一样本的数据，各视图既有共有信息，也有各自的特征。我的相关工作围绕如何共同利用这些信息展开：在{research_term('Support Vector Machines')}中引入结构信息和不同损失函数，通过视图权重、结构正则项或跨层知识迁移构造分类模型。</p><p>除了模型构造，相关研究也讨论优化问题的求解。在非凸损失模型中分析最优解与平稳点的关系，结合工作集策略求解；在孪生支持向量机中推导安全筛选规则，减少参数选择时需要处理的样本。具体方法与实验见<a href="../publications/index.html">论文列表</a>。</p></section>
    <section class="research-section" aria-labelledby="collaborative-research"><h3 class="h6" id="collaborative-research">合作研究 · 预测建模与统计测量</h3><p>在森林生物量碳储量估计中，参与基于局部样本信息的加权回归研究，将 K 近邻结构与参数优化用于碳储量预测。在风速预测工作中，结合多尺度湍流特征、气象序列独立建模与 Transformer 融合，分析不同时间尺度及气象变量所包含的信息。</p><p>另一项合作研究面向多维自适应测评，在多维项目反应理论框架下进行即时组卷，比较不同组卷策略的能力估计精度、题目曝光和实施灵活性。上述工作分别发表于 <i>Computers and Electronics in Agriculture</i>、<i>Energies</i> 与 <i>Mathematics</i>。</p></section>
    <p class="mb-0"><a href="../projects/index.html">Projects · 科研项目 {icon('fas fa-angle-double-right')}</a></p></div></section>
    {reviewer_service()}
    <section class="my-3 bg-white shadow-sm rounded-xl"><h2 class="h6 p-3 mb-0 border-bottom">Teaching <small class="text-muted">助教经历</small></h2><div class="p-4">{dated_list(TEACHING)}</div></section>
    <section class="my-3 bg-white shadow-sm rounded-xl" id="service"><h2 class="h6 p-3 mb-0 border-bottom">Service <small class="text-muted">志愿与服务</small></h2><div class="p-4"><p class="mb-3">{ESC(volunteering['recognition']['summary'])}</p>{dated_list(service_items)}<p class="mt-3">曾参与蓝信封通讯陪伴、临终关怀与国家动物博物馆等志愿服务。</p><ul class="pl-3 mb-0">{''.join('<li>' + ESC(item['activity']) + '<div class="small mt-1">' + external(item['url'], ESC(item['title'])) + '</div></li>' for item in PROFILE['outreach'])}</ul></div></section>
    <section class="my-3 bg-white shadow-sm rounded-xl" id="contact"><h2 class="h6 p-3 mb-0 border-bottom">Contact <small class="text-muted">联系</small></h2><div class="p-4"><p class="mb-2">欢迎就研究与学习交流。</p><p class="mb-2"><a href="mailto:chenc2025@stu.pku.edu.cn">chenc2025@stu.pku.edu.cn</a></p><p class="small mb-0">{external(ORCID,'ORCID · 0009-0006-6694-580X')}</p></div></section>'''


def projects():
    cards = []
    for item in PROJECTS:
        cards.append(f'''<article class="my-3 bg-white shadow-sm rounded-xl project-card"><div class="p-4">
        <div class="d-flex flex-wrap align-items-baseline mb-3"><h2 class="h5 font-weight-normal mb-2 mr-3 project-title">{ESC(item['title'])}</h2><em class="ml-auto text-muted no-break small">{ESC(item['period'])}</em></div>
        <dl class="row small mb-0"><dt class="col-sm-2 font-weight-normal text-muted">项目类别</dt><dd class="col-sm-10">{ESC(item['program'])}</dd><dt class="col-sm-2 font-weight-normal text-muted">项目编号</dt><dd class="col-sm-10">{ESC(item['id'])}</dd><dt class="col-sm-2 font-weight-normal text-muted">项目职责</dt><dd class="col-sm-10">{ESC(item['role'])}</dd><dt class="col-sm-2 font-weight-normal text-muted">结题结果</dt><dd class="col-sm-10 mb-0">{ESC(item['outcome'])}</dd></dl></div></article>''')
    return '<h1 class="h3 font-weight-normal mb-3">Projects <small class="text-muted">科研项目</small></h1>' + ''.join(cards)


def layout(page, body, base=''):
    titles = {'home':'Homepage','publications':'Publications','projects':'Projects','experience':'Experience','404':'页面未找到'}
    route = '' if page in ('home','404') else page+'/'
    if page == '404':
        base = BASE_PATH
    nav = ''.join(f'<li class="nav-item"><a class="nav-link{" active" if page==key else ""}" '+('aria-current="page" ' if page==key else '')+f'href="{base}{path}">{label}</a></li>' for key,path,label in [('home','index.html','Home'),('publications','publications/index.html','Publications'),('projects','projects/index.html','Projects'),('experience','experience/index.html','Experience')])
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,shrink-to-fit=no">
    <title>陈辰 Chen Chen · {titles[page]}</title><meta name="site-revision" content="{REVISION}"><meta name="description" content="陈辰的个人学术主页。北京大学第一临床医学院直博生，从事空间转录组算法设计，关注计算病理学与生物信息学。论文、科研项目、教育经历、获奖与教学。"><link rel="canonical" href="{ORIGIN}/{route}">
    <meta property="og:title" content="陈辰 Chen Chen · {titles[page]}"><meta property="og:description" content="个人简介、学术论文与学习经历。"><meta property="og:type" content="website"><meta property="og:url" content="{ORIGIN}/{route}"><meta name="theme-color" content="#f8f9fa">
    <link rel="icon" href="{base}assets/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="{base}assets/vendor/bootstrap.min.css"><link rel="stylesheet" href="{base}assets/vendor/fontawesome/css/all.min.css"><link rel="stylesheet" href="{base}assets/vendor/academic-homepage.css"><link rel="stylesheet" href="{base}style.css?v={REVISION}"><script src="{base}app.js" defer></script></head>
    <body class="bg-light d-flex flex-column min-vh-100"><a class="skip-link" href="#main">跳转到正文</a><nav class="navbar navbar-expand-sm navbar-light fixed-top mb-5 shadow-sm" aria-label="主导航"><div class="container-lg"><a class="navbar-brand" href="{base}index.html"><strong>陈辰</strong></a><button class="navbar-toggler" type="button" aria-controls="site-navigation" aria-expanded="false" aria-label="打开导航">{icon('fas fa-map')} Menu</button><div class="collapse navbar-collapse" id="site-navigation"><ul class="navbar-nav ml-auto">{nav}</ul></div></div></nav>
    <main class="flex-grow-1 flex-shrink-0 container-lg" id="main" tabindex="-1">{body}</main>
    <footer class="footer flex-shrink-0 border-top py-2 mt-5 bg-white small"><div class="container-lg"><div class="row my-3"><div class="col-6 text-muted"><i>Last updated: Oct. 2026</i><span class="d-block small">© 2026 陈辰</span></div><div class="col-6 text-right">{external('https://github.com/luost26/academic-homepage',icon('fas fa-pencil-ruler')+' academic-homepage')}</div></div></div></footer></body></html>'''


def main():
    (DIST / 'publications').mkdir(exist_ok=True)
    (DIST / 'experience').mkdir(exist_ok=True)
    (DIST / 'projects').mkdir(exist_ok=True)
    (DIST / 'index.html').write_text(layout('home', home()), encoding='utf-8')
    (DIST / 'publications/index.html').write_text(layout('publications', publications(), '../'), encoding='utf-8')
    (DIST / 'experience/index.html').write_text(layout('experience', experience(), '../'), encoding='utf-8')
    (DIST / 'projects/index.html').write_text(layout('projects', projects(), '../'), encoding='utf-8')
    (DIST / '404.html').write_text(layout('404', f'<section class="card border-0 shadow-sm"><div class="card-body p-4"><h1 class="h3">页面未找到</h1><p>这个地址可能已更改。</p><a href="{BASE_PATH}">返回首页 →</a></div></section>', '/'), encoding='utf-8')
    (DIST / 'assets/chen-chen-publications.bib').write_text('\n\n'.join(bibtex(p) for p in PUBLICATIONS) + '\n', encoding='utf-8')
    (DIST / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n')
    (DIST / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{ORIGIN}/{route}</loc></url>' for route in ['', 'publications/', 'projects/', 'experience/']) + '</urlset>\n')
    print(f'Built 4 pages, 404, {len(PUBLICATIONS)} verified citations, robots and sitemap.')


if __name__ == '__main__':
    main()
