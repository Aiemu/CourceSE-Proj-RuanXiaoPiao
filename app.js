//app.js
App({
  onShow (options) {
    var extraData = null
    if (options.referrerInfo.extraData) {
      extraData = options.referrerInfo.extraData
      console.log(extraData)
    }
  }
})