"use strict";

const heartbeat = async () => {
  const user = await userData.getData();
  if (user) {
    await serverApi.callUrl({
      url: API_URLS.heartbeat,
      method: 'PUT',
      data: {
        privateUserId: user.privateUserId
      }
    });
  }
};