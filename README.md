# 软小票交付文档
   * [软小票交付文档](#软小票交付文档)
      * [成员](#成员)
      * [产品目标](#产品目标)
      * [交付产品](#交付产品)
         * [服务器IP](#服务器ip)
         * [小程序码](#小程序码)
         * [管理员账号和密码](#管理员账号和密码)
      * [开发组织管理](#开发组织管理)
         * [过程管理](#过程管理)
         * [人员分工](#人员分工)
         * [开发环境](#开发环境)
         * [配置管理](#配置管理)
      * [系统设计](#系统设计)
         * [前端交互](#前端交互)
         * [后端模块](#后端模块)
         * [接口规范](#接口规范)
         * [数据库设计](#数据库设计)
      * [重难点及其解决](#重难点及其解决)
      * [测试总结](#测试总结)
      * [系统部署](#系统部署)
      
## 成员
涂亦驰 201701****  
邓博文 201701****  
朴铤浚 201508****   
曾正 201701****  

## 产品目标
- 为校园活动主办方提供方便公开的活动信息发布宣传平台
- 方便学生直观地了解到近期感兴趣的活动并抢购活动票
- 有利于校方进行活动管理

## 交付产品
### 服务器IP(已失效)
`IP: 62.234.50.47`

### 小程序码(已失效)
<img src=https://tva1.sinaimg.cn/large/006tNbRwly1gaqm77kda5j30d40d4mx1.jpg width=150>

### 管理员账号和密码(已失效)
账号: `superuser`  
密码: `dptzdptz`

## 开发组织管理
### 过程管理
- 使用Git进行代码版本管理（[Github仓库](https://github.com/Aiemu/CourceSE-Proj-RuanXiaoPaio)）
- 采用敏捷开发方法指导开发过程，使用Github进行辅助管理
- 每周为一个迭代周期，每周六，小组成员在608自习室进行集体开发，或是在图书馆团体研讨间举行周例会以总结上两周的成果并准备下两周的任务目标。除此之外，团队成员在微信群中保持紧密联系，利用闲暇时间开发，遇到问题或者需要合作时都能及时交流。在这样的节奏下，团队大概每两周达成一次Github Milestone
- 关于当前周次的任务，有团队成员提出新的问题或思路时，在经由全体成员充分讨论并得出结论后，组长会在微信群中发布文件并分配此次迭代的任务及分工（开发中后期转为使用Github Issue）。每个人在完成自己的当次分工之后，都会及时与其他组员对接并更新至Github上

### 人员分工
- 前端
  - 邓博文：实现个人主页的用户界面搭建，负责用户学生身份认证的跳转，完善优化了前端的界面显示  
  - 朴铤浚：实现小程序首页(活动展示页面)、活动详情页面及部分个人页面的用户界面搭建。完善了滚图显示和前端检票功能。负责与后端对接和交流的工作 

- 后端
  - 涂亦驰：完成models设计，确定票据二维码的生成规范，实现活动缩略图、票据二维码的图片静态文件功能，实现活动热度计算推荐算法和检票系统  
  - 曾正：后端response结构与状态码设计，实现后端与用户、活动、收藏、及部分票相关的函数，实现分词搜索算法，完成后端单元测试、基础性能测试、测试用前端，服务器部署配置  

### 开发环境
- 前端  
  - Windows 10 / MacOS Catalina
  - vant-weapp 1.0.3
  - Node.js 10.16.0
  - 微信开发者工具1.02
  - 调试基础库2.9.4

- 后端  
  - Windows 10 / MacOS Catalina
  - Django 2.2.4
  - Python 3.7
  - MySQL 8.0.18
  - nginx 1.14.0 (Ubuntu)
  - VS Code 1.41.1

### 配置管理
| 分支名称 | 生命周期 | 远程/本地 | 合并去向 | 功能 |
| --- | --- | --- | --- | --- |
| master | infinite | 远程 | * | 主分支 |
| back_end_dev | limited | 远程 | master | 后端更新与测试 |
| front_end_dev | limited | 远程 | master | 前端更新与测试 |
| userUI | limited | 远程 | front_end_dev | 用户个人界面的更新与测试 |
| merge_check_ticket | limited | 远程 | back_end_dev | 检票功能的更新与测试 |

## 系统设计
### 前端交互
1. 首页  
   - 从上到下分别是搜索框，滚动条，排序方式选择，活动列表  
   - 搜索框中输入搜索内容返回搜索结果总数和搜索出来的活动列表  
   - 滚动条实时滚动播放目前最火的活动的缩略图  
   - 可以选择不排序或者按照热度或者按照时间排序  
   - 活动列表列出了当前所有活动，并在列表项中展示了核心信息  
   - 点击活动列表项则进入详情页，详情页详细展示活动的具体情况，并设有分享，收藏，购票与申请检票员四个按钮，收藏和购票后可以在用户主页中查看，申请检票员在后端审核成功后可进入用户主页的检票员入口  

2. 用户主页  
   - 从上到下分别是用户信息展示与检票员入口，收藏夹，所购票，认证按钮  
   - 用户信息展示中头像和昵称来源于用户的微信头像和昵称，并显示当前用户是否已经认证  
   - 点击我的收藏显示收藏的活动的列表，列表项显示核心信息，点击列表项进入详情页，详情页同时提供取消收藏的功能  
   - 点击我的购票显示已购票的活动的列表，列表项提供核心信息和退票按钮，点击列表项进入票的详情页，票的详情页展示票的二维码和购票的具体时间等信息  
   - 点击认证转到认证界面通过认证后回到小程序并修改用户信息的认证信息并隐藏认证按钮  
   - 点击检票员入口进入检票页面，若无检票活动则提示并回退，否则有个扫码按钮和所管理的检票活动列表  

### 后端模块
后端采用`Django + MySQL`进行设计开发。  
根据接口功能总共分为**8**大模块，各模块又分为数个小模块。  
介绍如下（各接口详细的Args、Returns见文档`BackEnd_API.md`：
1. Init  
   Intro: 包含与用户登录及认证相关的接口函数  
   List: 
    ``` python
    def init(request): 
    '''
    用于用户在首次登录时认证
    '''
    def verifyUser(request): 
    '''
    用于用户的身份认证，即学号认证
    ```
2. Activity  
   Intro: 包含有关活动各种操作的接口函数
   List: 
    ``` python
    def getActivityList(request): 
    '''
    获取已有的活动列表（每一活动包含简单的信息），用于显示在首页界面
    '''
    def getActivityInfo(request): 
    '''
    获取该活动的详细信息（包括活动名，地点，时间等可公开的活动信息）
    '''
    def getScrollActivity(request): 
    '''
    获取最热门的5个未结束的活动，用于显示在首页的滚动条上（总活动数不足
    5个时则返回所有活动）
    '''
    def searchEngine(request): 
    '''
    根据用户输入的内容，应用分词搜索所有活动的信息（标题、地点、主办
    方、简介等），并返回能够匹配的活动列表
    '''
    def getTimeSortedActivity(request): 
    '''
    用于返回按时间排序的未结束的活动列表
    '''
    def getHeatSortedActivity(request): 
    '''
    用于返回按热度排序的未结束的活动列表
    '''
    def addActivity(request): 
    '''
    用于添加新的活动
    '''
    ```
3. Ticket  
   Intro: 包含有关票的各种操作的接口函数
   List: 
    ``` python
    def purchaseTicket(request): 
    '''
    用户购票接口，包括用户身份检查、活动检查、重复购票检查等，完成检查
    后生成一张新的票
    '''
    def refundTicket(request): 
    '''
    用户退票接口，包括用户身份检查、活动检查、重复退票检查等，完成检查
    后将票的 is_valid 属性置为False（为维护用户购票的记录不采用删除
    票的方式），表示该票已被退
    '''
    def getTicketList(request): 
    '''
    获取用户拥有的票的列表，包括已使用票、已退票
    '''
    def getTicketInfo(request): 
    '''
    获取该票的详情
    '''
    ```
4. Star  
   Intro: 包含有关收藏的各种操作的接口函数
   List: 
    ``` python
    def starActivity(request):
    '''
    用户收藏活动的接口，将活动添加到用户的收藏列表
    '''
    def deleteStar(request): 
    '''
    用户取消收藏的接口，将活动从用户的收藏的收藏列表中删除
    '''
    def getStarList(request): 
    '''
    获取该用户的收藏列表
    '''
    ```
5. Save test data  
   Intro: 包括有关向数据库中添加测试数据的接口函数
   List: 
    ``` python
    def saveTestData(request): 
    '''
    向数据库中添加初始测试数据
    '''
    ```
6. Index  
   Intro: 包含用于测试服务器启动状态的接口函数
   List: 
    ``` python
    def index(request): 
    '''
    用于快速测试服务器的启动情况
    '''
    ```
7. Inspector & admin control  
   Intro: 与检票、检票员、管理员有关的函数接口
   List: 
    ``` python
    def applyInspector(request): 
    '''
    发送用户对成为活动检票员的申请
    '''
    def showAllApply(request): 
    '''
    管理员确认接收到的用户申请记录
    '''
    def showApplyList(request): 
    '''
    用户查看自己发出的活动检票员申请记录
    '''
    def showInspectorList(request): 
    '''
    用户确认自己的活动检票员身份
    '''
    def checkTicket(request): 
    '''
    检票员入口扫描票据二维码的处理函数
    '''
    ```
8. Admin
   Intro: 用于管理端的启动

### 接口规范
1. 前端 --> 后端（`Requests`）
    前端向后端接口发送的请求中包含用于确认对象的信息，有以下5种类型：
    - `code`: 由微信服务器生成，发送给后端用于获取用户信息
    - `openid`: 用于确认用户
    - `student_id`: 用于用户认证，为用户对象的一个属性
    - `activity_id`: 用于确认活动
    - `ticket_id`: 用于确认票

2. 后端 --> 前端（`Responses`）
    后端向前端发送的响应包含三部分：
    - `code`: 描述此次响应状态的参数  
    `code`（状态码）的设计方式如下：  
    状态码共**三位**，形如：`000`，`001`  
    首位：状态描述，0为成功，1为用户异常，2为活动异常，3为票异常，4为其他异常  
    第二位：模块序号标记，标明当前为哪一个大模块  
    末位：模块中的函数序号，标明为模块中的哪一个函数  
    - `msg`: 详细说明此次描述的状态，成功或错误信息
    - `data`: 如响应成功且正确为前端向后端请求的所有数据，否则为前端确认发送数据是否有误的确认数据

### 数据库设计
数据库采用`MySQL`。  
数据库共包含为**4**张表，如下：
- `Activity`: 用于存放所有活动信息的表，包含`activity_id`、`title`、`image`等与活动信息相关的列。其中`activity_id`为主键
- `User`: 用于存放所有用户信息的表，包含`openid`、`username`、`student_id`等用户信息。其中`user_id`为主键。`User`中有两个多对多表(`ManyToManyField`)，一个用于实现用户的收藏列表，一个用于实现用户的可检票活动的列表
- `Ticket`: 用于存放所有票的信息的表，包含`ticket_id`、`is_valid`等票的信息，其中`ticket_id`为主键。`Ticket`中有两个外键(`ForeignKey`)，分别用于标明该票的所有者以及对应的活动
- `User_starred`: 由系统自动生成来存放用户收藏列表的表，是一个多对多表

## 重难点及其解决
- 前端
  1. 小程序每个页面有很多生命周期函数，在写逻辑的时候需要仔细考虑应该在页面的那个周期中写逻辑，并且整个小程序本身也有生命周期当涉及到小程序跳转的时候也要考虑应该在什么时候实现跳转和返回数据的获取。
  2. 在样式中熟练地使用`flex`能排版出比较好看的布局
  3. 后端返回的数据是`string`格式，将`string`格式转换成`json`格式小程序才能正常操作。
  4. 微信认证部分，说以前小程序可以一开始就弹出微信认证，现在必须得绑定在一个按钮上，为了这个而新建一个page感觉到很多余，然后就发现vant组件的弹窗里的按钮上可以绑定按钮事件，这就在比起开始进入一个界面，用弹窗更干净了。
  5. 其实比起写代码，时间更多花在与后端队友们的交流上了，为了之后不出奇怪的问题，感到提前交流好非常重要，还好这方面所有组员们都很积极。

- 后端
  1. model的设计存在较大的困难。  
      为解决多对多、一对多的属性，需要用到`ManyToManyField`、`ForeignKey`，其理解使用与管理有一定困难。
  2. 服务器部署困难。  
      服务器在配置时使用`NGINX`，其使用不熟悉。服务器的`Django`版本与本地不一致，导致许多本地未出现的报错，直接在服务器修改代码不方便导致服务器配置初期出现了大量的`commit`

## 测试总结
- 后端
  1. 单元测试（`Unit Test`）  
    原理：为后端所有模块中的接口函数编写了单元测试。测错方向包括用户错误、活动错误、票错误等。  
    测试方法：使用Django自带的单元测试模块编写测试代码。使用`coverage`计算覆盖率，使用`pip3 install coverage`安装  
    - 单元测试结果如下：  
    <img src=https://tva1.sinaimg.cn/large/006tNbRwly1gaqmkixbchj312i0d6dl9.jpg width=500>  
    
    - 覆盖率计算结果如下：  
    <img src=https://tva1.sinaimg.cn/large/006tNbRwly1gaql6uak1gj30uy0twaoo.jpg width=500>

  2. 服务器响应性能测试  
    原理：循环向服务器发送请求，计算时间。  
    测试方法：使用脚本`PerformanceTest.py`  
    测试结果如下：  
    <img src=https://tva1.sinaimg.cn/large/006tNbRwly1gaqlp0ed4bj30pi0ca7bf.jpg width=500>
    看见服务器基本能够保持`40requests/s`的请求处理速度，但会偶尔出现不稳定的情况，平均请求处理速度约为`24.7requests/s`

  3. 基础功能测试
    原理：在开发初期由于前端部分暂时无法提供用于测试的前端，为了保证后端开发的正常进行，出于微信小程序可能有特殊性的问题选择了开发后端测试用前端。  
    测试方法：每个按钮都会触发一个相应的后端接口函数，设计测试数据，逐个点击，检查返回结果  
    测试用前端界面如下：  
    <img src=https://tva1.sinaimg.cn/large/006tNbRwly1gaqlxkt7gij30hw0vm76g.jpg width=200>
    <img src=https://tva1.sinaimg.cn/large/006tNbRwly1gaqlzi8q36j30hu0vmwg9.jpg width=200>

## 系统部署
1. `MySQL`配置  
``` shell
sudo apt-get install mysql-server
mysql -u root -p 123456
create database test_db
```

2. `Python`配置  
``` shell
pip3 install django
pip3 install jieba
pip3 install pandas
pip3 install rest_frameworks
pip3 install qrcode
pip3 install pillow
pip3 install pymysql
```

3. `Django`数据库初始化
``` shell
python3 manage.py makemigrations
python3 manage.py migrate
```

4. `Nginx`安装
``` shell
sudo wget http://nginx.org/download/nginx-1.15.12.tar.gz 
tar -zxvf nginx-1.15.12.tar.gz
cd nginx-1.15.12
```
在`nginx`目录下修改配置文件`nginx.conf`

5. 运行
``` shell
nohup python3 manage.py runserver 127.0.0.1:8001 &
```
