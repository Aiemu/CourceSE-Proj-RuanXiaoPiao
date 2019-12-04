// pages/home/home.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    is_verify: true,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    //从后端抓取用户基本信息
    this.setData({
      
    })
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