"use strict";

{
  const fn = debounce(() => {
    for (const s of ['div.Fgvgjc', 'div.HTjtHe']) {
      document.querySelector(s)?.remove();
    }
    document.body?.classList.remove('EM1Mrb');
  }, 100);
  new MutationObserver(fn).observe(document.documentElement, {
    childList: true,
    subtree: true
  });
}