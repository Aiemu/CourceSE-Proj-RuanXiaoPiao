//app.js
App({
  onLaunch: function(options) {
    this.globalData.openId = wx.getStorageSync('OPENID')
  },

  onShow (options) {
    var extraData = null
    if (options.referrerInfo.extraData) {
      extraData = options.referrerInfo.extraData
      console.log(extraData)
      this.globalData.verifyToken = extraData.token
    }
},
  globalData: {
    openId: null,
    verifyToken: null
  }
})