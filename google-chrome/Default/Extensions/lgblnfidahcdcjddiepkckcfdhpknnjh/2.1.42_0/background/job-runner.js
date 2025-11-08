"use strict";

class JobRunner {
  allJobs = {};
  onAlarm(alarm) {
    this.allJobs[alarm.name]?.();
  }
  addJob(name, func, periodInMinutes) {
    browser.alarms.get(name).then(alarm => {
      if (!alarm || alarm.periodInMinutes !== periodInMinutes) {
        browser.alarms.create(name, {
          periodInMinutes
        });
      }
    });
    this.allJobs[name] = func;
  }
}
const jobRunner = new JobRunner();
function createAllJobs() {
  jobRunner.addJob('reset-icon-badge', updateIcon, 10);
  jobRunner.addJob('heartbeat', heartbeat, 60);
  jobRunner.addJob('cleanup-tabs', tab.cleanupTabs.bind(tab), 30);
  jobRunner.addJob('periodic-logger-save', serverLogger.prepareAndSend.bind(serverLogger, true), 60);
  jobRunner.addJob('periodic-reporter-save', analysisReporter.reportBulk.bind(analysisReporter, true), 60);
  jobRunner.addJob('send-notifications-data', notifications.sendDataToServer.bind(notifications), 60 * 24 * 7);
  jobRunner.addJob('get-matched-rules', countMatchedRules, 1);
}