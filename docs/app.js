/* Small progressive enhancements; all content and links work without JavaScript. */
const toggle = document.querySelector('.navbar-toggler');
const navigation = document.getElementById('site-navigation');
toggle?.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') !== 'true';
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? '关闭导航' : '打开导航');
  navigation.classList.toggle('show', open);
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && navigation?.classList.contains('show')) {
    navigation.classList.remove('show');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', '打开导航');
    toggle.focus();
  }
});
for (const button of document.querySelectorAll('[data-filter]')) {
  button.addEventListener('click', () => {
    const year = button.dataset.filter;
    for (const choice of document.querySelectorAll('[data-filter]')) {
      const selected = choice === button;
      choice.setAttribute('aria-pressed', String(selected));
      choice.classList.toggle('active', selected);
    }
    let count = 0;
    for (const paper of document.querySelectorAll('.publication')) {
      paper.hidden = year !== 'all' && paper.dataset.year !== year;
      if (!paper.hidden) count++;
    }
    for (const group of document.querySelectorAll('[data-year-group]')) {
      group.hidden = year !== 'all' && group.dataset.yearGroup !== year;
    }
    document.getElementById('filter-status').textContent = `显示 ${count} 篇论文`;
  });
}
for (const link of document.querySelectorAll('.year-nav a')) {
  link.addEventListener('click', () => {
    document.querySelector('[data-filter="all"]')?.click();
  });
}
for (const button of document.querySelectorAll('.copy-citation')) {
  button.addEventListener('click', async () => {
    const code = button.parentElement.querySelector('code');
    const status = button.parentElement.querySelector('.copy-status');
    try {
      await navigator.clipboard.writeText(code.textContent);
      status.textContent = '已复制';
    } catch {
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = '已选中，请手动复制';
    }
  });
}
