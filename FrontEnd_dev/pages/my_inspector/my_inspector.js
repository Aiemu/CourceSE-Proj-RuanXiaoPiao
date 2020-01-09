import Toast from '../../vant-weapp/toast/toast'
import Dialog from '../../vant-weapp/dialog/dialog'
const app = getApp()

Page({
    data: {
        inspectorList: []
    },
    onLoad(e) {
        this.showInspectorList()
    },
    showInspectorList: function(e) {
        console.log("查看检票：")
        let that = this  
        let list = []
        let postData = {
            openid: app.globalData.openId
        }
        wx.request({
            url: 'http://62.234.50.47/showInspectorList/',
            data: postData,
            method: 'POST',
            header: {
                'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
            },
            success: function (res) {
                console.log(res.data.data)
                if(res.data.data.activityList.length == 0) {
                    Dialog.alert({
                        title: '您不是检票员！',
                        message: '不存在的检票员'
                      }).then(() => {
                        // on close
                        let pages = getCurrentPages(); //当前页面
                        let beforePage = pages[pages.length - 2]; //前一页
                        wx.navigateBack({
                        success: function () {
                            beforePage.onLoad(); // 执行前一个页面的onLoad方法
                        }
                        })
                      })
                }
                else {
                    console.log(res.data.data.activityList)
                    list = res.data.data.activityList
                    for (let i = 0; i < list.length; i++) {
                        list[i] = JSON.parse(list[i])
                        list[i].heat = Math.ceil(list[i].heat)
                    }
                    console.log(list)
                    that.setData({
                        inspectorList: list
                    })
                }
            },
            fail: function (error) {
                console.log(error);
            }
        })
    },
    tapQrButton: function(e) {
        let that = this
        let postData = {}
        wx.scanCode({
            success: function(res) {
                let result = res.result
                result = result.match(/\d+/g)
                postData['user_id'] = Number(result[0])
                postData['activity_id'] = Number(result[1])
                console.log(postData)
                wx.request({
                  url: 'http://62.234.50.47/checkTicket/',
                  data: postData,
                  method: 'POST',
                  header: {
                      'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
                  },
                  success: function (res) {
                      console.log('checkTicket-OK!');
                      console.log(res.data);
                      /**  324: 检票失败，该票不存在
                       *   224: 检票失败，该活动已结束
                       *   324: 检票失败，该票已使用
                       *   024: 检票成功
                       */
    
                      if(res.data.code == "024") {
                          //TODO: dialog
                      }
                      else if(res.data.code == "224") {
                          Toast.fail(res.data.msg)
                      }
                      else {
                          let msg = res.data.msg.match(/(?<=，).*/)
                          Toast.fail(msg[0])
                      }
                  },
                  fail: function (error) {
                      console.log(error);
                  }
                })        
            },
            fail: function(error) {
                console.log(error)
            }
        })
      }
})