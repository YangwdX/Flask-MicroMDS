## Dataset

- 目前的知识图谱来源于：[DiseaseKG:基于cnSchma常见疾病信息知识图谱](http://www.openkg.cn/dataset/disease-information)

## DIS（智能问药系统）
## MTS（智能就医系统）

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

- 知识图谱中需要引入**疾病的得病率（get_prob）（数据收集部分的工作）**，用正则表达式提取最大的数，没有就设为1（让用户自行判断）
- 处理用户文字输入部分需要使用**深度学习模型（模型训练部分的工作）**，输入为文字描述（String，不同症状间以“,”分隔），输出为症状列表（List）
  - 该部分模型涉及命名实体识别（识别出图谱中含有的症状）和实体映射（将一个字符串映射到图谱中的某一症状，如肚子有点疼→腹痛）
  - 命名实体识别部分：采用jieba分词，结合图谱中已有症状的txt文件，对文字描述进行分词，提取出文字描述中包含在图谱中的症状
  - 针对没有被命名实体识别部分成功识别出来的部分，进一步做实体映射：使用Bert模型编码字符串，选择余弦相似度最高的症状
    - 此部分Bert模型的训练需要用到的数据：**症状名称及其描述（数据收集部分的工作）**

## QAS（智能咨询系统）
