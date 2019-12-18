Page({
    data: {
      value: "",
      activityList: []
    },
    onChange(e) {
      this.setData({
        value: e.detail
      })
    },
  
    onSearch(event) {
      if (this.data.value) {
          var that = this
          var postData = {
              line: this.data.value
          }
          wx.request({
              url: 'http://62.234.50.47/searchEngine/',
              data: postData,
              method: 'POST',
              header: {
                  'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
              },
              success: function (res) {
                  var list = res.data.data.actList
                  for (let i = 0; i < list.length; i++) {
                      list[i] = JSON.parse(list[i])
                  }
                  that.setData({
                      activityList: list,
                      listLen: list.length
                  })
                  console.log(that.data.activityList)
                  
              },
              fail: function (error) {
                  console.log(error);
              }
          })
        }
    },
  
    onCancel() {

    },
    toDetailsTap: function(e) {
      wx.navigateTo({
        url: '/pages/activity-details/activity-details?id=' + e.currentTarget.dataset.id
      })
    }
});
  