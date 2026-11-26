/**
 * TeachAny — 开源知识图谱/题库增强层（旁挂，可静默降级）
 *
 * 数据来源与授权见 data/external/open-kg/NOTICE.md
 * 红线：不修改权威图谱、不写 curriculum_points、关系仅作候选。
 */
(function (global) {
  'use strict';

  var BASE = './data/external/open-kg/';
  var VERSION = '?v=20261126';
  var api = {
    ready: false,
    topics: {},
    questions: [],
    alignment: [],
    report: null,
    _byKp: null,
    _byTopic: null,

    load: function () {
      if (this._promise) return this._promise;
      var self = this;
      this._promise = Promise.all([
        fetch(BASE + 'topics.json' + VERSION).then(function (r) { return r.ok ? r.json() : {}; }),
        fetch(BASE + 'questions.json' + VERSION).then(function (r) { return r.ok ? r.json() : []; }),
        fetch(BASE + 'alignment.json' + VERSION).then(function (r) { return r.ok ? r.json() : []; }),
        fetch(BASE + 'report.json' + VERSION).then(function (r) { return r.ok ? r.json() : null; })
      ]).then(function (parts) {
        self.topics = parts[0] || {};
        self.questions = parts[1] || [];
        self.alignment = parts[2] || [];
        self.report = parts[3];
        self._byKp = new Map(self.alignment.map(function (a) { return [a.kp_id, a]; }));
        self._byTopic = new Map(self.questions.map(function (q) { return [q.topic_id, q]; }));
        self.ready = true;
        console.log('[open-kg] ✅ 增强层: ' + Object.keys(self.topics).length +
          ' 概念 / ' + self.questions.length + ' 题 / ' + self.alignment.length + ' 对齐');
        return self;
      }).catch(function (e) {
        console.warn('[open-kg] 增强层不可用，静默降级:', e);
        return self;
      });
      return this._promise;
    },

    /** 取某 kp 的对齐 topic（按置信度降序） */
    topicsFor: function (kpId) {
      var a = this._byKp && this._byKp.get(kpId);
      if (!a) return [];
      return (a.okg_topic_ids || []).map(function (id, i) {
        var t = this.topics[id];
        return t ? Object.assign({ score: (a.scores || [])[i] }, t) : null;
      }, this).filter(Boolean);
    },

    /** 取某 kp 关联的题目（仅 high/medium 置信；low 不自动出给学生） */
    questionsFor: function (kpId, opts) {
      opts = opts || {};
      var a = this._byKp && this._byKp.get(kpId);
      if (!a) return [];
      if (!opts.includeLow && a.confidence === 'low') return [];
      var ids = new Set(a.okg_topic_ids || []);
      var limit = opts.limit || 8;
      var out = [];
      for (var i = 0; i < this.questions.length && out.length < limit; i++) {
        var q = this.questions[i];
        if (q.topic_id && ids.has(q.topic_id)) out.push(q);
      }
      return out;
    },

    /** 按学科取题（用于 PBL 候选池；默认只中文题） */
    questionsBySubject: function (subject, opts) {
      opts = opts || {};
      var lang = opts.language || 'zh';
      var limit = opts.limit || 20;
      return this.questions.filter(function (q) {
        return q.subject === subject && q.language === lang;
      }).slice(0, limit);
    },

    /** 概念前置候选（不做权威边） */
    candidatePrereqs: function (topicId) {
      var t = this.topics[topicId];
      if (!t) return [];
      return (t.prerequisites || []).map(function (p) {
        return { id: p.id, type: p.type, title: (this.topics[p.id] || {}).title || p.id, review: 'candidate' };
      }, this);
    }
  };

  global.TeachAnyOpenKG = api;
})(window);
