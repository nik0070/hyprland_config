"use strict";

function getDateString(date, hours = 0) {
  const result = new Date(date);
  result.setUTCHours(hours, 0, 0, 0);
  return result.toISOString();
}
class Statistics {
  container = new DataContainer('dailyStatsBuffer', {});
  async incrementBlock({
    typeId,
    tabId,
    amount
  }) {
    const [hasConsent, pageData] = await Promise.all([dataProcessingConsent.getConsent(), pageDataComponent.getData(tabId)]);
    if (!hasConsent || !pageData) {
      return;
    }
    const hour = getDateString(new Date(), new Date().getHours());
    const data = await this.container.get();
    data[hour] = data[hour] || {};
    if (typeId === BLOCK_TYPES.ad) {
      data[hour].ads = (data[hour].adServers || data[hour].ads || 0) + amount;
      pageData.stats.ads += amount;
    }
    if (typeId === BLOCK_TYPES.popup) {
      data[hour].popups = (data[hour].popups || 0) + amount;
      pageData.stats.popups += amount;
    }
    if (typeId === BLOCK_TYPES.tracker) {
      data[hour].trackers = (data[hour].trackers || 0) + amount;
      pageData.stats.trackers += amount;
    }
    if (typeId === BLOCK_TYPES.cookieBanner) {
      data[hour].cookieBanners = (data[hour].cookieBanners || 0) + amount;
      pageData.stats.cookieBanners += amount;
    }
    pageData.stats.total += amount;
    pageData.stats.timeSaved += amount * this.getCoefficient(typeId);
    await Promise.all([pageDataComponent.updateData(tabId, pageData), this.container.set(data)]);
  }
  getCoefficient(type) {
    if (type === BLOCK_TYPES.ad) {
      return 0.05;
    }
    if (type === BLOCK_TYPES.tracker) {
      return 0.01;
    }
    return 1;
  }
  async getBlockingData() {
    const result = {
      total: {
        ads: 0,
        trackers: 0,
        popups: 0,
        cookieBanners: 0
      },
      daily: {}
    };
    const data = await this.container.get();
    for (const date in data) {
      if (Number.isNaN(Date.parse(date))) {
        continue;
      }
      const dateObj = new Date(date);
      const dateKey = getDateString(dateObj);
      if (!result.daily[dateKey]) {
        result.daily[dateKey] = {
          ads: 0,
          trackers: 0,
          popups: 0,
          cookieBanners: 0
        };
      }
      result.daily[dateKey].ads += data[date].adServers || data[date].ads || 0;
      result.total.ads += data[date].adServers || data[date].ads || 0;
      result.daily[dateKey].trackers += data[date].trackers || 0;
      result.total.trackers += data[date].trackers || 0;
      result.daily[dateKey].popups += data[date].popups || 0;
      result.total.popups += data[date].popups || 0;
      result.daily[dateKey].cookieBanners += data[date].cookieBanners || 0;
      result.total.cookieBanners += data[date].cookieBanners || 0;
    }
    result.daily = function (obj) {
      const dates = Object.keys(obj).map(date => new Date(date)).sort((a, b) => a.getTime() - b.getTime());
      if (!dates.length) {
        return obj;
      }
      const res = {
        ...obj
      };
      const startDate = dates[0];
      const endDate = dates[dates.length - 1];
      const currentDate = new Date(startDate);
      while (currentDate <= endDate) {
        const isoDate = currentDate.toISOString();
        if (!obj[isoDate]) {
          res[isoDate] = {
            ads: 0,
            trackers: 0,
            popups: 0,
            cookieBanners: 0
          };
        }
        currentDate.setDate(currentDate.getDate() + 1);
      }
      return res;
    }(result.daily);
    return result;
  }
  async getSummary() {
    const summary = {
      today: 0,
      total: 0,
      blocking: {
        ads: 0,
        trackers: 0,
        popups: 0,
        cookieBanners: 0
      },
      timeSaved: 0
    };
    const todayMidnight = new Date(getDateString(new Date()));
    const data = await this.container.get();
    for (const date in data) {
      if (isNaN(Date.parse(date))) {
        continue;
      }
      const currentDate = new Date(date);
      summary.blocking.ads += data[date].adServers || data[date].ads || 0;
      summary.blocking.trackers += data[date].trackers || 0;
      summary.blocking.popups += data[date].popups || 0;
      summary.blocking.cookieBanners += data[date].cookieBanners || 0;
      summary.total += summary.blocking.ads + summary.blocking.trackers + summary.blocking.popups + summary.blocking.cookieBanners;
      if (currentDate >= todayMidnight) {
        summary.today += summary.total;
      }
    }
    summary.timeSaved += summary.blocking.ads * this.getCoefficient(BLOCK_TYPES.ad) + summary.blocking.trackers * this.getCoefficient(BLOCK_TYPES.tracker) + summary.blocking.popups * this.getCoefficient(BLOCK_TYPES.popup) + summary.blocking.cookieBanners * this.getCoefficient(BLOCK_TYPES.cookieBanner);
    return summary;
  }
}
const statistics = new Statistics();