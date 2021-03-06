


"""
搜集插件各个类
"""


class Plugin(object):


    def __init__(self):

        # 插件的３个组件
        self.connection = {}
        self.actions = {}
        self.triggers = {}


    def add_connection(self, connect):
        self.connection[connect.name] = connect

    def add_actions(self, action):
        self.actions[action.name] = action

    def add_triggers(self, trigger):
        self.triggers[trigger.name] = trigger


