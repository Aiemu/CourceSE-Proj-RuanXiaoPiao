//app.js
App({
    onLaunch: function () {
      // 登录
      wx.login({
        success: res => {
          if(res.code) {
          // 发送 res.code 到后台换取 openId, sessionKey, unionId
            /*
            wx.request({
  
            })
            */
          }
        } 
      })
    }
  })