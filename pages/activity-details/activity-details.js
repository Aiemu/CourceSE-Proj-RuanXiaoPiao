import Dialog from '../../vant-weapp/dialog/dialog'
import Toast from '../../vant-weapp/toast/toast'
//富文本转换器
let WxParse = require('../../wxParse/wxParse.js')


Page({
    data: {
        activityDetail: {},
    },
    onLoad(e) {
        // e.id位传入的活动id
        this.activityId = e.id
        this.getActivityInfo()
        this.getIfCollectThisAct()
    },

    // 获取活动详情
    getActivityInfo: function () {
        const that = this
        var postData = {
            activity_id: this.activityId,
        };
        wx.request({
            url: 'http://62.234.50.47/getActivityInfo/',
            data: postData,
            method: 'POST',
            header: {
                'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
            },
            success: function (res) {
                console.log('getList-OK!');
                console.log(res.data.data);
                that.setData({
                    activityDetail: {
                        basicInfo: res.data.data
                    }
                })
                // content 富文本解析并展示
                // WxParse.wxParse('article', 'html', that.activityDetail.content, that, 5);

            },
            fail: function (error) {
                console.log(error);
            }
        })
    },
    getIfCollectThisAct: function() {
        var that = this
        wx.login({
          success: function (data) {
            var postData = {
              code: data.code,
            };
            wx.request({
              url: 'http://62.234.50.47/getStarList/',
              data: postData,
              method: 'POST',
              header: {
                'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
              },
              success: function (res) {
                var list = res.data.data.activityList
                for (var i = 0; i < list.length; i++) {
                  list[i] = JSON.parse(list[i])
                }
                let actID = that.activityId
                for(let act in list) {
                    act = list[act]
                    if(act.activity_id == actID) {
                        that.setData({
                            collected: true
                        })
                        return
                    }
                }
                that.setData({
                    collected: false
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
    
    tapCollect: function() {
        let that = this
        let ifCollected = that.data.collected
        console.log("ifC:"+ifCollected)
        wx.login({
            success: function (data) {
                console.log('获取 Code：' + data.code)
                var postData = {
                    code: data.code,
                    activity_id: that.activityId,
                }
                let tmpUrl = 'http://62.234.50.47/starActivity/'
                if(ifCollected) {
                    tmpUrl = 'http://62.234.50.47/deleteStar/'
                }
                wx.request({
                    url: tmpUrl,
                    data: postData,
                    method: 'POST',
                    header: {
                        'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
                    },
                    success: function (res) {
                        //回调处理
                        console.log('getOpenID-OK!');
                        console.log(res.data);
                    
                        that.setData({
                            collected: !ifCollected
                        })
                        console.log(that.data.collected)
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
    onClickTicketing(e) {
        // 看是否是多长次或需要支付
        // 不是，则直接弹出对话框确认购买
        // 否饿，跳到选择支付页面
        console.log(this)
        let temp = false
        if (!temp) {
            Dialog.confirm({
                title: '确认抢票',
                message: '确认要抢 ' + this.data.activityDetail.basicInfo.title + ' 的票吗?'
              }).then(() => {
                // on confirm
                this.buyTicket()
              }).catch(() => {
                // on cancel
              });
        }
        else {
            wx.navigateTo({
                url: '/pages/buy-ticket/buy-ticket?id=' + this.activityId
              })      
        }
    },
    buyTicket() {
        let that = this
        wx.login({
            success: function (data) {
                console.log('获取购买 Code：' + data.code)
                var postData = {
                    code: data.code,
                    activity_id: that.activityId
                }
                wx.request({
                    url: 'http://62.234.50.47/purchaseTicket/',
                    data: postData,
                    method: 'POST',
                    header: {
                        'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
                    },
                    success: function (res) {
                        //回调处理
                        console.log('getOpenID-OK!');
                        console.log(res.data);
                        if(res.data.code == "002") {
                            Toast.success('抢票成功!')
                        }
                        else {
                            Toast.fail('票已存在!')
                        }
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
    }
})