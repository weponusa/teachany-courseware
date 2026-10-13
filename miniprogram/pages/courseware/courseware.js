const COURSEWARE_BASE = 'https://www.teachany.cn/community/'

function sanitizeId(id) {
  return String(id || '').trim().replace(/[^a-zA-Z0-9_-]/g, '')
}

Page({
  data: {
    src: ''
  },
  onLoad(query) {
    const id = sanitizeId(query.id || query.courseId || '')
    const rawUrl = query.url ? decodeURIComponent(query.url) : ''
    let src = ''
    if (rawUrl && /^https:\/\/weponusa\.github\.io\/teachany-courseware\//.test(rawUrl)) {
      src = rawUrl
    } else if (id) {
      src = `${COURSEWARE_BASE}${id}/index.html`
    } else {
      src = `${COURSEWARE_BASE}hist-m-renaissance/index.html`
    }
    if (!src.includes('#wechat_redirect')) src += '#wechat_redirect'
    this.setData({ src })
  },
  onWebViewLoad(e) {
    console.log('[TeachAny web-view load]', e.detail)
  },
  onError(e) {
    console.error('[TeachAny web-view error]', e.detail)
    wx.showToast({ title: '课件加载失败', icon: 'none' })
  }
})
