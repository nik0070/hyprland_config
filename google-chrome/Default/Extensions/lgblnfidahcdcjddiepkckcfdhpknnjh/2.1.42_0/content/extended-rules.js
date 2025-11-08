"use strict";

class ExtendedRules {
  rules = [];
  blockType;
  attribute;
  styleElementId;
  observer = null;
  hiddenNodes = new WeakSet();
  constructor(blockType) {
    this.blockType = blockType;
    this.attribute = `data-stndz-hidden-${blockType}`;
    this.styleElementId = `stndz-extended-rules-${blockType}`;
  }
  findClosingParen(str, start) {
    let depth = 1;
    for (let i = start; i < str.length; i++) {
      if (str[i] === '(') {
        depth++;
      }
      if (str[i] === ')') {
        depth--;
        if (depth === 0) {
          return i;
        }
      }
    }
    return -1;
  }
  parse(rule) {
    let pos = 0;
    const selectors = [];
    let currentSelector = null;
    while (pos < rule.length) {
      let index = rule.indexOf(':has(', pos);
      const abpIndex = rule.indexOf(':-abp', pos);
      if (abpIndex !== -1 && (index === -1 || abpIndex < index)) {
        index = abpIndex;
      }
      if (index === -1) {
        const selector = rule.slice(pos).trim();
        if (selector) {
          selectors.push({
            selector
          });
        }
        break;
      }
      const baseSelector = rule.slice(pos, index).trim();
      if (baseSelector || !currentSelector) {
        currentSelector = {
          selector: baseSelector
        };
        selectors.push(currentSelector);
      }
      let type = '';
      if (rule.startsWith(':-abp-has', index) || rule.startsWith(':has(', index)) {
        type = 'has';
      } else if (rule.startsWith(':-abp-contains', index)) {
        type = 'contains';
      } else {
        debug.error('Unknown rule type');
        return [];
      }
      const start = index + rule.slice(index, rule.indexOf('(', index) + 1).length;
      const end = this.findClosingParen(rule, start);
      if (end === -1) {
        debug.error('Mismatched parentheses in rule');
        return [];
      }
      const content = rule.slice(start, end).trim();
      if (type === 'has') {
        const nestedHas = this.parse(content);
        if (!currentSelector.has) {
          currentSelector.has = [];
        }
        currentSelector.has.push(...nestedHas);
      } else if (type === 'contains') {
        currentSelector.text = content;
      }
      pos = end + 1;
    }
    return selectors;
  }
  findNodesByRule(rules, root = document.body) {
    const result = [];
    for (const rule of rules) {
      try {
        const matchedNodes = Array.from(root.querySelectorAll(rule.selector)).filter(node => {
          if (this.hiddenNodes.has(node)) {
            return false;
          }
          if (rule.has) {
            return this.findNodesByRule(rule.has, node).length > 0;
          }
          if (rule.text) {
            if (rule.text.includes('|')) {
              let inclusion = false;
              const textVariants = rule.text.split('|');
              for (const text of textVariants) {
                if (text.startsWith('/')) {
                  inclusion = node.textContent?.includes(text.substring(1)) ?? false;
                } else if (text.endsWith('/')) {
                  inclusion = node.textContent?.includes(text.substring(0, text.length - 1)) ?? false;
                } else {
                  inclusion = node.textContent?.includes(text) ?? false;
                }
                if (inclusion) {
                  break;
                }
              }
              return inclusion;
            }
            return node.textContent?.includes(rule.text);
          }
          return true;
        });
        result.push(...matchedNodes);
      } catch (e) {
        debug.error('Error in findNodesByRule', e);
      }
    }
    return result;
  }
  applyAll() {
    let amount = 0;
    for (const rule of this.rules) {
      try {
        for (const node of this.findNodesByRule(rule)) {
          if (!this.hiddenNodes.has(node)) {
            node.setAttribute(this.attribute, 'true');
            this.hiddenNodes.add(node);
            amount += 1;
          }
        }
      } catch (e) {
        debug.error('Error in applyExtendedRules', e);
      }
    }
    this.updateStatistics(amount);
  }
  handleMutations = mutations => {
    const addedRoots = new Set();
    for (const mutation of mutations) {
      if (mutation.type === 'childList') {
        for (const node of mutation.addedNodes) {
          if (node.nodeType === Node.ELEMENT_NODE) {
            addedRoots.add(node);
          }
        }
      }
    }
    if (addedRoots.size > 0) {
      this.applyToAddedNodes(Array.from(addedRoots));
    }
  };
  applyToAddedNodes(addedElements) {
    for (const rule of this.rules) {
      try {
        for (const root of addedElements) {
          for (const node of this.findNodesByRule(rule, root)) {
            if (!this.hiddenNodes.has(node)) {
              node.setAttribute(this.attribute, 'true');
              this.hiddenNodes.add(node);
            }
          }
        }
      } catch (e) {
        debug.error('Error in applyToAddedNodes', e);
      }
    }
    this.updateStatistics(0);
  }
  updateStatistics(amount) {
    if (amount > 0) {
      sendMessage({
        type: MESSAGE_TYPES.updateStatistics,
        payload: {
          typeId: this.blockType,
          amount
        }
      });
    }
  }
  start() {
    const styleElement = currentDocument.createElement('style');
    styleElement.id = this.styleElementId;
    styleElement.textContent = `[${this.attribute}="true"] ${BLOCK_CSS_VALUE}`;
    addElementToHead(styleElement);
    this.applyAll();
    this.observer?.disconnect();
    const debouncedHandler = debounce(this.handleMutations, 100);
    this.observer = new MutationObserver(debounce(debouncedHandler, 100));
    this.observer.observe(document.documentElement, {
      childList: true,
      subtree: true
    });
  }
  stop() {
    currentDocument.querySelector(`style[id="${this.styleElementId}"]`)?.remove();
    this.observer?.disconnect();
    this.observer = null;
  }
  setState(state) {
    if (state) {
      this.start();
    } else {
      this.stop();
    }
  }
  setRules(rules) {
    this.rules = rules.map(rule => this.parse(rule));
  }
}