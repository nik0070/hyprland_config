"use strict";

{
  const fn = debounce(() => {
    document.querySelector(`
div[aria-label="Decline optional cookies"],
div[aria-label="Отклонить необязательные файлы cookie"]
`)?.click();
  }, 100);
  new MutationObserver(fn).observe(document.documentElement, {
    childList: true,
    subtree: true
  });
}