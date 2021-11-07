# SoftwareEngineeringB11
### [前端 client](/client)
### [后端 server](/server)
### 前后端接口
- 登录
  - 路径：/login
  - 后端函数：login()
  - 功能：验证用户名与密码
  - 输入：data { username, password }
  - 输出：data { status, message }
- 注册
  - 路径：/register
  - 后端函数：register()
  - 功能：验证注册信息，写入数据库
  - 输入：data { username, password, email, phone, birthday }
  - 输出：data { status, message }
