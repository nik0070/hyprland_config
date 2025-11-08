"use strict";

async function updateIcon() {
  try {
    const pageData = await pageDataComponent.getActiveTabData();
    if (!pageData) {
      return;
    }
    const [{
      enabled,
      iconBadgePeriod
    }, hasConsent] = await Promise.all([userData.getSettings(), dataProcessingConsent.getConsent()]);
    const disabled = !hasConsent || !pageData.enabled || !enabled;
    await setIcon({
      path: {
        19: `icons/19${disabled ? '_gray' : ''}.png`,
        38: `icons/38${disabled ? '_gray' : ''}.png`
      }
    });
    if (disabled) {
      await Promise.all([setAppIconBadgeText(getLocalizedText(!enabled || !hasConsent ? 'off' : '')), setAppIconBadgeTitle(!enabled || !hasConsent ? getLocalizedText('stands_is_paused') : getLocalizedText('the_site_was_whitelisted', [pageData.hostAddress]))]);
      return;
    }
    let amount = 0;
    let title = '';
    if (iconBadgePeriod === ICON_BADGE_PERIODS.Today) {
      const {
        today
      } = await statistics.getSummary();
      amount = today;
      title = `${amount} ${getLocalizedText('blocks_today')}`;
    }
    if (iconBadgePeriod === ICON_BADGE_PERIODS.Page) {
      amount = pageData.stats.total;
      title = `${amount} ${getLocalizedText('blocks_on_this_page')}`;
    }
    await Promise.all([setAppIconBadgeText(amount > 0 ? amount.toString() : ''), setAppIconBadgeTitle(amount > 0 ? title : getLocalizedText('stands'))]);
  } catch (error) {
    debug.error(`Error in updateIcon: ${error}`);
  }
}