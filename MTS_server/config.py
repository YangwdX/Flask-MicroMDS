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