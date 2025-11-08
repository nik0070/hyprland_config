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
      } else if (str[i] === ')') {
        depth--;
        if (depth === 0) {
          return i;
        }
      }
    }
    return -1;
  }
  hasExtendedPseudoClass(str) {
    return str.includes(':has(') || str.includes(':-abp-has(') || str.includes(':-abp-contains(');
  }
  parse(rule) {
    let pos = 0;
    const result = [];
    let baseSelector = '';
    let currentRule = null;
    while (pos < rule.length) {
      const notIndex = rule.indexOf(':not(', pos);
      const hasIndex = rule.indexOf(':has(', pos);
      const abpHasIndex = rule.indexOf(':-abp-has(', pos);
      const abpContainsIndex = rule.indexOf(':-abp-contains(', pos);
      const indices = [{
        index: notIndex,
        type: 'not',
        offset: 5
      }, {
        index: hasIndex,
        type: 'has',
        offset: 5
      }, {
        index: abpHasIndex,
        type: 'abp-has',
        offset: 10
      }, {
        index: abpContainsIndex,
        type: 'abp-contains',
        offset: 15
      }].filter(i => i.index !== -1);
      if (!indices.length) {
        baseSelector += rule.substring(pos);
        break;
      }
      indices.sort((a, b) => a.index - b.index);
      const {
        index,
        type,
        offset
      } = indices[0];
      baseSelector += rule.substring(pos, index);
      const contentStart = index + offset;
      const contentEnd = this.findClosingParen(rule, contentStart);
      if (contentEnd === -1) {
        debug.error('Mismatched parentheses:', rule);
        return [];
      }
      const content = rule.substring(contentStart, contentEnd);
      if (type === 'not') {
        if (this.hasExtendedPseudoClass(content)) {
          if (!currentRule) {
            currentRule = {
              selector: baseSelector
            };
            result.push(currentRule);
          }
          const notContent = this.parse(content);
          if (notContent.length > 0) {
            if (!currentRule.not) {
              currentRule.not = [];
            }
            currentRule.not.push(...notContent);
          }
        } else {
          baseSelector += `:not(${content})`;
        }
      } else if (type === 'has' || type === 'abp-has') {
        if (!currentRule) {
          currentRule = {
            selector: baseSelector
          };
          result.push(currentRule);
        }
        const hasRules = this.parse(content);
        if (hasRules.length > 0) {
          if (!currentRule.has) {
            currentRule.has = [];
          }
          currentRule.has.push(...hasRules);
        }
      } else if (type === 'abp-contains') {
        if (!currentRule) {
          currentRule = {
            selector: baseSelector
          };
          result.push(currentRule);
        }
        currentRule.text = content;
      }
      pos = contentEnd + 1;
    }
    if (baseSelector && !currentRule) {
      result.push({
        selector: baseSelector.trim()
      });
    } else if (baseSelector && currentRule) {
      currentRule.selector = baseSelector.trim();
    }
    return result;
  }
  findNodesByRule(rules, root = document.body) {
    const result = [];
    for (const rule of rules) {
      try {
        if (!rule.selector.trim()) {
          const rootAsArray = root instanceof HTMLElement ? [root] : [];
          if (rootAsArray.length && this.elementMatchesConditions(rootAsArray[0], rule)) {
            if (root instanceof HTMLElement && !this.hiddenNodes.has(root)) {
              result.push(root);
            }
          }
          continue;
        }
        let candidates;
        try {
          candidates = Array.from(root.querySelectorAll(rule.selector)).filter(node => !this.hiddenNodes.has(node));
        } catch (e) {
          debug.error('Invalid selector in findNodesByRule:', rule.selector, e);
          continue;
        }
        if (!candidates.length) {
          continue;
        }
        const filtered = candidates.filter(node => this.elementMatchesConditions(node, rule));
        result.push(...filtered);
      } catch (e) {
        debug.error('Error in findNodesByRule', e, rule);
      }
    }
    return result;
  }
  elementMatchesConditions(element, rule) {
    if (rule.not && rule.not.length) {
      for (const notRule of rule.not) {
        if (!notRule.selector.trim() && notRule.has) {
          let hasMatch = false;
          for (const hasRule of notRule.has) {
            if (this.findNodesByRule([hasRule], element).length > 0) {
              hasMatch = true;
              break;
            }
          }
          if (hasMatch) {
            return false;
          }
        } else if (this.findNodesByRule([notRule], element).length > 0) {
          return false;
        }
      }
    }
    if (rule.has && rule.has.length) {
      let hasAnyMatch = false;
      for (const hasRule of rule.has) {
        if (this.findNodesByRule([hasRule], element).length > 0) {
          hasAnyMatch = true;
          break;
        }
      }
      if (!hasAnyMatch) {
        return false;
      }
    }
    if (rule.text) {
      return this.checkTextContent(element, rule.text);
    }
    return true;
  }
  checkTextContent(element, textCondition) {
    const nodeText = element.textContent || '';
    if (textCondition.includes('|')) {
      const textParts = textCondition.split('|');
      for (const part of textParts) {
        const trimmedText = part.trim();
        if (trimmedText.startsWith('/') && nodeText.includes(trimmedText.substring(1))) {
          return true;
        } else if (trimmedText.endsWith('/') && nodeText.includes(trimmedText.substring(0, trimmedText.length - 1))) {
          return true;
        } else if (nodeText.includes(trimmedText)) {
          return true;
        }
      }
      return false;
    }
    return nodeText.includes(textCondition);
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
    if (!this.rules.length) {
      return;
    }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', this.start.bind(this));
      return;
    }
    const styleElement = currentDocument.createElement('style');
    styleElement.id = this.styleElementId;
    styleElement.textContent = `[${this.attribute}="true"] ${BLOCK_CSS_VALUE}`;
    addElementToHead(styleElement);
    this.applyAll();
    this.observer?.disconnect();
    const debouncedHandler = debounce(this.applyAll.bind(this), 100);
    this.observer = new MutationObserver(debouncedHandler);
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