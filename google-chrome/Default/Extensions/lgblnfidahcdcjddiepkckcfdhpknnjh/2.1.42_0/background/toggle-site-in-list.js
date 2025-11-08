"use strict";

async function toggleSiteInList(host, list, sendMessageToPopup = false) {
  if (list === 'cookieBanners') {
    await cookieBannersAllowedSites.toggle(host);
  }
  if (list === 'deactivatedSites') {
    await deactivatedSites.toggle(host);
  }
  if (list === 'popups') {
    await Promise.all([popupShowNotificationList.removeValueByHost(host), popupAllowedSites.toggle(host)]);
  }
  if (sendMessageToPopup) {
    await sendMessage({
      type: MESSAGE_TYPES.toggleSiteInListResponse,
      payload: {
        forStandsPopup: true
      }
    });
  }
  const tabs = await queryTabs();
  const tabIds = tabs.filter(({
    url
  }) => host === getUrlHost(url || '')).map(({
    id
  }) => id).filter(id => typeof id === 'number');
  await pageDataComponent.refreshBulk(tabIds);
  await Promise.all([updateIcon(), updateCurrentTabContextMenus()]);
  tabIds.forEach(reloadTab);
}