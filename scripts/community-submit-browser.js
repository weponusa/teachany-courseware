/**
 * TeachAny 浏览器端社区提交（零安装）
 * 从 IndexedDB 中的导入课件打包并 POST 到官方 Worker API。
 */
(function (global) {
  'use strict';

  const SUBMIT_API = 'https://teachany-community.pages.dev/api/submit';
  const MAX_PACKAGE_MB = 5;
  const JSZIP_CDN = 'https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js';

  let jszipLoading = null;

  function ensureJSZip() {
    if (typeof JSZip !== 'undefined') return Promise.resolve();
    if (jszipLoading) return jszipLoading;
    jszipLoading = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = JSZIP_CDN;
      script.onload = () => resolve();
      script.onerror = () => reject(new Error('JSZip 加载失败'));
      document.head.appendChild(script);
    });
    return jszipLoading;
  }

  function normalizePath(path) {
    return String(path || '').replace(/^\.?\//, '').replace(/\\/g, '/');
  }

  function guessMimeType(path) {
    const ext = (path.split('.').pop() || '').toLowerCase();
    const map = {
      html: 'text/html',
      css: 'text/css',
      js: 'application/javascript',
      json: 'application/json',
      png: 'image/png',
      jpg: 'image/jpeg',
      jpeg: 'image/jpeg',
      webp: 'image/webp',
      svg: 'image/svg+xml',
      mp3: 'audio/mpeg',
      wav: 'audio/wav',
    };
    return map[ext] || 'application/octet-stream';
  }

  function blobToBase64(blob) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const dataUrl = reader.result || '';
        const comma = String(dataUrl).indexOf(',');
        resolve(comma >= 0 ? String(dataUrl).slice(comma + 1) : '');
      };
      reader.onerror = () => reject(reader.error || new Error('读取课件包失败'));
      reader.readAsDataURL(blob);
    });
  }

  function validateManifest(manifest) {
    const m = manifest || {};
    const missing = ['node_id', 'name', 'subject', 'grade'].filter((k) => {
      const v = m[k];
      return v === undefined || v === null || v === '';
    });
    if (missing.length) {
      throw new Error('manifest.json 缺少必填字段：' + missing.join(', '));
    }
    return m;
  }

  async function packImportedCourse(courseId) {
    const Importer = global.TeachAnyImporter;
    if (!Importer || typeof Importer.getUserCourseRecord !== 'function') {
      throw new Error('课件导入模块未加载，请刷新页面后重试');
    }
    await ensureJSZip();
    const record = await Importer.getUserCourseRecord(courseId);
    if (!record || !record.files || !record.files.length) {
      throw new Error('未找到课件完整数据，可能已被删除');
    }
    const manifest = validateManifest(record.manifest || {});
    const hasIndex = record.files.some((f) => normalizePath(f.path) === 'index.html');
    if (!hasIndex) throw new Error('课件包缺少 index.html');

    const zip = new JSZip();
    for (const file of record.files) {
      const filePath = normalizePath(file.path);
      if (!filePath) continue;
      const blob = file.blob instanceof Blob
        ? file.blob
        : new Blob([file.blob], { type: guessMimeType(filePath) });
      zip.file(filePath, blob);
    }
    if (!record.files.some((f) => normalizePath(f.path) === 'manifest.json')) {
      zip.file('manifest.json', JSON.stringify(manifest, null, 2));
    }

    const zipBlob = await zip.generateAsync({ type: 'blob', compression: 'DEFLATE' });
    const sizeMb = zipBlob.size / 1024 / 1024;
    if (sizeMb > MAX_PACKAGE_MB) {
      throw new Error(`课件包 ${sizeMb.toFixed(1)} MB 超过 ${MAX_PACKAGE_MB} MB 限制，请压缩资源后重试`);
    }
    const packageBase64 = await blobToBase64(zipBlob);
    return { manifest, packageBase64, sizeBytes: zipBlob.size };
  }

  async function submitImportedCourse(courseId, options) {
    options = options || {};
    const onProgress = typeof options.onProgress === 'function' ? options.onProgress : () => {};

    onProgress('packing', '正在打包课件…');
    const { manifest, packageBase64, sizeBytes } = await packImportedCourse(courseId);

    let author = String(options.author || manifest.author || '').trim();
    if (!author) {
      author = String(global.prompt('请输入你的名字（将显示在社区课件作者栏）', '') || '').trim();
    }
    if (!author) throw new Error('已取消：需要填写作者名');

    const message = String(options.message || global.prompt('可选：写一句提交说明', '') || '').trim();

    const payload = {
      node_id: manifest.node_id,
      name: manifest.name,
      subject: manifest.subject,
      grade: manifest.grade,
      author,
      description: manifest.description || manifest.description_zh || '',
      extra: {
        name_en: manifest.name_en || '',
        version: manifest.version || '1.0.0',
        tags: manifest.tags || [],
        teachany_version: manifest.teachany_version || '',
        curriculum: manifest.curriculum || 'cn-national',
        user_message: message,
        submit_source: 'browser-my-page',
      },
      packageBase64,
    };

    onProgress('uploading', '正在提交到社区…');
    const resp = await fetch(SUBMIT_API, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify(payload),
    });

    let data = {};
    try {
      data = await resp.json();
    } catch (_e) {
      data = { ok: false, message: `HTTP ${resp.status}` };
    }

    if (!resp.ok || data.ok === false) {
      throw new Error(data.message || data.error || `提交失败（HTTP ${resp.status}）`);
    }

    onProgress('done', '提交成功');
    return {
      ok: true,
      sizeBytes,
      author,
      data,
      message: '已提交！GitHub Actions 将自动质检并合并，通过后出现在 Gallery「用户共创」筛选中。',
    };
  }

  global.TeachAnyCommunitySubmit = {
    SUBMIT_API,
    MAX_PACKAGE_MB,
    packImportedCourse,
    submitImportedCourse,
  };
})(typeof window !== 'undefined' ? window : globalThis);
