"use strict";

class DeactivatedSites {
  container = new DataContainer('deactivatedSites', {});
  async init() {
    const sites = await this.container.get();
    await this.updateDynamicRules(sites);
    await this.updateContentScripts(sites);
  }
  async updateContentScripts(sitesData) {
    const data = [{
      hosts: ['facebook.com'],
      scripts: [{
        allFrames: true,
        id: 'facebook-customer-script',
        js: ['content/custom-scripts/meta/common.js', 'content/custom-scripts/meta/facebook.js'],
        matches: ['*://*.facebook.com/*'],
        runAt: 'document_start'
      }]
    }, {
      hosts: ['instagram.com'],
      scripts: [{
        allFrames: true,
        id: 'instagram-customer-script',
        js: ['content/custom-scripts/meta/common.js', 'content/custom-scripts/meta/instagram.js'],
        matches: ['*://*.instagram.com/*'],
        runAt: 'document_start'
      }]
    }, {
      hosts: ['youtube.com', 'youtu.be', 'yt.be'],
      scripts: [{
        allFrames: true,
        id: 'yt-main',
        js: ['content/custom-scripts/youtube/globals.js', 'content/custom-scripts/dependencies/safe-self.js', 'content/custom-scripts/dependencies/modify-setTimeout.js', 'content/custom-scripts/dependencies/generate-exception-token.js', 'content/custom-scripts/dependencies/json-prune-fetch-response.js', 'content/custom-scripts/dependencies/json-prune-xhr-response.js', 'content/custom-scripts/dependencies/does-object-match-properties.js', 'content/custom-scripts/dependencies/matches-stack-trace.js', 'content/custom-scripts/dependencies/find-object-owner.js', 'content/custom-scripts/dependencies/prune-object.js', 'content/custom-scripts/dependencies/create-property-match-map.js', 'content/custom-scripts/dependencies/replace-fetch-response-content.js', 'content/custom-scripts/dependencies/replace-xhr-response-content.js', 'content/custom-scripts/dependencies/schedule-execution.js', 'content/custom-scripts/dependencies/define-constant.js', 'content/custom-scripts/dependencies/get-validated-constant.js', 'content/custom-scripts/youtube/main.js'],
        matches: ['*://*.youtube.com/*', '*://*.youtu.be/*', '*://*.yt.be/*'],
        runAt: 'document_start',
        world: 'MAIN'
      }, {
        allFrames: true,
        id: 'yt-isolated',
        js: ['content/custom-scripts/youtube/isolated.js'],
        matches: ['*://*.youtube.com/*', '*://*.youtu.be/*', '*://*.yt.be/*'],
        runAt: 'document_start'
      }]
    }, {
      hosts: ['bbc.com'],
      scripts: [{
        allFrames: true,
        id: 'bbc.com-customer-script',
        js: ['content/custom-scripts/bbc.com.js'],
        matches: ['*://*.bbc.com/*'],
        runAt: 'document_start'
      }]
    }, {
      hosts: ['marca.com'],
      scripts: [{
        allFrames: true,
        id: 'marca.com-customer-script',
        js: ['content/custom-scripts/dependencies/unblock-content-scrolling.js', 'content/custom-scripts/marca.com.js'],
        matches: ['*://*.marca.com/*'],
        runAt: 'document_start'
      }]
    }, {
      hosts: ['eldiario.es'],
      scripts: [{
        allFrames: true,
        id: 'eldiario.es-customer-script',
        js: ['content/custom-scripts/dependencies/unblock-content-scrolling.js', 'content/custom-scripts/eldiario.es.js'],
        matches: ['*://*.eldiario.es/*'],
        runAt: 'document_start'
      }]
    }, {
      hosts: ['dailymail.co.uk'],
      scripts: [{
        allFrames: true,
        id: 'dailymail.co.uk-customer-script',
        js: ['content/custom-scripts/dependencies/unblock-content-scrolling.js', 'content/custom-scripts/dailymail.co.uk.js'],
        matches: ['*://*.dailymail.co.uk/*'],
        runAt: 'document_end'
      }]
    }, {
      hosts: ['abc.es'],
      scripts: [{
        allFrames: true,
        id: 'abc.es-customer-script',
        js: ['content/custom-scripts/dependencies/unblock-content-scrolling.js', 'content/custom-scripts/abc.es.js'],
        matches: ['*://*.abc.es/*'],
        runAt: 'document_end'
      }]
    }, {
      hosts: ['sporcle.com'],
      scripts: [{
        allFrames: true,
        id: 'sporcle.com-customer-script',
        js: ['content/custom-scripts/dependencies/unblock-content-scrolling.js', 'content/custom-scripts/sporcle.com.js'],
        matches: ['*://*.sporcle.com/*'],
        runAt: 'document_end'
      }]
    }, {
      hosts: ['eltiempo.es'],
      scripts: [{
        allFrames: true,
        id: 'eltiempo.es-customer-script',
        js: ['content/custom-scripts/dependencies/unblock-content-scrolling.js', 'content/custom-scripts/eltiempo.es.js'],
        matches: ['*://*.eltiempo.es/*'],
        runAt: 'document_end'
      }]
    }, {
      hosts: ['op.gg'],
      scripts: [{
        allFrames: true,
        id: 'op.gg-customer-script',
        js: ['content/custom-scripts/dependencies/unblock-content-scrolling.js', 'content/custom-scripts/op.gg.js'],
        matches: ['*://*.op.gg/*'],
        runAt: 'document_end'
      }]
    }, {
      hosts: ['usatoday.com'],
      scripts: [{
        allFrames: true,
        id: 'usatoday.com-customer-script',
        js: ['content/custom-scripts/dependencies/unblock-content-scrolling.js', 'content/custom-scripts/usatoday.com.js'],
        matches: ['*://*.usatoday.com/*'],
        runAt: 'document_end'
      }]
    }, {
      hosts: ['quizlet.com'],
      scripts: [{
        allFrames: true,
        id: 'quizlet.com-customer-script',
        js: ['content/custom-scripts/quizlet.com.js'],
        matches: ['*://*.quizlet.com/*'],
        runAt: 'document_start'
      }]
    }, {
      hosts: ['qq.com', 'new.qq.com'],
      scripts: [{
        allFrames: true,
        id: 'qq.com-customer-script',
        js: ['content/custom-scripts/dependencies/override-json.js', 'content/custom-scripts/qq.com.js'],
        matches: ['*://*.qq.com/*', '*://*.new.qq.com/*'],
        runAt: 'document_start'
      }]
    }, {
      hosts: ['bing.com'],
      scripts: [{
        allFrames: true,
        id: 'bing.com-customer-script',
        js: ['content/helpers.js', 'content/custom-scripts/dependencies/hide-elems-in-shadow-dom.js', 'content/custom-scripts/bing.com.js'],
        matches: ['*://*.bing.com/*'],
        runAt: 'document_start'
      }]
    }, {
      hosts: ['msn.com'],
      scripts: [{
        allFrames: true,
        id: 'msn.com-customer-script',
        js: ['content/helpers.js', 'content/custom-scripts/dependencies/hide-elems-in-shadow-dom.js', 'content/custom-scripts/msn.com.js'],
        matches: ['*://*.msn.com/*'],
        runAt: 'document_start'
      }]
    }, {
      hosts: ['ebay.com'],
      scripts: [{
        allFrames: true,
        id: 'ebay.com-customer-script',
        js: ['content/custom-scripts/ebay.com.js'],
        matches: ['*://*.ebay.com/*'],
        runAt: 'document_end'
      }]
    }, {
      hosts: ['elpais.com'],
      scripts: [{
        allFrames: true,
        id: 'elpais.com-customer-script',
        js: ['content/custom-scripts/dependencies/unblock-content-scrolling.js', 'content/custom-scripts/elpais.com.js'],
        matches: ['*://*.elpais.com/*'],
        runAt: 'document_end'
      }]
    }, {
      hosts: ['canalrcn.com'],
      scripts: [{
        allFrames: true,
        id: 'canalrcn.com-customer-script',
        js: ['content/custom-scripts/dependencies/unblock-content-scrolling.js', 'content/custom-scripts/canalrcn.com.js'],
        matches: ['*://*.canalrcn.com/*'],
        runAt: 'document_end'
      }]
    }, {
      hosts: ['eltiempo.com'],
      scripts: [{
        allFrames: true,
        id: 'eltiempo.com-customer-script',
        js: ['content/custom-scripts/dependencies/unblock-content-scrolling.js', 'content/custom-scripts/eltiempo.com.js'],
        matches: ['*://*.eltiempo.com/*'],
        runAt: 'document_end'
      }]
    }];
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
  async updateDynamicRules(sitesData) {
    const hosts = Object.keys(sitesData);
    const addRules = hosts.length ? [{
      id: ALLOWED_RULES_IDS.general,
      priority: 100,
      action: {
        type: 'allow'
      },
      condition: {
        initiatorDomains: hosts
      }
    }] : [];
    await updateDynamicRules({
      removeRuleIds: [1],
      addRules
    });
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
  async isHostDeactivated(host) {
    const data = await this.container.get();
    return data[host];
  }
}
const deactivatedSites = new DeactivatedSites();