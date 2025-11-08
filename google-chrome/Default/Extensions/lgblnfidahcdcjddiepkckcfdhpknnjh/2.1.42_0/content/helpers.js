"use strict";

function addElementToHead(element) {
  if (document.head) {
    document.head.insertBefore(element, document.head.firstChild);
  } else {
    window.setTimeout(() => {
      addElementToHead(element);
    }, 10);
  }
}
function getAllShadowDomNodes() {
  const shadowNodes = [];
  const getAllNodes = node => {
    if (node?.shadowRoot) {
      shadowNodes.push(node);
    }
    if (node?.children) {
      for (const child of node.children) {
        getAllNodes(child);
      }
      if (node.shadowRoot) {
        getAllNodes(node.shadowRoot);
      }
    }
  };
  getAllNodes(document.body);
  return shadowNodes;
}