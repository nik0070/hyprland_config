"use strict";

const skipIGStoriesAds = debounce(() => {
  const stories = document.querySelectorAll('div[style*="transform: translateX(calc(-50%"]');
  for (let i = 0; i < stories.length - 1; i++) {
    if (stories[i].clientHeight === 0) {
      const storyButtons = stories[i].querySelectorAll('div[role="button"]');
      const nextStoryButton = storyButtons[storyButtons.length - 1];
      nextStoryButton?.click();
    }
  }
}, 500);
new MutationObserver(skipIGStoriesAds).observe(document.documentElement, {
  childList: true,
  subtree: true
});
blockMetaFeedAds('article>div');