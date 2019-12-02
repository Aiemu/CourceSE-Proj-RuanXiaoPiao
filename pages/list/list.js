Page({
    data: {
        searchbar: {
        },
        activityList: []
    },
    onLoad() {
        this.setData({
            search: this.search.bind(this),
            banners: this.getBanners(),
            activityList: this.getActivityList()
        })
    },
    // 获取滑动信息栏图片
    getBanners: function () {
        //TODO: 改成服务器请求获取banner
      this.banners = ["滚图1", "滚图2", "滚图3", "滚图4"]
        return this.banners
    },
    //获取活动列表
    getActivityList: function () {
        //TODO: 改成服务器请求获取活动列表
        this.activityList = [{
            id: 0,
            image: 'https://img.yzcdn.cn/vant/cat.jpeg',
            title: '软件学院学生节',
            date: '2020.04.20',
            location: '大礼堂',
            sponsor: '软院学生会主办',
            state: 0,
            hot: 500
        },
        {
            id: 1,
            image: 'https://img.yzcdn.cn/vant/cat.jpeg',
            title: '软件学院学生节2',
            date: '2020.04.20',
            location: '大礼堂',
            sponsor: '软院学生会主办',
            state: 0,
            hot: 500
        },
    ]
        return this.activityList
    },
    search: function (value) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve([{text: '搜索结果', value: 1}, {text: '搜索结果2', value: 2}])
            }, 200)
        })
    },

    toDetailsTap: function(e) {
        wx.navigateTo({
          url: '/pages/activity-details/activity-details?id=' + e.currentTarget.dataset.id
        })
    },
}
)