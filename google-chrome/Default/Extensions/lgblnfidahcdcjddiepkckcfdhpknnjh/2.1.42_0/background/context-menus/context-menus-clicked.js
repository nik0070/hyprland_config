"use strict";

async function contextMenusClicked(info) {
  const activeTabId = await getActiveTabId();
  switch (info.menuItemId) {
    case CONTEXT_MENU_IDS.blockElementsPage:
    case CONTEXT_MENU_IDS.blockElements:
      {
        await sendMessageToTab(activeTabId, {
          type: MESSAGE_TYPES.blockElementInContent,
          payload: {
            forStandsContent: true
          }
        });
        break;
      }
    case CONTEXT_MENU_IDS.unblockElementsPage:
    case CONTEXT_MENU_IDS.unblockElements:
      {
        await unblockElementsOnPage(activeTabId, true);
        break;
      }
    case CONTEXT_MENU_IDS.siteDisablePage:
    case CONTEXT_MENU_IDS.siteDisable:
      {
        const pageData = await pageDataComponent.getData(activeTabId);
        if (pageData) {
          await toggleSiteInList(pageData.hostAddress, 'deactivatedSites');
        }
        break;
      }
    case CONTEXT_MENU_IDS.disable:
    case CONTEXT_MENU_IDS.disablePage:
      {
        await toggleExtension();
        break;
      }
    default:
      break;
  }
}