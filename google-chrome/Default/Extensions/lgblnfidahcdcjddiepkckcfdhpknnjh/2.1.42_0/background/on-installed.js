"use strict";

async function openOnboardingPageOnInstall() {
  const tabs = await queryTabs();
  const tab = tabs.find(({
    url
  }) => url?.includes('detail/stands-adblocker') || url?.includes('detail/adblocker-stands') || url?.includes('addon/stands-fair-adblocker') || url?.includes('addons/detail/fair-adblocker'));
  const search = tab ? new URL(tab.url || '').search : '';
  await openTabWithUrl(`https://www.standsapp.org/thank-you-${"chrome"}${search}`);
}
async function reportOpenedTabs() {
  const data = await pageDataComponent.getAllData();
  const arr = Object.values(data).filter(r => r.isValidSite).map(r => ({
    loadTime: r.loadTime,
    previousUrl: r.previousUrl,
    pageUrl: r.pageUrl
  }));
  for (let i = 0; i < arr.length; i += 10) {
    await analysisReporter.addReportsBulk(arr.slice(i, i + 10));
  }
}
async function injectContentScriptsOnExistingTabs() {
  const tabs = await queryTabs({
    url: '<all_urls>'
  });
  const js = getManifest().content_scripts?.filter(s => s.js && s.js.length > 1).flatMap(s => s.js || []);
  for (const tab of tabs) {
    if (typeof tab.id === 'number') {
      await executeScriptOnTab(tab.id, {
        allFrames: true,
        files: js
      });
    }
  }
}
async function migrateData() {
  const allowedKeys = ['anonyReportObjectKey', 'dailyStatsBuffer', 'cookieBannersAllowedSites', 'trackersListValue', 'trackersListDate', 'easylistCssValue', 'easylistCssDate', 'popupAllowedSites', 'popupShowNotificationList', 'notificationsData', 'deactivatedSites', 'dataProcessingConsent', 'customCssRules', 'anonyReportBulk', 'pageDataDict', 'logEvents', 'tabsData', 'userData'];
  try {
    const allKeys = await storageService.keys();
    for (const key of allKeys.filter(k => !allowedKeys.includes(k))) {
      await storageService.remove(key);
    }
    const pagesData = await storageService.get('pageDataDict');
    if (pagesData) {
      for (const id in pagesData) {
        if (!pagesData[id].stats) {
          pagesData[id].stats = {
            total: 0,
            ads: 0,
            trackers: 0,
            popups: 0,
            cookieBanners: 0,
            timeSaved: 0
          };
        }
      }
      await storageService.set('pageDataDict', pagesData);
    }
    await chrome.declarativeNetRequest.setExtensionActionOptions({
      displayActionCountAsBadgeText: false
    });
  } catch (error) {
    debug.error('Failed to migrate data', error);
  }
}
async function openNoMoreCookieBannersPage({
  reason
}, hasConsent) {
  if (!hasConsent) {
    return;
  }
  const settings = await userData.getSettings();
  if (reason === 'install' || reason === 'update' && typeof settings.hideCookieBanners !== 'boolean') {
    await openTabWithUrl('/index.html#no-more-cookie-banners');
  }
}
async function onInstalled(details) {
  if (details.reason === 'update') {
    await migrateData();
  }
  const [,, hasConsent] = await Promise.all([createContextMenus(), pageDataComponent.createForAllTabs(), dataProcessingConsent.getConsent()]);
  if (details.reason === 'install') {
    serverLogger.logInstall();
    await Promise.all([openOnboardingPageOnInstall(), reportOpenedTabs(), openNoMoreCookieBannersPage(details, hasConsent)]);
    if (hasConsent) {
      setTimeout(injectContentScriptsOnExistingTabs, 5000);
    }
  } else {
    await openNoMoreCookieBannersPage(details, hasConsent);
    serverLogger.logUpdate(details);
  }
  if (!hasConsent) {
    await openTabWithUrl('/index.html');
  }
}