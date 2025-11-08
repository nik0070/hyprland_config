"use strict";

async function sendMessage(message) {
  if (browser.runtime?.id) {
    try {
      return await browser.runtime.sendMessage(message);
    } catch (error) {
      debug.error(`Error sending message with type ${message.type}`, error);
    }
  }
}