//富文本转换器
import Dialog from '../../vant-weapp/dialog/dialog';
let WxParse = require('../../wxParse/wxParse.js')


Page({
    data: {
        activityDetail: {},
        collected: true,
    },
    onLoad(e) {
        // e.id位传入的活动id
        this.activityId = e.id
        this.setData({
            activityDetail: this.getActivityDetail()
        })
    },
    getActivityDetail: function () {
        const that = this
        // TODO: 改成服务器请求获取Detail
        that.activityDetail = {
            basicInfo: {
                id: 0,
                image: 'https://img.yzcdn.cn/vant/cat.jpeg',
                title: '软件学院学生节',
                date: '2020.04.20',
                location: '大礼堂',
                sponsor: '软院学生会主办',
                state: 0,
                hot: 500
            },
            content: '<div>富文本商品详情，需要HTML或者Markdown格式</div>'
        }
        WxParse.wxParse('article', 'html', that.activityDetail.content, that, 5);
        return that.activityDetail
    },
    onClickTicketing(e) {
        // 看是否是多长次或需要支付
        // 不是，则直接弹出对话框确认购买
        // 否饿，跳到选择支付页面
        let temp = false
        if (!temp) {
            Dialog.confirm({
                title: '确认抢票',
                message: '确认要抢 ' + this.activityDetail.basicInfo.title + ' 的票吗?'
              }).then(() => {
                // on confirm
                this.buyTicket()
              }).catch(() => {
                // on cancel
              });
        }
        else {

        }
    },
    buyTicket() {
        // TODO: request buy
        wx.navigateTo({
          url: '/pages/buy-ticket/buy-ticket?id=' + this.activityId
        })
    }
})