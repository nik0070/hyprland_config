"use strict";

function setStyle(element, style) {
  for (const key in style) {
    element?.style.setProperty(key, style[key], 'important');
  }
}
function setCustomCssIntoPage(customCss) {
  let styleElement = document.querySelector('#stndz-custom-css');
  if (!styleElement) {
    styleElement = document.createElement('style');
    styleElement.id = 'stndz-custom-css';
    addElementToHead(styleElement);
  }
  styleElement.textContent = customCss || '';
}