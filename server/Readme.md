1. 服务器上运行，首次运行需执行```pip install -r requirements.txt```
2. (Linux) 运行./run.sh启动后端（可能需要先执行chmod u+x run.sh)
3. (Windows) 依次执行
 ```
 set FLASK_APP=__init__.py
 set FLASK_RUN_HOST=0.0.0.0
 set FLASK_RUN_PORT=8000
 flask run
 ```
执行set FLASK_APP=\_\_init\_\_.py，set FLASK_RUN_HOST=0.0.0.0 和 set FLASK_RUN_PORT=8000，最后再执行flask run启动后端

### models.py
- 调用数据库的类

### auth.py
- 与前端关联函数（登录、注册）

### group.py
- 与前端关联函数（群组）

### gathering.py
- 与前端关联函数（聚会）

### utils.py
- 后端的函数（与前端无关）

