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
        this.collected = false
        this.setData({
            collected: this.collected
        })
        this.getActivityInfo()
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

    tapCollect: function() {
        let that = this
        wx.login({
            success: function (data) {
                console.log('获取 Code：' + data.code)
                var postData = {
                    code: data.code,
                    activity_id: that.activityId,
                };
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
                        Toast.success('购买成功')
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