# 设置neo4j的配置信息
NEO4J_CONFIG = {
    "uri": "bolt://127.0.0.1:7687",
    "auth": ("neo4j", "123456"),
    "encrypted": False
}


# 读取txt文件返回list
def txt2list(file):
    with open(file, encoding="utf-8") as f:
        content = f.read()
        return content.split("\n")


# 定义pipeline中可能出现的错误
error_code_description = dict([
    (1, "请输入有效的症状描述！"),  # description 为空
    (2, "抱歉，我没有识别出有效的症状！"),  # symptoms 为空
    (3, "抱歉，这超出我的知识范围了！")  # diseases 为空
])
