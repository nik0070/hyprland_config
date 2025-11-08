"use strict";

const staticBaseUrl = (() => 'https://static-dev.standsapp.org')();
const API_URLS = {
  log: 'https://prod.standsapp.org/api/v2/events',
  user: 'https://prod.standsapp.org/api/v2/user',
  heartbeat: 'https://prod.standsapp.org/user/heartbeat',
  geo: 'https://prod.standsapp.org/geolookup',
  reportUrl: 'https://thepromise.standsapp.org/convert',
  notifications: 'https://prod.standsapp.org/api/v2/user/notifications/',
  easyList: `${staticBaseUrl}/lists/css-latest`,
  trackersList: `${staticBaseUrl}/lists/trackers-list`
};