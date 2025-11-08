"use strict";

async function unblockElementsOnPage(tabId, showNotification) {
  const pageData = await pageDataComponent.getData(tabId);
  if (pageData) {
    if (showNotification) {
      const elementsCount = await customCssRules.countRulesOnTab(tabId);
      await notifications.showUnblockNotification(elementsCount);
    }
    await Promise.all([customCssRules.remove(pageData.hostAddress), pageDataComponent.refreshBulk([tabId])]);
    const newPageData = await pageDataComponent.getData(tabId);
    await sendMessageToTab(tabId, {
      type: MESSAGE_TYPES.updatePageData,
      payload: {
        pageData: newPageData
      }
    });
  }
}