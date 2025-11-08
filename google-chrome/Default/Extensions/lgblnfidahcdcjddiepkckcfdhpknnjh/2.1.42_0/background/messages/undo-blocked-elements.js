"use strict";

async function actionInCaseUndoBlockedElements() {
  const activeTabId = await getActiveTabId();
  await unblockElementsOnPage(activeTabId);
  await sendMessage({
    type: MESSAGE_TYPES.undoBlockedElementsResponse,
    payload: {
      forStandsPopup: true
    }
  });
}