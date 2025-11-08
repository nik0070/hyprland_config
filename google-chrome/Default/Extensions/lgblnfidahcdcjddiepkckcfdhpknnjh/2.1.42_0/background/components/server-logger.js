"use strict";

const LOG_EVENT_TYPES = {
  clientError: 3,
  extensionInstalled: 4,
  extensionUpdated: 5,
  extensionStateChange: 6
};
class ServerLogger {
  container = new DataContainer('logEvents', []);
  async sendToServer(events) {
    const [user, anonymousUserId, hasManagementPermissions] = await Promise.all([userData.getData(), loadAnonyId(), hasPermission('management')]);
    let extensions = [];
    if (hasManagementPermissions) {
      extensions = await getAllExtensions();
    }
    const data = {
      privateUserId: user?.privateUserId,
      anonymousUserId,
      installedExtensions: extensions.map(({
        id
      }) => id),
      appVersion: getAppVersion(),
      extensionId: getExtensionId(),
      events
    };
    await serverApi.callUrl({
      url: API_URLS.log,
      method: 'POST',
      data
    });
  }
  async prepareAndSend(sendImmediately) {
    const hasConsent = await dataProcessingConsent.getConsent();
    if (!hasConsent) {
      return;
    }
    const logs = await this.container.get();
    if (logs.length >= 10 || sendImmediately && logs.length) {
      await this.container.set([]);
      await this.sendToServer(logs);
    }
  }
  async log(event, sendImmediately = false) {
    const now = new Date();
    now.setUTCHours(now.getHours(), now.getMinutes(), now.getSeconds(), 0);
    const logObj = {
      ...event,
      eventTime: now.toISOString()
    };
    const logs = await this.container.get();
    await this.container.set([...logs, logObj]);
    await this.prepareAndSend(sendImmediately);
  }
  logInstall() {
    const event = {
      eventType: LOG_EVENT_TYPES.extensionInstalled
    };
    this.log(event, true);
  }
  logUpdate(details) {
    const event = {
      eventType: LOG_EVENT_TYPES.extensionUpdated,
      reason: details.reason,
      previousVersion: details.previousVersion || ''
    };
    this.log(event, true);
  }
  logError(error, source) {
    debug.error(`Error ${error.message} from ${source}`);
    const event = {
      eventType: LOG_EVENT_TYPES.clientError,
      source,
      message: encodeURIComponent((error.message || '').replace('\n', '')),
      stack: encodeURIComponent((error.stack || '').replace('\n', ''))
    };
    this.log(event);
  }
  logStateChange(enabled, url) {
    const event = {
      eventType: LOG_EVENT_TYPES.extensionStateChange,
      state: enabled ? 'enabled' : 'disabled',
      url
    };
    this.log(event, true);
  }
}
const serverLogger = new ServerLogger();