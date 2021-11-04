1. 服务器上运行，首次运行需执行pip install Flask==1.1.2 Flask-Cors==3.0.10 mysql-connector-python
2. (Linux) 运行./run.sh启动后端（可能需要先执行chmod u+x run.sh)
3. (Windows) 依次执行set FLASK_APP=init.py，set FLASK_RUN_HOST=0.0.0.0 和 set FLASK_RUN_PORT=8000，最后再执行flask run启动后端
