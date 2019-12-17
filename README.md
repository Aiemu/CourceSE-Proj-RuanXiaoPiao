## Tips:
- Aiemu和tuyc17测试时使用的是各自的数据库，因此注意修改settings.py里关于DATABASE的设置。
- 重建数据库打的方法:删除app中migrations下的除_init_.py的所有文件,数据库中清除所有的表(DROP TABLE IF EXIST tablename;),执行migrate,makemigrations,migrate(Tricks:SET FOREIGN_KEY_CHEKCS = 0;最好清空表后回复1)
-ubuntu上的django倒退至2.2ver，安装了django-crontab。注意：只能在Linux环境下运行。

## Todo List:

backend:
-QRCode
-heat和django-crontab
...
-后续的数值确定与代码整理

frontend:
-sessionid与清华校园身份对接
...
-后续的ui优化

对接：
后端给前端提供认证成功时返回信息给后端的接口

- 更新总github有关开发进度记录

