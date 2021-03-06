import os
import json

from .config import *
from .tools import Tools



tools = Tools()


def generate(path: str, yml: str):
    """
    生成插件
    """

    # 验证路径，　是否是yaml文件
    yml_path = os.path.join(path, yml)
    if not any([yml.endswith(y) for y in ["yml", "yaml"]]) or not os.path.exists(yml_path):
        logging.error(f"yaml路径错误 - {yml_path}")
        return
    else:
        yaml_data = tools.readYaml(yml_path)
        logging.info(f"readed {yml}")

    plugin_name = yaml_data.get("name", "hah")
    actions_class_list = []
    triggers_class_list = []

    # 当前文件路劲下生成sdk
    tar_path = os.path.join(BASE_DIR, os.path.join("res", "demo.tar.gz"))
    target_path = path
    tools.tarExtract(tar_path, target_path)

    # 读取types
    types = yaml_data.get("types")
    typesTemp = ""
    if types:
        for types_name, types_data in types.items():
            typesData = {
                "className": tools.getModelName(types_name),
                "args": tools.ymlTransPy(types_data)
            }
            typesTemp += tools.renderStrTemplate(typesData, MODELTEMPLATE)


    # 读取connection
    connection = yaml_data.get("connection")
    connection = {
                "className": tools.getModelName("connection"),
                "args": tools.ymlTransPy(connection)
            }
    connTemp = tools.renderStrTemplate(connection, MODELTEMPLATE)

    # 创建tests
    tests_path = os.path.join(path, "tests")
    if not os.path.exists(tests_path):
        os.mkdir(tests_path)


    # 生成actions
    actions_path = os.path.join(path, "actions")
    if not os.path.exists(actions_path):
        os.mkdir(actions_path)

    actionsTemp = ""
    actionsModelTemp = ""
    actionsModelTemp += modelHeader
    actionsModelTemp += typesTemp
    actionsModelTemp += connTemp

    actions = yaml_data.get("actions")
    if actions:

        init_list = []

        for title, data in actions.items():

            # models
            inp = data.get("input")
            outp = data.get("output")

            actionsName = tools.getModelName(title, "Actions")
            inpClassName = tools.getModelName(title, "Input")
            outpClassName = tools.getModelName(title, "Output")

            actions_class_list.append(actionsName)
            init_list.append([
                title,
                actionsName
            ])

            inp_data = {
                "className": inpClassName,
                "args": tools.ymlTransPy(inp)
            }
            outp_data = {
                "className": outpClassName,
                "args": tools.ymlTransPy(outp)
            }

            inpTemp = tools.renderStrTemplate(inp_data, MODELTEMPLATE)
            outpTemp = tools.renderStrTemplate(outp_data, MODELTEMPLATE)

            # model主要内容
            actionsModelTemp += inpTemp
            actionsModelTemp += outpTemp

            # action
            actionData = {
                "actionsName": actionsName,
                "name": title,
                "inputModel": inpClassName,
                "outputModel": outpClassName,
                "connModel": tools.getModelName("connection"),
            }
            actionsTemp = tools.renderStrTemplate(actionData, ACTIONTEMPLATE)

            file_path = os.path.join(actions_path, f"{title}.py")
            if not os.path.exists(file_path):
                tools.writeFile(actionsTemp, file_path)
                logging.info(f"gnerated actions/{title}.py ok")

            # 生成测试文件
            file_path = os.path.join(tests_path, f"{title}.json")
            testData = tools.renderStrTemplate({"title": title}, ACTIONSTESTTEMPLATE)
            tools.writeFile(testData, file_path)
            logging.info(f"generated tests/{title}.json ok")

        # 生成__init__.py
        file_path = os.path.join(actions_path, "__init__.py")
        initData = tools.renderStrTemplate({"init_list": init_list}, INITTEMPLATE)
        tools.writeFile(initData, file_path)
        logging.info(f"generated actions/__init__.py ok")

    file_path = os.path.join(actions_path, "models.py")
    tools.writeFile(actionsModelTemp, file_path)
    logging.info(f"gnerated actions/models.py ok")


    # 生成triggers
    triggers_path = os.path.join(path, "triggers")
    if not os.path.exists(triggers_path):
        os.mkdir(triggers_path)

    triggersTemp = ""
    triggersModelTemp = ""
    triggersModelTemp += modelHeader
    triggersModelTemp += typesTemp
    triggersModelTemp += connTemp

    triggers = yaml_data.get("triggers")
    if triggers:
        init_list = []

        for title, data in triggers.items():

            # models
            inp = data.get("input")
            outp = data.get("output")

            triggersName = tools.getModelName(title, "Triggers")
            inpClassName = tools.getModelName(title, "Input")
            outpClassName = tools.getModelName(title, "Output")

            triggers_class_list.append(triggersName)
            init_list.append([
                title,
                triggersName
            ])

            inp_data = {
                "className": inpClassName,
                "args": tools.ymlTransPy(inp)
            }
            outp_data = {
                "className": outpClassName,
                "args": tools.ymlTransPy(outp)
            }

            inpTemp = tools.renderStrTemplate(inp_data, MODELTEMPLATE)
            outpTemp = tools.renderStrTemplate(outp_data, MODELTEMPLATE)

            # model主要内容
            triggersModelTemp += inpTemp
            triggersModelTemp += outpTemp

            # trigger
            triggerData = {
                "triggersName": triggersName,
                "name": title,
                "inputModel": inpClassName,
                "outputModel": outpClassName,
                "connModel": tools.getModelName("connection"),
            }
            triggersTemp = tools.renderStrTemplate(triggerData, TRIGGERSTEMPLATE)

            file_path = os.path.join(triggers_path, f"{title}.py")
            if not os.path.exists(file_path):
                tools.writeFile(triggersTemp, file_path)
                logging.info(f"gnerated triggers/{title}.py ok")

            # 生成测试文件
            file_path = os.path.join(tests_path, f"{title}.json")
            testData = tools.renderStrTemplate({"title": title}, TRIGGERSTESTTEMPLATE)
            tools.writeFile(testData, file_path)
            logging.info(f"generated tests/{title}.json ok")

        # 生成__init__.py
        file_path = os.path.join(triggers_path, "__init__.py")
        initData = tools.renderStrTemplate({"init_list": init_list}, INITTEMPLATE)
        tools.writeFile(initData, file_path)
        logging.info(f"generated actions/__init__.py ok")


    file_path = os.path.join(triggers_path, "models.py")
    tools.writeFile(triggersModelTemp, file_path)
    logging.info(f"gnerated triggers/models.py ok")


    # 创建入口文件　main.py
    mainData = {
        "pluginName": tools.getModelName(plugin_name, "Plugin"),
        "actionClassees": actions_class_list,
        "triggerClassees": triggers_class_list
    }
    file_path = os.path.join(path, "main.py")
    mainTemp = tools.renderStrTemplate(mainData, MAINTEMPLATE)
    tools.writeFile(mainTemp, file_path)
    logging.info(f"generated main.py ok")


    # 创建help.md
    helpData = yaml_data
    file_path = os.path.join(path, "help.md")
    mainTemp = tools.renderStrTemplate(helpData, HELPTEMPLATE)
    tools.writeFile(mainTemp, file_path)
    logging.info("generated help.md ok")

    # 生成util
    util_path = os.path.join(path, "util")
    if not os.path.exists(util_path):
        os.mkdir(util_path)
        logging.info("generated util ok")



    logging.info("All things done successfully ^_^")

def run(path: str, tests: str):

    main_path = os.path.join(path, "main.py")
    tests_path = os.path.join(path, tests)

    if not os.path.exists(tests_path):
        logging.error(f"请正确输入路径")


    cmd = f"python {main_path} run < {tests_path}"
    os.system(cmd)

def http(path: str):
    main_path = os.path.join(path, "main.py")


    cmd = f"python {main_path} http"
    os.system(cmd)

def test(path: str, tests: str):
    main_path = os.path.join(path, "main.py")
    tests_path = os.path.join(path, tests)

    if not os.path.exists(tests_path):
        logging.error(f"请正确输入路径")

    cmd = f"python {main_path} test < {tests_path}"
    os.system(cmd)

def tarball(path: str):

    Makefile_path = os.path.join(path, "Makefile")
    if os.path.exists(Makefile_path):
        cmd = "make tarball"
        os.system(cmd)


def mkimg(path: str):
    Makefile_path = os.path.join(path, "Makefile")
    if os.path.exists(Makefile_path):
        cmd = "make image"
        os.system(cmd)


