"use strict";

class PageDataComponent {
  container = new DataContainer('pageDataDict', {});
  async getData(tabId) {
    const data = await this.container.get();
    return data[tabId];
  }
  async setData(tabId, pageData) {
    const data = await this.container.get();
    data[tabId] = pageData;
    await this.container.set(data);
  }
  async updateData(tabId, pageData) {
    const data = await this.container.get();
    const oldPageData = data[tabId];
    if (oldPageData) {
      data[tabId] = {
        ...oldPageData,
        ...pageData
      };
    }
    await this.container.set(data);
  }
  async deleteData(tabId) {
    const data = await this.container.get();
    delete data[tabId];
    await this.container.set(data);
  }
  getAllData() {
    return this.container.get();
  }
  setAllData(data) {
    return this.container.set(data);
  }
  async create(url) {
    const isValidSite = url.startsWith('http');
    const host = getUrlHost(url);
    const settings = await userData.getSettings();
    const blockPopups = isValidSite && settings.enabled && settings.blockPopups && !(await popupAllowedSites.isAllowed(host));
    return {
      pageUrl: url,
      hostAddress: host,
      enabled: isValidSite && settings.enabled && !(await deactivatedSites.isHostDeactivated(host)),
      hideCookieBanners: isValidSite && !!settings.hideCookieBanners && !(await cookieBannersAllowedSites.isAllowed(host)),
      blockPopups,
      showBlockedPopupNotification: blockPopups ? (await popupShowNotificationList.getValueByHost(host)) ?? true : true,
      isValidSite,
      loadTime: new Date().getTime(),
      blockTracking: settings.blockTracking,
      customCss: isValidSite ? await customCssRules.getCssRules(host) : undefined,
      previousUrl: '',
      stats: {
        total: 0,
        ads: 0,
        trackers: 0,
        popups: 0,
        cookieBanners: 0,
        timeSaved: 0
      }
    };
  }
  async refreshBulk(tabIds) {
    const data = await this.container.get();
    for (const tabId of tabIds) {
      const oldData = data[tabId];
      if (oldData) {
        const newData = await this.create(oldData.pageUrl);
        newData.previousUrl = oldData.previousUrl;
        newData.loadTime = oldData.loadTime;
        newData.stats = oldData.stats;
        data[tabId] = newData;
      }
    }
    await this.container.set(data);
  }
  async createForAllTabs() {
    const tabs = await queryTabs({
      windowType: 'normal'
    });
    for (const {
      id,
      url
    } of tabs) {
      if (typeof id === 'number' && typeof url === 'string') {
        const currentData = await this.getData(id);
        if (!currentData) {
          const data = await this.create(url);
          await this.setData(id, data);
        }
      }
    }
  }
  async getFramePageData({
    tabId,
    frameId,
    frameUrl,
    isMainFrame
  }) {
    const mainFramePageData = await this.getData(tabId);
    let result = null;
    if (!frameId || isMainFrame) {
      result = mainFramePageData || null;
    }
    if (!result) {
      result = await this.create(frameUrl);
    }
    if (frameId && mainFramePageData?.isValidSite && result) {
      result.enabled = mainFramePageData.enabled;
    }
    return result;
  }
  async getActiveTabData() {
    const tabId = await getActiveTabId();
    return this.getData(tabId);
  }
}
const pageDataComponent = new PageDataComponent();