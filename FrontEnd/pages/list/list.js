Page({
    getList: function() {
        var postData = {
            str: 'get list'
        };
        wx.request({
            url: 'http://127.0.0.1:8000/getList/',
            data: postData,
            method: 'POST',
            header: {
                'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
            },
            success: function (res) {
                console.log('getList-OK!');
                console.log(res.data);
            },
            fail: function (error) {
                console.log(error);
            }
        })
    },

    purchaseTicket: function(e) {
        console.log(e.detail.rawData);
        wx.login({
            success: function (data) {
                console.log('获取购买 Code：' + data.code)
                var postData = {
                    code: data.code,
                    activity_id: 2, // TODO
                };
                wx.request({
                    url: 'http://127.0.0.1:8000/purchaseTicket/',
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
    }
}
)