// pages/my_order/my_order.js
import Dialog from '../../vant-weapp/dialog/dialog'
const app = getApp()
Page({
  /**
   * 页面的初始数据
   */
  data: {
    //根据当前的时间去判断活动是否开始
    orderlist:[],
    show: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this
    var postData = {
      openid: app.globalData.openId
    }
    wx.request({
      url: 'http://62.234.50.47/getTicketList/',
      data: postData,
      method: 'POST',
      header: {
        'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
      },
      success: function (res) {
        console.log(res.data)
        var list = res.data.data.ticketList
        for (var i = 0; i < list.length; i++) {
          list[i] = JSON.parse(list[i])
        }
        console.log(list)
        that.setData({
          orderlist: list
        })
      },
      fail: function (error) {
        console.log(error);
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
    var tmp = '/pages/ticket/ticket?' + 'id=' + e.currentTarget.dataset.id
    wx.navigateTo({
      url: tmp,
    })
  },

  refund: function(e) {
    var that = this
    Dialog.confirm({
      title: '提示',
      message: '是否要退票？',
      width: '700rpx'
    }).then(() => {
      // on confirm
      var postData = {
        openid: app.globalData.openId,
        ticket_id: e.currentTarget.dataset.id,
      }
      wx.request({
        url: 'http://62.234.50.47/refundTicket/',
        data: postData,
        method: 'POST',
        header: {
          'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        },
        success: function (res) {
          //回调处理
          console.log('getOpenID-OK!');
          console.log(res.data);
          that.onLoad()
        },
        fail: function (error) {
          console.log(error);
        }
      })
    }).catch(() => {
      // on cancel
    });

  },
  
})