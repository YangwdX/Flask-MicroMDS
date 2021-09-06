from os import error
from flask import Flask
from flask import request
from neo4j import GraphDatabase
from itertools import combinations
from config import *
import jieba
jieba.load_userdict("./dict/symptom.txt")
print("-" * 52 + "\n")

app = Flask(__name__)
neo4j_driver = GraphDatabase.driver(**NEO4J_CONFIG)
neo4j_symptoms = txt2list("./dict/symptom.txt")
flask_mode = True


# 处理用户症状选择或文字输入
def description_process(type, description):
    if not type:  # 类型0，症状选择
        symptoms = description.split(",")
    else:  # 类型1，文字输入
        symptoms = []
        jieba_lcut = jieba.lcut(description)
        print(f"\033[;36mjieba_lcut: \033[0m{jieba_lcut}")
        for item in jieba_lcut:
            if item in neo4j_symptoms:
                symptoms.append(item)
            elif len(item) >= 2:
                pass
    symptoms = sorted(set(symptoms), key=symptoms.index)  # 去除重复项
    return symptoms


# 构造症状List
def get_symptoms_list(symptoms):
    # # 按照前向最大匹配的思路构造症状List
    # symptoms_list = []
    # symptoms_list.append(symptoms)
    # for index in range(len(symptoms) - 1, 0, -1):
    #     symptoms_list.append(symptoms[:index])

    # 按照从长到短的顺序，以组合的形式构造症状List
    symptoms_list = []
    for length in range(len(symptoms), 0, -1):
        symptoms_list.extend(list(combinations(symptoms, length)))
    return symptoms_list


# 查询Neo4j图数据库
def query_neo4j(symptoms):
    # 构造症状List
    symptoms_list = get_symptoms_list(symptoms)
    print(f"\033[;36msymptoms_list: \033[0m{symptoms_list}")

    # 基于症状List查询图数据库
    for symptoms in symptoms_list:
        with neo4j_driver.session() as session:
            cypher = ""
            template = 'MATCH (a:Symptom)-[r:has_symptom]-(b:Disease) WHERE ("Placeholder" IN a.name) WITH b '
            for symptom in symptoms:
                cypher += template.replace("Placeholder", symptom)
            cypher = cypher[:-7] + "RETURN b LIMIT 20"  # 去掉最后一个"WITH b "
            # print(cypher)
            records = session.run(cypher)
            # 从records中读取疾病信息, 并封装成List
            result = list(map(lambda x: dict(x.items()), records.value()))
            # 以疾病name为key，疾病相关信息为value重新构建result
            keys = list(map(lambda disease: disease["name"], result))
            result = dict(zip(keys, result))
            if result:  # symptoms_list中前面的item优先级高，如果查询到结果就返回
                print(f"\033[;36mquery_symptoms: \033[0m{symptoms}")
                return result
    return None


@app.route('/MTS_server/main_serve/', methods=["POST"])
def main_serve():
    if flask_mode:
        type = request.form['type']  # 0代表症状选择，1代表文字输入
        description = request.form['description']  # 两种方式都以String形式传递，0类型用“,”分隔
    else:
        type = 1
        # description = "鼻塞情绪性感冒"
        description = "鼻塞情绪性感冒傻逼玩意鼻塞咳嗽"
        # description = "这是一个无效的症状描述！"
    print(f"\033[;36mdescription: \033[0m{description}")
    # 判断当前pipeline的结果是否符合预期（description非空）
    if not description:
        print(error_code_description[1], end="\n\n")
        return {1: error_code_description[1]}

    symptoms = description_process(type, description)
    print(f"\033[;36msymptoms: \033[0m{symptoms}")
    # 判断当前pipeline的结果是否符合预期（symptoms非空）
    if not symptoms:
        print(error_code_description[2], end="\n\n")
        return {2: error_code_description[2]}

    diseases = query_neo4j(symptoms)
    print(f"\033[;36mdiseases: \033[0m{diseases.keys()}")
    # 判断当前pipeline的结果是否符合预期（diseases非空）
    if not diseases:
        print(error_code_description[3], end="\n\n")
        return {3: error_code_description[3]}

    print("\n" + "-" * 52 + "\n")
    return str(diseases)


if __name__ == '__main__':
    flask_mode = False
    main_serve()
