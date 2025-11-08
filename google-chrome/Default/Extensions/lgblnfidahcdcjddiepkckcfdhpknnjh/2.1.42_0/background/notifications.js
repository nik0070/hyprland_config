"use strict";

class Notifications {
  container = new DataContainer('notificationsData', {
    notifications: {
      [NOTIFICATION_TYPES.rate]: {
        status: NOTIFICATION_STATUSES.ready,
        showTime: {
          2: [16],
          6: [16]
        }
      },
      [NOTIFICATION_TYPES.standsBrowserPromo]: {
        status: NOTIFICATION_STATUSES.ready,
        showTime: {
          4: [17]
        }
      },
      [NOTIFICATION_TYPES.reactivate]: {
        status: NOTIFICATION_STATUSES.nothing,
        showTime: {}
      }
    },
    timeNotificationShown: 0
  });
  async showNotification(details, options) {
    await createNotification(JSON.stringify(details), {
      type: 'basic',
      iconUrl: getExtensionRelativeUrl('/icons/128.png'),
      title: options.title,
      message: options.message,
      priority: 2,
      buttons: options.buttons
    });
  }
  async init() {
    const data = await this.container.get();
    const settings = await userData.getSettings();
    const reactivateNotification = data.notifications[NOTIFICATION_TYPES.reactivate];
    if (reactivateNotification.status === NOTIFICATION_STATUSES.ready && !settings.enabled) {
      await this.showReactivateNotification();
    }
    if (reactivateNotification.status === NOTIFICATION_STATUSES.forLater) {
      await this.changeNotificationStatus(NOTIFICATION_TYPES.reactivate, NOTIFICATION_STATUSES.ready);
    }
    const todayDay = new Date().getDay();
    const todayHours = new Date().getHours();
    const thisDay = new Date().getTime();
    const rateNotification = data.notifications[NOTIFICATION_TYPES.rate];
    if (rateNotification.showTime[todayDay]?.includes(todayHours)) {
      if (rateNotification.status === NOTIFICATION_STATUSES.forLater && thisDay - data.timeNotificationShown > 30 * 24 * 60 * 60 * 1000) {
        await this.changeNotificationStatus(NOTIFICATION_TYPES.rate, NOTIFICATION_STATUSES.nothing);
        await this.setTimeNotificationShown();
        await this.showRateNotification();
      }
      if (rateNotification.status === NOTIFICATION_STATUSES.ready) {
        await this.changeNotificationStatus(NOTIFICATION_TYPES.rate, NOTIFICATION_STATUSES.forLater);
        await this.setTimeNotificationShown();
        await this.showRateNotification();
      }
    }
    const standsBrowserPromoNotification = data.notifications[NOTIFICATION_TYPES.standsBrowserPromo];
    if (standsBrowserPromoNotification.showTime[todayDay]?.includes(todayHours)) {
      if (standsBrowserPromoNotification.status === NOTIFICATION_STATUSES.ready && thisDay - data.timeNotificationShown > 20 * 24 * 60 * 60 * 1000) {
        await this.changeNotificationStatus(NOTIFICATION_TYPES.standsBrowserPromo, NOTIFICATION_STATUSES.nothing);
        await this.setTimeNotificationShown();
        await this.showStandsBrowserPromoNotification();
      }
    }
  }
  async showRateNotification() {
    const stats = await statistics.getSummary();
    function getNormalizedNumber(value) {
      if (!value) {
        return '0';
      }
      if (value < 1000) {
        return value.toString();
      }
      if (value < 1000000) {
        return `over ${Math.floor(value / 1000)}K`;
      }
      return `over ${Math.floor(value / 1000000)}M`;
    }
    await this.showNotification({
      type: NOTIFICATION_TYPES.rate
    }, {
      title: getLocalizedText('you_blocked_ads_popups_and_saved', [getNormalizedNumber(stats.blocking.ads), getNormalizedNumber(stats.blocking.popups), function (value) {
        if (!value) {
          return '0 seconds';
        }
        if (value < 100) {
          return `${Math.round(value * 10) / 10} seconds`;
        }
        if (value < 60 * 60) {
          return `over ${value / 60} minutes`;
        }
        if (value < 60 * 60 * 24) {
          return `over ${value / (60 * 60)} hours`;
        }
        return `over ${value / (60 * 60 * 24)} days`;
      }(stats.timeSaved)]),
      message: getLocalizedText('rate_stands_adblocker'),
      buttons: [{
        title: 'Rate',
        iconUrl: getExtensionRelativeUrl('/icons/rate-star.png')
      }, {
        title: getLocalizedText('close')
      }]
    });
  }
  async showStandsBrowserPromoNotification() {
    await this.showNotification({
      type: NOTIFICATION_TYPES.standsBrowserPromo
    }, {
      title: 'Try Stands Browser on Android!',
      message: 'Experience a new level of ad-blocking with our Android browser. Block ads and enjoy faster browsing—anytime, anywhere.',
      buttons: [{
        title: 'Try now'
      }, {
        title: getLocalizedText('close')
      }]
    });
  }
  async showReactivateNotification() {
    await this.showNotification({
      type: NOTIFICATION_TYPES.reactivate,
      rand: Math.random() * 10000000000000
    }, {
      title: getLocalizedText('turn_on_blocking'),
      message: getLocalizedText('stands_turned_off_would_turn'),
      buttons: [{
        title: getLocalizedText('turn_on'),
        iconUrl: getExtensionRelativeUrl('/icons/turn-on.png')
      }, {
        title: getLocalizedText('keep_off')
      }]
    });
    await this.changeNotificationStatus(NOTIFICATION_TYPES.reactivate, NOTIFICATION_STATUSES.forLater);
  }
  async showUnblockNotification(elementsCount) {
    await this.showNotification({
      type: NOTIFICATION_TYPES.unblock,
      rand: Math.random() * 10000000000000
    }, {
      title: elementsCount > 0 ? getLocalizedText('you_unblocked_on_this_page', [`${elementsCount}`, elementsCount > 1 ? getLocalizedText('elements') : getLocalizedText('element')]) : getLocalizedText('no_blocked_on_this_page'),
      message: getLocalizedText('')
    });
  }
  async showExtensionOnOffNotification(bypass) {
    await this.showNotification({
      type: NOTIFICATION_TYPES.extensionOnOff,
      tabId: await getActiveTabId(),
      rand: Math.random() * 10000000000000
    }, {
      title: bypass ? getLocalizedText('stands_back_on') : getLocalizedText('stands_turned_off'),
      message: getLocalizedText('refresh_take_effect'),
      buttons: [{
        title: getLocalizedText('refresh'),
        iconUrl: getExtensionRelativeUrl('/icons/refresh.png')
      }, {
        title: getLocalizedText('close'),
        iconUrl: getExtensionRelativeUrl('/icons/close.png')
      }]
    });
  }
  async changeNotificationStatus(type, status) {
    const data = await this.container.get();
    data.notifications[type].status = status;
    await this.container.set(data);
  }
  async setTimeNotificationShown() {
    const data = await this.container.get();
    data.timeNotificationShown = new Date().getTime();
    await this.container.set(data);
  }
  async sendDataToServer() {
    const data = await this.container.get();
    const user = await userData.getData();
    await serverApi.callUrl({
      data: data.notifications,
      url: `${API_URLS.notifications}${user?.privateUserId}`,
      method: 'PUT'
    });
  }
  async onClick(notificationId, buttonIndex = 0) {
    const actions = [{
      [NOTIFICATION_TYPES.rate]: async () => {
        await openTabWithUrl(browserInfo.getRateUrl());
        await this.changeNotificationStatus(NOTIFICATION_TYPES.rate, NOTIFICATION_STATUSES.done);
      },
      [NOTIFICATION_TYPES.reactivate]: async () => {
        await toggleExtension();
        await this.changeNotificationStatus(NOTIFICATION_TYPES.reactivate, NOTIFICATION_STATUSES.done);
      },
      [NOTIFICATION_TYPES.extensionOnOff]: d => reloadTab(d.tabId),
      [NOTIFICATION_TYPES.siteOnOff]: d => reloadTab(d.tabId),
      [NOTIFICATION_TYPES.standsBrowserPromo]: async () => {
        await openTabWithUrl('https://project10941031.tilda.ws/');
        await this.changeNotificationStatus(NOTIFICATION_TYPES.standsBrowserPromo, NOTIFICATION_STATUSES.done);
      }
    }, {
      [NOTIFICATION_TYPES.rate]: async () => {
        await this.changeNotificationStatus(NOTIFICATION_TYPES.rate, NOTIFICATION_STATUSES.nothing);
      },
      [NOTIFICATION_TYPES.reactivate]: async () => {
        await this.changeNotificationStatus(NOTIFICATION_TYPES.reactivate, NOTIFICATION_STATUSES.forLater);
      },
      [NOTIFICATION_TYPES.standsBrowserPromo]: async () => {
        await this.changeNotificationStatus(NOTIFICATION_TYPES.standsBrowserPromo, NOTIFICATION_STATUSES.nothing);
      }
    }];
    const details = JSON.parse(notificationId);
    actions[buttonIndex][details.type]?.(details);
    await clearNotification(notificationId);
  }
}
const notifications = new Notifications();