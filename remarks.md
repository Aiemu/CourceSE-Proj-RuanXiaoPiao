## Tips:
- 不需要wechat_id,需要open_id,用以向微信服务器索取用户信息
- 重建数据库打的方法:删除app中migrations下的除_init_.py的所有文件,数据库中清除所有的表(DROP TABLE IF EXIST tablename;),执行migrate,makemigrations,migrate(Tricks:SET FOREIGN_KEY_CHEKCS = 0;最好清空表后回复1)


## Todo List:
- 修改数据库中的数据表(已创建表.需要添加数据)(考虑使用mysql workbench进行可视化管理)
- (动态\随时)根据其它端打需要,修改models.py
- ForeignKey的理解似乎有误
- 从数据库中读入数据表的方法
- (疑惑)修改models后,如果表的成员类型发生了变化,原先的数据会如何变化?直接失效?对应类型转换?(已解决)
- 更新总github有关开发进度记录
    
## Operation on mysql: 
``` bash
mysql -p -h 127.0.0.1 TEST_DATA
password: xe1peeGh
```
``` bash
SHOW TABLES;
SELECT * FROM TEST_DATA.auth_group;
DESCRIBE Ticket
```


## Current DataBase Info: 
``` bash
MariaDB [TEST_DATA]> DESCRIBE Ticket;
```
+-----------+---------+------+-----+---------+-------+  
| Field     | Type    | Null | Key | Default | Extra |  
+-----------+---------+------+-----+---------+-------+  
| ticket_id | int(11) | NO   | PRI | NULL    |       |  
+-----------+---------+------+-----+---------+-------+  
1 row in set (0.001 sec)  

``` bash 
MariaDB [TEST_DATA]> describe Activity;
```

+-------------+-------------+------+-----+---------+-------+  
| Field       | Type        | Null | Key | Default | Extra |  
+-------------+-------------+------+-----+---------+-------+  
| activity_id | int(11)     | NO   | PRI | NULL    |       |  
| title       | varchar(20) | NO   |     | NULL    |       |  
+-------------+-------------+------+-----+---------+-------+  
2 rows in set (0.002 sec)  

``` bash 
MariaDB [TEST_DATA]> describe User;
```

+------------+-------------+------+-----+---------+-------+  
| Field      | Type        | Null | Key | Default | Extra |  
+------------+-------------+------+-----+---------+-------+  
| user_id    | int(11)     | NO   | PRI | NULL    |       |  
| username   | varchar(30) | NO   |     | NULL    |       |  
| password   | varchar(30) | NO   |     | NULL    |       |  
| student_id | varchar(10) | NO   |     | NULL    |       |  
+------------+-------------+------+-----+---------+-------+  
4 rows in set (0.002 sec)  
