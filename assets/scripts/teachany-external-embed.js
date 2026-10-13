/* TeachAny 外部模拟内嵌降级
 *
 * 背景：课件里 328 个 <iframe> 内嵌 PhET / GeoGebra 等境外模拟站点。
 * 这些站点在弱网、内网或境外线路抖动时加载不出来，学生会看到一片空白，
 * 误以为课件坏了。
 *
 * 做法：不改课件正文，只给每个外部 iframe 补一条「说明条」——
 *   1) 立刻显示来源与「在新窗口打开」链接（即使 iframe 一直空白，学生也有路可走）
 *   2) iframe 加载成功则把说明条收成一行小字，不干扰正文
 *   3) 超时未加载则明确提示「可能加载较慢」，而不是静默空白
 *
 * 纯增量、无依赖、幂等（重复执行不会叠加）。
 */
(function () {
  'use strict';
  if (window.__teachanyExternalEmbedLoaded) return;
  window.__teachanyExternalEmbedLoaded = true;

  var HOSTS = {
    'phet.colorado.edu': 'PhET 互动模拟',
    'www.geogebra.org': 'GeoGebra 数学工具',
    'geogebra.org': 'GeoGebra 数学工具',
    'basic.smartedu.cn': '国家中小学智慧教育平台',
    'www.bilibili.com': '外部视频'
  };
  var TIMEOUT_MS = 12000;

  function hostOf(url) {
    try { return new URL(url, location.href).hostname.toLowerCase(); } catch (e) { return ''; }
  }
  function labelFor(host) {
    for (var k in HOSTS) { if (host === k || host.endsWith('.' + k)) return HOSTS[k]; }
    return '外部资源';
  }

  function decorate(fr) {
    if (!fr || fr.dataset.teachanyEmbed === '1') return;
    var src = fr.getAttribute('src') || '';
    if (!/^https?:/i.test(src)) return;
    var host = hostOf(src);
    var label = labelFor(host);
    if (label === '外部资源' && host.indexOf('phet') < 0 && host.indexOf('geogebra') < 0 &&
        host.indexOf('smartedu') < 0 && host.indexOf('bilibili') < 0) {
      return; // 不认识的域不动
    }
    fr.dataset.teachanyEmbed = '1';

    var bar = document.createElement('div');
    bar.className = 'ta-embed-bar';
    bar.setAttribute('role', 'note');
    bar.innerHTML =
      '<span class="ta-embed-dot" aria-hidden="true"></span>' +
      '<span class="ta-embed-text">外部资源：' + label + '（需要联网加载）</span>' +
      '<a class="ta-embed-link" href="' + src + '" target="_blank" rel="noopener">在新窗口打开 ↗</a>';

    var hint = document.createElement('span');
    hint.className = 'ta-embed-hint';
    hint.textContent = '加载较慢？可点右侧链接在新窗口打开。';

    var parent = fr.parentNode;
    if (!parent) return;
    parent.insertBefore(bar, fr);

    var done = false;
    fr.addEventListener('load', function () {
      if (done) return;
      done = true;
      bar.classList.add('is-loaded');
      if (hint.parentNode) hint.parentNode.removeChild(hint);
    });

    setTimeout(function () {
      if (done) return;
      bar.classList.add('is-slow');
      bar.insertBefore(hint, bar.querySelector('.ta-embed-link'));
    }, TIMEOUT_MS);
  }

  function scan() {
    var frs = document.querySelectorAll('iframe[src]');
    for (var i = 0; i < frs.length; i++) decorate(frs[i]);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', scan);
  } else {
    scan();
  }
  // 课件是分页式，可能有页面后插入的 iframe
  document.addEventListener('click', function () { setTimeout(scan, 300); }, true);
  window.TeachAnyExternalEmbed = { scan: scan };
})();
