"use strict";

class CookieBannersAllowedSites {
  container = new DataContainer('cookieBannersAllowedSites', {});
  async init() {
    const sitesData = await this.container.get();
    await Promise.all([this.updateDynamicRules(sitesData), this.updateContentScripts(sitesData)]);
  }
  async updateDynamicRules(sitesData) {
    const hosts = Object.keys(sitesData);
    const addRules = hosts.length ? [{
      id: ALLOWED_RULES_IDS.cookieBanner,
      priority: 100,
      action: {
        type: 'allow'
      },
      condition: {
        initiatorDomains: hosts
      }
    }] : [];
    await updateDynamicRules({
      removeRuleIds: [2],
      addRules
    });
  }
  async updateContentScripts(sitesData) {
    const data = [{
      hosts: ['euronews.com'],
      scripts: [{
        allFrames: true,
        id: 'euronews.com-cookie-banner-custom-script',
        js: ['common/helpers.js', 'content/custom-scripts/cookie-banners/euronews.com.js'],
        matches: ['*://*.euronews.com/*'],
        runAt: 'document_start'
      }]
    }, {
      hosts: ['google.com'],
      scripts: [{
        allFrames: true,
        id: 'google.com-cookie-banner-custom-script',
        js: ['common/helpers.js', 'content/custom-scripts/cookie-banners/google.com.js'],
        matches: ['*://*.google.com/*'],
        runAt: 'document_start'
      }]
    }, {
      hosts: ['facebook.com'],
      scripts: [{
        allFrames: true,
        id: 'facebook.com-cookie-banner-custom-script',
        js: ['common/helpers.js', 'content/custom-scripts/cookie-banners/facebook.com.js'],
        matches: ['*://*.facebook.com/*'],
        runAt: 'document_start'
      }]
    }, {
      hosts: ['consent.yahoo.com'],
      scripts: [{
        allFrames: true,
        id: 'consent.yahoo.com-cookie-banner-custom-script',
        js: ['common/helpers.js', 'content/custom-scripts/cookie-banners/consent.yahoo.com.js'],
        matches: ['*://*.consent.yahoo.com/*'],
        runAt: 'document_end'
      }]
    }];
    ['theguardian.com', 'telegraph.co.uk', 'thesun.co.uk', 'politico.eu'].forEach(host => {
      data.push({
        hosts: [host],
        scripts: [{
          allFrames: true,
          id: `${host}-cookie-banner-custom-script`,
          js: ['common/helpers.js', 'content/custom-scripts/cookie-banners/sp-message-iframe.js'],
          matches: [`*://*.${host}/*`],
          runAt: 'document_start'
        }]
      });
    });
    const registeredScripts = await getRegisteredContentScripts({
      ids: data.flatMap(({
        scripts
      }) => scripts.map(({
        id
      }) => id))
    });
    const idsToUnregister = data.filter(({
      hosts
    }) => hosts.some(h => sitesData[h])).flatMap(({
      scripts
    }) => scripts).filter(({
      id
    }) => registeredScripts.some(s => s.id === id)).map(({
      id
    }) => id);
    if (idsToUnregister.length) {
      await unregisterContentScripts({
        ids: idsToUnregister
      });
    }
    const scriptsToRegister = data.flatMap(({
      scripts
    }) => scripts.filter(script => !idsToUnregister.includes(script.id) && !registeredScripts.some(s => s.id === script.id)));
    if (scriptsToRegister.length) {
      await registerContentScripts(scriptsToRegister);
    }
  }
  async toggle(host) {
    const data = await this.container.get();
    if (data[host]) {
      delete data[host];
    } else {
      data[host] = true;
    }
    await Promise.all([this.container.set(data), this.updateDynamicRules(data), this.updateContentScripts(data)]);
  }
  async getList() {
    const data = await this.container.get();
    return Object.keys(data);
  }
  async isAllowed(host) {
    const data = await this.container.get();
    return data[host];
  }
}
const cookieBannersAllowedSites = new CookieBannersAllowedSites();