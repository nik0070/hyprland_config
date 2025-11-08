"use strict";

async function updateUserSettings(settings, sendMessageForPopup = false) {
  const currentSettings = await userData.getSettings();
  await userData.updateData({
    settings: {
      ...currentSettings,
      ...settings
    }
  });
  if (sendMessageForPopup) {
    await sendMessage({
      type: MESSAGE_TYPES.updateUserSettingsResponse,
      payload: {
        forStandsPopup: true
      }
    });
  }
  if (typeof settings.enabled === 'boolean' && settings.enabled !== currentSettings.enabled) {
    await Promise.all([updateCurrentTabContextMenus(), notifications.changeNotificationStatus(NOTIFICATION_TYPES.reactivate, settings.enabled ? NOTIFICATION_STATUSES.nothing : NOTIFICATION_STATUSES.ready), updateEnabledRulesets({
      [settings.enabled ? 'enableRulesetIds' : 'disableRulesetIds']: ['requests']
    })]);
    const pageData = await pageDataComponent.getActiveTabData();
    serverLogger.logStateChange(settings.enabled, pageData?.hostAddress);
  }
  if (typeof settings.hideCookieBanners === 'boolean' && settings.hideCookieBanners !== currentSettings.hideCookieBanners) {
    await updateEnabledRulesets({
      [settings.hideCookieBanners ? 'enableRulesetIds' : 'disableRulesetIds']: ['cookie-banners-requests']
    });
  }
  const tabs = await queryTabs({
    windowType: 'normal'
  });
  const tabIds = tabs.map(({
    id
  }) => id).filter(id => typeof id === 'number');
  await applyNewSettingsOnTabs(tabIds);
}