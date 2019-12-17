Page({
    bindGetOpenID: function (e) {
        console.log(e.detail.rawData);
        wx.login({
            success: function (data) {
                console.log('获取登录 Code：' + data.code)
                var postData = {
                    code: data.code,
                    info: e.detail.rawData,
                };
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

    bindGetTicketList: function (e) {
        console.log(e.detail.rawData);
        wx.login({
            success: function (data) {
                console.log('获取登录 Code：' + data.code)
                var postData = {
                    code: data.code,
                };
                wx.request({
                    url: 'http://62.234.50.47/getTicketList/',
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

    bindGetTicketInfo: function (e) {
        console.log(e.detail.rawData);
        wx.login({
            success: function (data) {
                console.log('获取登录 Code：' + data.code)
                var postData = {
                    code: data.code,
                    ticket_id: 11, // TODO
                };
                wx.request({
                    url: 'http://62.234.50.47/getTicketInfo/',
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

    bindRefundTicket: function (e) {
        console.log(e.detail.rawData);
        wx.login({
            success: function (data) {
                console.log('获取登录 Code：' + data.code)
                var postData = {
                    code: data.code,
                    ticket_id: 11, // TODO
                };
                wx.request({
                    url: 'http://62.234.50.47/refundTicket/',
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

    bindGetStarList: function (e) {
        console.log(e.detail.rawData);
        wx.login({
            success: function (data) {
                console.log('获取登录 Code：' + data.code)
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

    saveTestData: function () {
        var postData = {
            str: 'save test data'
        };
        wx.request({
            url: 'http://62.234.50.47/saveTestData/',
            data: postData,
            method: 'POST',
            header: {
                'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
            },
            success: function (res) {
                console.log('saveTestData-OK!');
                console.log(res.data);
            },
            fail: function (error) {
                console.log(error);
            }
        })
    },

}
)