## Tips:
- Aiemu和tuyc17测试时使用的是各自的数据库，因此注意修改settings.py里关于DATABASE的设置。
- 重建数据库打的方法:删除app中migrations下的除_init_.py的所有文件,数据库中清除所有的表(DROP TABLE IF EXIST tablename;),执行migrate,makemigrations,migrate(Tricks:SET FOREIGN_KEY_CHEKCS = 0;最好清空表后回复1)
- 为应对版本兼容性问题，ubuntu服务器上的django倒退至2.2ver，安装了django-crontab。注意：只能在Linux环境下运行。

## Todo List:

backend:
- QRCode的url生成规则
- heat和django-crontab
- ...
- 后续的数值确定与代码整理

frontend:
- sessionid与清华校园身份对接
- ...
- 后续的ui优化

- 更新总github有关开发进度记录

## API Intro
### Part 0
Intro: Function to init  
Num: 1  
List:   
  - init(request)  授权
    ``` python
    '''
    Intro: 
        get openid, add user into database
    Args(request): 
        code(str): used as certificate to get openid
        user_info(str): used to enrich user's info in database
    Returns:    
        {code: 000, msg: 授权成功, data: {jwt(str), openid(str), nickname(str)}}
    '''
    ```
  - verifyUser(request)  认证
    ``` python
    '''
    Intro: 
        update user's is_verified
    Args(request): 
        openid(str): used to identify user
    Returns: 
        {code: 101, msg: 认证失败，该用户不存在, data: {openid(str)}}
        {code: 001, msg: 认证成功, data: {openid(str)}}
    '''
    ```

### Part 1
Intro: Functions to operate activity  
Num: 4  
List:  
  - getActivityList(request)  获取活动列表
    ``` python
    '''
    Intro: 
        return all activities in database
    Args(request): 
        None
    Returns: 
        {code: 010, msg: 获取活动列表成功, data: {activityList(list)}}
    '''
    ```
  - getActivityInfo(request)  获取活动详情
    ``` python 
    '''
    Intro: 
        get the details of an activity with activity_id
    Args(request): 
        activity_id(int): used to identify activity
    Returns: 
        {code: 211, msg: 获取活动详情失败，该活动不存在, data: {activity_id(int)}}
        {code: 011, msg: 活动详情获取成功, data: {activity_id(int), title(str), 
                                            image(str), status(str), remain(int), 
                                            publisher(str), description(str), 
                                            time(date), place(str), price(double), 
                                            heat(double)}}
    '''
    ```
  - getScrollActivity(request)  获取滚图活动
    ``` python
    '''
    Intro: 
        return top 5 activities(rank with heat)
    Args(request): 
        None
    Returns: 
        {code: 012, msg: 获取滚图成功, data: {activityList(list)}}
    '''
    ```
  - searchEngine(request)  搜索
    ``` python 
    '''
    Intro: 
        cut line into words, use words to compare with activitise' info to get suitable activities
    Args(request): 
        line(str): what user typed in edit-line
    Returns: 
        {code: 013, msg: 搜索成功, data: {actList(list)}}
    '''
    ```

### Part 2
Intro: Functions to operate ticket  
Num: 5  
List:   
  - purchaseTicket(request)  购票
    ``` python 
    '''
    Intro: 
        create new ticket and add it into user's ticket list
    Args(request): 
        openid(str): used to identify user, saved in the cache of front-end
        activity_id: used to identify activity
    Returns: 
        {code: 120, msg: 购票失败，该用户不存在, data: {openid(str), activity_id(int)}}
        {code: 120, msg: 购票失败，该用户未认证, data: {openid(str), activity_id(int)}}
        {code: 220, msg: 购票失败，该活动不存在, data: {openid(str), activity_id(int)}}
        {code: 320, msg: 购票失败，余票不足, data: {openid(str), activity_id(int), remain(int)}}
        {code: 320, msg: 购票失败，票已存在, data: {openid(str), activity_id(int), remain(int)}}
        {code: 020, msg: 购票成功, data: {openid(str), activity_id(int), remain(int)}}
    '''
    ```
  - refundTicket(request)  退票
    ``` python
    '''
    Intro: 
        update ticket's is_valid into false
    Args(request): 
        ticket_id(int): used to identify ticket
    Returns: 
        {code: 321, msg: 退票失败，该票不存在, data: {ticket_id(int)}}
        {code: 021, msg: 退票成功, data: {ticket_id(int), is_valid(bool)}}
        {code: 321, msg: 退票失败，该票为已退票状态, data: {ticket_id(int), is_valid(bool)}}
    '''
    ```
  - getTicketList(request)  获取已购票列表
    ``` python 
    '''
    Intro: 
        return user's all tickets, include refunded ones
    Args(request): 
        openid: used to identify user
    Returns: 
        {code: 122, msg: 获取已购票列表失败，该用户不存在, data: {openid(str)}}
        {code: 022, msg: 获取已购票列表成功, data: {openid(str), ticketList(list)}}
    '''
    ```
  - getTicketInfo(request)  获取票的详情
    ``` python 
    '''
    Intro: 
        get ticket's info from database and return
    Args(request): 
        ticket_id(int): used to identify ticket
    Returns: 
        {code: 323, msg: 获取票详情失败，该票不存在, data: {ticket_id(int)}}
        {code: 023, msg: 获取票详情成功, data: {ticket_id(int), owner(str), title(str), 
                                            price(double), place(str), heat(double), 
                                            tic_time(date), act_time(date), is_valid(bool), 
                                            QRCode(image)}}
    '''
    ```
  - checkTicket(request)  检票端检票
    ``` python 
    '''
    Intro: 
        check ticket in check-ticket end
    Args(request): 
        ticket_id(int)
    Returns: 
        {code: 324, msg: 检票失败，该票不存在, data: {ticket_id(int)}}
        {code: 224, msg: 检票失败，该活动已结束, data: {ticket_id(int)}}
        {code: 324, msg: 检票失败，该票已使用, data: {ticket_id(int)}}
        {code: 024, msg: 检票成功, data: {ticket_id(int)}}
    '''
    ```

### Part 3
Intro: Functions to operate star  
Num: 3  
List:  
  - starActivity(request)  收藏
    ``` python 
    '''
    Intro: 
        add activity into user's star list
    Args(request): 
        openid(str): used to identify user
        activity_id(int): used to identify activity
    Returns: 
        {code: 130, msg: 收藏失败，该用户不存在, data: {openid(str), activity_id(int)}}
        {code: 230, msg: 收藏失败，该活动不存在, data: {openid(str), activity_id(int)}}
        {code: 030, msg: 收藏成功, data: {openid(str), activity_id(int)}}
    '''
    ```
  - deleteStar(request)  取消收藏
    ``` python 
    '''
    Intro: 
        delete activity from user's star list
    Args(request): 
        openid(str): used to identify user
        activity_id: used to identify activity
    Returns: 
        {code: 131, msg: 取消收藏失败，该用户不存在, data: {openid(str), activity_id(int)}}
        {code: 231, msg: 取消收藏失败，该活动不存在, data: {openid(str), activity_id(int)}}
        {code: 031, msg: 取消收藏成功, data: {openid(str), activity_id(int)}}
    '''
    ```
  - getStarList(request)  获取收藏列表
    ``` python
    '''
    Intro: 
        return user's star list
    Args(request): 
        openid(str): used to identify user
    Returns: 
        {code: 132, msg: 获取收藏列表失败，该用户不存在, data: {openid(str)}}
        {code: 032, msg: 获取收藏列表成功, data: {activityList(list)}}
    '''
    ```

### Part 4
Intro: Functions to save test data  
Num: 1  
List:   
  - saveTestData(request)  存入测试数据
    ``` python 
    '''
    Intro: 
        save some data into database
    Args(request): 
        None
    Returns: 
        {code: 050, msg: 保存成功, data: {newUser(str), newActivity(list)}}
    '''
    ```

### Part 5
Intro: Function to show page for testing net connect  
Num: 1  
List:   
  - index(request)  测试界面
    ``` python
    '''
    Intro: 
        Used to test net connection
    Args(request): 
        None
    Returns: 
        None
    '''
    ```