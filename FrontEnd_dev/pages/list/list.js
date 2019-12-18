import Dialog from '../../vant-weapp/dialog/dialog'
const app = getApp()

Page({
    data: {
        ifNeedAuth: false,
        searchbar: {
        },
        activityList: []
    },
    onLoad() {
        if(!app.globalData.openId) {
          this.setData({
            ifNeedAuth: true
          })
        }
        this.getBanners()
        this.getActivityList()
    },
    getUserInfo: function (e) {
      let that = this
      let detail = e.detail.rawData
      wx.login({
        success: res => {
          // 获取到用户的 code 之后：res.code
          console.log("用户的code:" + res.code)
          console.log("用户的Info:" + detail)
            var postData = {
                code: res.code,
                info: detail
            }
            wx.request({
                url: 'http://62.234.50.47/init/',
                data: postData,
                method: 'POST',
                header: {
                    'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
                },
                success: function (res) {
                    //回调处理
                    console.log('getOpenID-OK!');
                    console.log(res.data);
                    // 本地存储openid
                    app.globalData.openId = res.data.data.openid
                    wx.setStorageSync('OPENID', res.data.data.openid)
                    console.log(app.globalData)
                    that.ifNeedAuth = false
                    that.setData({
                      ifNeedAuth: false
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
    getBanners: function () {
      let that = this
      var postData = {
      }
      wx.request({
        url: 'http://62.234.50.47/getScrollActivity/',
        data: postData,
        method: 'POST',
        header: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        },
        success: function (res) {
          let list = res.data.data.activityList
          for (let i = 0; i < list.length; i++) {
              list[i] = JSON.parse(list[i])
              list[i].heat = Math.ceil(list[i].heat)
          }
          that.setData({
            banners: list
          })
        },
        fail: function (error) {
            console.log(error);
        }
    })
    },
    //获取活动列表
    getActivityList: function () {
        let list = []
        let that = this
        var postData = {
            str: 'get list'
        };
        wx.request({
            url: 'http://62.234.50.47/getActivityList/',
            data: postData,
            method: 'POST',
            header: {
                'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
            },
            success: function (res) {
                list = res.data.data.activityList
                for (let i = 0; i < list.length; i++) {
                    list[i] = JSON.parse(list[i])
                    list[i].heat = Math.ceil(list[i].heat)
                }
                that.setData({
                    activityList: list
                })
            },
            fail: function (error) {
                console.log(error);
            }
        })
    },

    toDetailsTap: function(e) {
        wx.navigateTo({
          url: '/pages/activity-details/activity-details?id=' + e.currentTarget.dataset.id
        })
    },
    toSearchTap: function(e) {
        wx.navigateTo({
          url: '/pages/search/search'
        })
    },
}
)