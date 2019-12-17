// pages/home/home.js
const app = getApp()
Page({
  /**
   * 页面的初始数据
   */
  data: {
    is_verify: false,
    post_verify_flag: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    console.log(app.globalData.verifyToken)
    if(app.globalData.verifyToken) {
      this.setData({
        is_verify: true
      })
      // 如果前端已认证，但还没发送给后端
      if(!this.post_verify_flag) {
        var that = this
        var postData = {
          openid: app.globalData.openId
        }  
        console.log(postData)
        wx.request({
          url: 'http://62.234.50.47/verifyUser/',
          data: postData,
          method: 'POST',
          header: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
          },
          success: function (res) {
            console.log(res.data)
            that.post_verify_flag = true
            that.setData({
              post_verify_flag: true
            })
          },
          fail: function (error) {
            console.log(error);
          }
        })
    
      }
    }
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },

  //自定义信号
  myOrder: function(){
    wx.navigateTo({
      url: '../my_order/my_order',
    })
  },

  myCollect: function(){
    wx.navigateTo({
      url: '../my_collect/my_collect',
    })
  },

  myProfile: function(){
    wx.navigateTo({
      url: '../profile/profile',
    })
  },

  verify: function() {
    wx.navigateToMiniProgram({
      "appId": "wx1ebe3b2266f4afe0", 
      "path": "pages/index/index", 
      "envVersion": "trial",
      "extraData": { 
        "origin": "miniapp",
        "type": "id.tsinghua" 
        }
    })
  }
})