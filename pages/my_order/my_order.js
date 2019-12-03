// pages/my_order/my_order.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    //根据当前的时间去判断活动是否开始
    orderlist:[]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this
    wx.login({
      success: function (data) {
        var postData = {
          code: data.code,
        };
        wx.request({
          url: 'http://62.234.50.47/getTicketList/',
          data: postData,
          method: 'POST',
          header: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
          },
          success: function (res) {
            var list = res.data.data.ticketList
            for (var i = 0; i < list.length; i++) {
              list[i] = JSON.parse(list[i])
            }
            that.setData({
              orderlist: list
            })
          },
          fail: function (error) {
            console.log(error);
          }
        })
      },
      fail: function () {
        console('登录获取Code失败！');
      }
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

  info: function(e) {
    var tmp = '../ticket/ticket?' + 'id=' + e.currentTarget.dataset.id
    wx.navigateTo({
      url: tmp,
    })
  },

  refund: function() {
    
  }
})