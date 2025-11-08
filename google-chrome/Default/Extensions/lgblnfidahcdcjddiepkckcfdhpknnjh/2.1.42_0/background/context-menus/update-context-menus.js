"use strict";

async function updateCurrentTabContextMenus() {
  const [pageData, settings] = await Promise.all([pageDataComponent.getActiveTabData(), userData.getSettings()]);
  await updateContextMenuItem(CONTEXT_MENU_IDS.disable, {
    title: settings.enabled ? getLocalizedText('turn_off_blocking_everywhere') : getLocalizedText('turn_on_blocking'),
    enabled: true
  });
  await updateContextMenuItem(CONTEXT_MENU_IDS.disablePage, {
    title: settings.enabled ? getLocalizedText('turn_off_blocking_everywhere') : getLocalizedText('turn_on_blocking'),
    enabled: true
  });
  if (pageData) {
    const isMenuEnabled = pageData.isValidSite && settings.enabled;
    const isHostDisabled = !!pageData.hostAddress && (await deactivatedSites.isHostDeactivated(pageData.hostAddress));
    const isCurrentHostMenuEnabled = isMenuEnabled && !isHostDisabled;
    const customCssSelectors = await customCssRules.getSelectors(pageData.hostAddress);
    const documentUrlPatterns = await customCssRules.getUrlPatterns();
    const itemsToUpdate = [{
      id: CONTEXT_MENU_IDS.siteDisable,
      props: {
        title: isHostDisabled ? getLocalizedText('resume_blocking') : getLocalizedText('whitelist_this_site'),
        enabled: isMenuEnabled
      }
    }, {
      id: CONTEXT_MENU_IDS.siteDisablePage,
      props: {
        title: isHostDisabled ? getLocalizedText('resume_blocking') : getLocalizedText('whitelist_this_site'),
        enabled: isMenuEnabled
      }
    }, {
      id: CONTEXT_MENU_IDS.blockElements,
      props: {
        enabled: isCurrentHostMenuEnabled
      }
    }, {
      id: CONTEXT_MENU_IDS.blockElementsPage,
      props: {
        enabled: isCurrentHostMenuEnabled
      }
    }, {
      id: CONTEXT_MENU_IDS.unblockElements,
      props: {
        enabled: isCurrentHostMenuEnabled && !!customCssSelectors
      }
    }, {
      id: CONTEXT_MENU_IDS.unblockElementsPage,
      props: {
        enabled: isCurrentHostMenuEnabled,
        documentUrlPatterns
      }
    }];
    for (const {
      id,
      props
    } of itemsToUpdate) {
      await updateContextMenuItem(id, props);
    }
  }
}