"use strict";

const hasPermission = permission => {
  return browser.permissions.contains({
    permissions: [permission]
  });
};