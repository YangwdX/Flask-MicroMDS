#### 运行前准备
- 导入[DiseaseKG:基于cnSchma常见疾病信息知识图谱](http://www.openkg.cn/dataset/disease-information)（用户名：neo4j，密码：123456）
- 确认 config.py 中的 NEO4J_CONFIG（主要是端口号）
- 安装 gunicorn（用来运行和管理Flask）

#### 以Flask项目形式启动
- 启动后台服务，终端运行：gunicorn -w 1 -b 127.0.0.1:5000 main_server:app --log-level debug
- 重启后台服务，终端运行：pgrep gunicorn | xargs kill -HUP（或者Ctrl C，再启动）
- 模拟网页前端，终端运行：python test_server.py（或者先重启一下 pgrep gunicorn | xargs kill -HUP; python test_server.py）

#### 以普通模式启动
- 终端运行：python main_server.py

#### Notes
- 知识图谱中需要引入疾病的得病率（get_prob），用正则表达式提取最大的数，没有就设为1（让用户自行判断）