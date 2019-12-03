// pages/ticket/ticket.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    info: {},
    is_refund: true,
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
          ticket_id: options.id
        };
        wx.request({
          url: 'http://62.234.50.47/getTicketInfo/',
          data: postData,
          method: 'POST',
          header: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
          },
          success: function (res) {
            //回调处理
            that.setData({
              info: res.data.data
            })
            console.log(that.data.info)
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

  }
})