import Dialog from '../../vant-weapp/dialog/dialog'
import Toast from '../../vant-weapp/toast/toast'
//富文本转换器
let WxParse = require('../../wxParse/wxParse.js')
let app = getApp()

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
                res.data.data.heat = Math.ceil(res.data.data.heat)
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
        var postData = {
            openid: app.globalData.openId
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
    
    tapCollect: function() {
        let that = this
        let ifCollected = that.data.collected
        console.log("ifC:"+ifCollected)
        var postData = {
            openid: app.globalData.openId,
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
    onShareAppMessage: function (res) {
        if (res.from === 'button') {
        }
        return {
            title: '分享',
            path: '/pages/activity-details/activity-details?id=' + this.activityId,
            success: function (res) {
                console.log('成功', res)
            }
        }
    },
    onClickTicketing(e) {
        let that = this
        if(!app.globalData.verifyToken) {
            Toast.fail('尚未绑定清华账户!')
        }
        else {
            Dialog.confirm({
                title: '确认抢票',
                message: '确认要抢 ' + that.data.activityDetail.basicInfo.title + ' 的票吗?'
                }).then(() => {
                    // on confirm
                    that.buyTicket()
                }).catch(() => {
                    // on cancel
                })
        }
    },
    buyTicket() {
        let that = this
        var postData = {
            openid: app.globalData.openId,
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
                if(res.data.code == "020") {
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
    onClickInspector(e) {
        let that = this
        Dialog.confirm({
            title: '确认申请检票员',
            message: '确认要申请 ' + that.data.activityDetail.basicInfo.title + ' 的检票员吗?'
            }).then(() => {
                // on confirm
                that.applyInspector()
            }).catch(() => {
                // on cancel
            })
    },
    applyInspector() {
        let that = this
        var postData = {
            openid: app.globalData.openId,
            activity_id: Number(that.activityId)
        }
        console.log(postData)
        wx.request({
            url: 'http://62.234.50.47/applyInspector/',
            data: postData,
            method: 'POST',
            header: {
                'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
            },
            success: function (res) {
                //回调处理
                console.log('getOpenID-OK!');
                console.log(res.data);
                if(res.data.code == "030") {
                    Toast.success(res.data.msg)
                }
                else {
                    Toast.fail(res.data.msg)
                }
            },
            fail: function (error) {
                console.log(error);
            }
        })
    },
})