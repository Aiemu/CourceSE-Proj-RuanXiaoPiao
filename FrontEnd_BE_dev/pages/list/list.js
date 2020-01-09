Page({
    getActivityList: function() {
        var postData = {
            str: 'get list',
        };
        wx.request({
            // url: 'http://62.234.50.47/getActivityList/',
            url: 'http://62.234.50.47/getActivityList/',
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

<<<<<<< HEAD
=======
    getTimeActivityList: function () {
        var postData = {
            str: 'get list',
        };
        wx.request({
            // url: 'http://62.234.50.47/getActivityList/',
            url: 'http://62.234.50.47/getTimeSortedActivity/',
            data: postData,
            method: 'POST',
            header: {
                'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
            },
            success: function (res) {
                console.log('getTimeList-OK!');
                console.log(res.data);
            },
            fail: function (error) {
                console.log(error);
            }
        })
    },

    getHeatActivityList: function () {
        var postData = {
            str: 'get list',
        };
        wx.request({
            // url: 'http://62.234.50.47/getActivityList/',
            url: 'http://62.234.50.47/getHeatSortedActivity/',
            data: postData,
            method: 'POST',
            header: {
                'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
            },
            success: function (res) {
                console.log('getHeatList-OK!');
                console.log(res.data);
            },
            fail: function (error) {
                console.log(error);
            }
        })
    },

>>>>>>> back-end-dev
    getScrollActivity: function () {
        var postData = {
            str: 'get list'
        };
        wx.request({
            url: 'http://62.234.50.47/getScrollActivity/',
            data: postData,
            method: 'POST',
            header: {
                'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
            },
            success: function (res) {
                console.log('getScroll-OK!');
                console.log(res.data);
            },
            fail: function (error) {
                console.log(error);
            }
        })
    },

    getActivityInfo: function () {
        var postData = {
            activity_id: 2,
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
                    // code: data.code,
                    openid: 'oNEnn5bp28pd7N7RKKLKyu5V8G1w',
                    // openid: 'testOpenid',
                    activity_id: 31, // TODO
                };
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

    starActivity: function (e) {
        console.log(e.detail.rawData);
        wx.login({
            success: function (data) {
                console.log('获取 Code：' + data.code)
                var postData = {
                    // code: data.code,
                    openid: 'oNEnn5bp28pd7N7RKKLKyu5V8G1w',
                    activity_id: 3, // TODO
                };
                wx.request({
                    url: 'http://62.234.50.47/starActivity/',
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

    deleteStar: function (e) {
        console.log(e.detail.rawData);
        wx.login({
            success: function (data) {
                console.log('获取 Code：' + data.code)
                var postData = {
                    // code: data.code,
                    openid: 'oNEnn5bp28pd7N7RKKLKyu5V8G1w',
                    activity_id: 3, // TODO
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

    searchEngine: function () {
        var postData = {
            line: '大礼堂项目部'
        };
        wx.request({
            url: 'http://62.234.50.47/searchEngine/',
            data: postData,
            method: 'POST',
            header: {
                'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
            },
            success: function (res) {
                console.log('search-OK!');
                console.log(res.data);
            },
            fail: function (error) {
                console.log(error);
            }
        })
    },
}
)