"use strict";

const easylistCssData = new DataUpdaterFromServer({
  name: 'easylistCss',
  expiration: 60 * 24 * 4 + 60,
  url: API_URLS.easyList
});
const trackersListData = new DataUpdaterFromServer({
  name: 'trackersList',
  expiration: 90 * 24 * 60,
  url: API_URLS.trackersList
});
async function loadLists() {
  await Promise.allSettled([easylistCssData.start(), trackersListData.start()]);
}