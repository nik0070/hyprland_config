"use strict";

async function createNotification(notificationId, options) {
  return browser.notifications.create(notificationId, options);
}
async function clearNotification(notificationId) {
  return browser.notifications.clear(notificationId);
}