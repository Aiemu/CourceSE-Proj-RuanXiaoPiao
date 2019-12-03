Page({
    data: {
      radio: '1',
      placeList: [],
    },
    onLoad() {
        this.setData({
            placeList: this.getPlaceList()
        })
    },
    onChange(event) {
      console.log(event.detail)
      this.setData({
        radio: event.detail,
      });
    },
  
    onClick(event) {
      const { name } = event.currentTarget.dataset;
      console.log(event.currentTarget)
      this.setData({
        radio: name
      });
    },
    getPlaceList: function() {
        //TODO: 改成服务器请求获地点
        this.placeList = ["大礼堂1", "大礼堂2"]
        return this.placeList
    }
  });