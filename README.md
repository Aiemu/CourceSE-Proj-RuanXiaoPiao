## Tips:
- Aiemu和tuyc17测试时使用的是各自的数据库，因此注意修改settings.py里关于DATABASE的设置。
- 重建数据库打的方法:删除app中migrations下的除_init_.py的所有文件,数据库中清除所有的表(DROP TABLE IF EXIST tablename;),执行migrate,makemigrations,migrate(Tricks:SET FOREIGN_KEY_CHEKCS = 0;最好清空表后回复1)
- 可以在admin界面上传、管理图片了

## Todo List:
- 修改在admin界面增加Activity时会出现的未知错误
- 等待前端对接getList等
- 更新总github有关开发进度记录

