

try:
    from .web import Server
    from .base import Core, CatchErr
except:
    from web import Server
    from base import Core, CatchErr



"""
入口后第一步，中转各种情况
"""


core = Core()

@CatchErr.print_err_stack
def run(plugin_stdin, plugins):

    stdin_body = core.parse_stdin(plugin_stdin)


    # 判断是 actions 还是 triggers
    action_name = core.extract_pointer(stdin_body, "/action")
    trigger_name = core.extract_pointer(stdin_body, "/trigger")

    connect_data = core.extract_pointer(stdin_body, "/connection")

    if action_name:
        """
        actions
        plugin_spec_version: v1
        走脚本
        """

        # 外部类
        action_model = plugins.actions[action_name]

        # 获取input
        inp = core.extract_pointer(stdin_body, "/input")

        # 执行　外部run 相关操作
        action_model._run(inp, connect_data)



    elif trigger_name:

        enable_web = core.extract_pointer(stdin_body, "/enable_web")

        if enable_web:
            """
            triggers
            body.enable_web: True
            跑web服务
            """
            server = Server(plugins)
            server.runserver()

        else:
            """
            triggers
            body.enable_web: False
            走脚本
            """

            # 外部类
            trigger_model = plugins.triggers[trigger_name]

            # 获取input
            inp = core.extract_pointer(stdin_body, "/input")
            dispatcher_url = core.extract_pointer(stdin_body, "/dispatcher/url")

            # 执行　外部run 相关操作
            trigger_model._run(inp, connect_data, dispatcher_url)



@CatchErr.print_err_stack
def test(plugin_stdin, plugins):

    stdin_body = core.parse_stdin(plugin_stdin)

    connect_data = core.extract_pointer(stdin_body, "/connection")

    name = ""
    action_name = core.extract_pointer(stdin_body, "/action")
    trigger_name = core.extract_pointer(stdin_body, "/trigger")

    if action_name:
        name = action_name
        model = plugins.actions[name]
    elif trigger_name:
        name = trigger_name
        model = plugins.triggers[name]

    if name:
        output = model.test(connect_data)
        return output



@CatchErr.print_err_stack
def http(plugins):
    server = Server(plugins)
    server.runserver()


