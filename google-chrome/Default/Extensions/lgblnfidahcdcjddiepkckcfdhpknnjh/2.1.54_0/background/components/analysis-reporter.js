"use strict";

class AnalysisReporter {
  container = new DataContainer('anonyReportBulk', {
    bulk: []
  });
  async addReportsBulk(data) {
    const reports = await this.container.get();
    await this.container.set({
      bulk: [...reports.bulk, ...data]
    });
    await this.reportBulk();
  }
  async reportBulk(sendImmediately = false) {
    const hasConsent = await dataProcessingConsent.getConsent();
    if (!hasConsent) {
      return;
    }
    const data = await this.container.get();
    if (data.bulk.length >= 10 || data.bulk.length && sendImmediately) {
      const reports = data.bulk.splice(0, 10);
      await this.container.set({
        bulk: data.bulk
      });
      await this.sendAnonyReportToServer(reports);
    }
  }
  async sendAnonyReportToServer(data) {
    try {
      const [nid, os, cc] = await Promise.all([loadAnonyId(), getOperatingSystem(), userData.getGeo()]);
      const rows = data.map(r => ({
        nid,
        pid: '',
        sid: '',
        cc,
        ts: r.loadTime,
        rfu: encodeURIComponent(r.previousUrl),
        tu: encodeURIComponent(r.pageUrl),
        trt: r.trt || '',
        trq: r.trq?.join(',') || '',
        os,
        ver: getAppVersion(),
        blk: data.length
      }));
      const {
        error
      } = await serverApi.callUrl({
        url: API_URLS.reportUrl,
        method: 'POST',
        data: {
          rows
        }
      });
      if (error) {
        throw error;
      }
    } catch (e) {
      const {
        bulk
      } = await this.container.get();
      await this.container.set({
        bulk: [...data, ...bulk]
      });
      serverLogger.logError(e, 'AnalysisReporter.sendAnonyReportToServer', true);
    }
  }
}
const analysisReporter = new AnalysisReporter();