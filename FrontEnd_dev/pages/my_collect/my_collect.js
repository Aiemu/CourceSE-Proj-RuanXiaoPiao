// pages/my_collect/my_collect.js
import Dialog from '../../vant-weapp/dialog/dialog'
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    has_activity: true,
    collectlist:[]
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
      url: 'http://62.234.50.47/getStarList/',
      data: postData,
      method: 'POST',
      header: {
        'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
      },
      success: function (res) {
        console.log(res.data)
        var list = res.data.data.activityList
        for (var i = 0; i < list.length; i++) {
          list[i] = JSON.parse(list[i])
        }
        console.log(list)
        if(list.length == 0)
        {
          that.setData({
            collectlist: list,
            has_activity: false
          })
        }
        else
        {
          that.setData({
            collectlist: list,
            has_activity: true
          })
        }
      },
      fail: function (error) {
        console.log(error);
      }
    })
  },

  cancelstar: function(e) {
    var that = this

    Dialog.confirm({
      title: '提示',
      message: '是否要取消收藏',
      width:'700rpx'
    }).then(() => {
      // on confirm
      var postData = {
        openid: app.globalData.openId,
        activity_id: e.currentTarget.dataset.id, 
      }
      wx.request({
        url: 'http://62.234.50.47/deleteStar/',
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
  info: function(e) {
    var tmp = '/pages/activity-details/activity-details?' + 'id=' + e.currentTarget.dataset.id
    wx.navigateTo({
      url: tmp,
    })
  },

})