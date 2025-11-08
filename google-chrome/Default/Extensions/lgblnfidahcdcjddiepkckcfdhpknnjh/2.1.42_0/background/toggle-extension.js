"use strict";

async function toggleExtension() {
  const settings = await userData.getSettings();
  await updateUserSettings({
    enabled: !settings.enabled,
    iconBadgePeriod: settings.enabled ? ICON_BADGE_PERIODS.Disabled : ICON_BADGE_PERIODS.Page
  });
  await notifications.showExtensionOnOffNotification(settings.enabled);
}