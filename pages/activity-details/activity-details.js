//富文本转换器
let WxParse = require('../../wxParse/wxParse.js')


Page({
    data: {
        activityDetail: {},
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
    }
})