import Dialog from '../../vant-weapp/dialog/dialog'

Page({
    data: {
        searchbar: {
        },
        activityList: []
    },
    onLoad() {
        this.setData({
            ifNeedAuth: false,
            banners: this.getBanners(),
        })
        this.getActivityList()
        let that = this
        // // 查看是否授权
        // wx.getSetting({
        //     success: function (res) {
        //         console.log(res.authSetting)
        //       if (res.authSetting['scope.userInfo']) {
        //         wx.getUserInfo({
        //           success: function (res) {
        //             // 用户已经授权过,不需要显示授权页面,所以不需要改变 isHide 的值
        //             // 根据自己的需求有其他操作再补充
        //             // 我这里实现的是在用户授权成功后，调用微信的 wx.login 接口，从而获取code
        //             wx.login({
        //               success: res => {
        //                 // 获取到用户的 code 之后：res.code
        //                 console.log("用户的code:" + res.code)
        //                   var postData = {
        //                       code: res.code,
        //                       // TODO： 传下面的
        //                       info: e.detail.rawData,
        //                   };
        //                   wx.request({
        //                       url: 'http://62.234.50.47/init/',
        //                       data: postData,
        //                       method: 'POST',
        //                       header: {
        //                           'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        //                       },
        //                       success: function (res) {
        //                           //回调处理
        //                           console.log('getOpenID-OK!');
        //                           console.log(res.data);
        //                       },
        //                       fail: function (error) {
        //                           console.log(error);
        //                       }
        //                   })
        //               },
        //               fail: function () {
        //                   console('登录获取Code失败！');
        //               }
        //             }) // login
        //           }
        //         })
        //       } else {
        //         // 用户没有授权
        //         that.setData({
        //           ifNeedAuth: true
        //         })
        //       }
        //     }

        // })
    },
    onReady() {
        if (this.ifNeedAuth) {
            Dialog.confirm({
                title: '软小票申请获取以下权限',
                message: '获得你的公开信息(昵称，头像等)'
              }).then(() => {
                // on confirm
                this.getUserInfo()
              }).catch(() => {
                // on cancel
                console.log("取消")
              })
        }
    },
    getUserInfo: function (e) {
        if (e.detail.userInfo) {
          //用户按了允许授权按钮
          var that = this;
          // 获取到用户的信息了，打印到控制台上看下
          console.log("用户的信息如下：");
          console.log(e.detail.userInfo);
          //授权成功后,通过改变 isHide 的值，让实现页面显示出来，把授权页面隐藏起来
          that.setData({
            isHide: false
          });
        } else {
          //用户按了拒绝按钮
          wx.showModal({
            title: '警告',
            content: '您点击了拒绝授权，将无法进入小程序，请授权之后再进入!!!',
            showCancel: false,
            confirmText: '返回授权',
            success: function (res) {
              // 用户没有授权成功，不需要改变 isHide 的值
              if (res.confirm) {
                console.log('用户点击了“返回授权”');
              }
            }
          })
        }
    },
    getBanners: function () {
        //TODO: 改成服务器请求获取banner
      this.banners = ["滚图1", "滚图2", "滚图3", "滚图4"]
        return this.banners
    },
    //获取活动列表
    getActivityList: function () {
        // //TODO: 改成服务器请求获取活动列表
        // this.activityList = [{
        //     id: 0,
        //     image: 'https://img.yzcdn.cn/vant/cat.jpeg',
        //     title: '软件学院学生节',
        //     date: '2020.04.20',
        //     location: '大礼堂',
        //     sponsor: '软院学生会主办',
        //     state: 0,
        //     hot: 500
        // },
        // {
        //     id: 1,
        //     image: 'https://img.yzcdn.cn/vant/cat.jpeg',
        //     title: '软件学院学生节2',
        //     date: '2020.04.20',
        //     location: '大礼堂',
        //     sponsor: '软院学生会主办',
        //     state: 0,
        //     hot: 500
        // },]
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