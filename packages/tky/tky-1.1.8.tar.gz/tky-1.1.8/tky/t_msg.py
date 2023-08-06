# _*_ coding:utf-8 _*_
"""
常用数据类函数集合
\n 目前支持方法有：
\n we_msg （微信自有接口消息推送，依赖Json/urllib.request）
\n wek_msg （推送企业微信机器人消息，依赖Json/urllib.request）
\n @author: 'TangKaiYue'
"""

from .t_jde import null


# 企业微信推送（自有接口）
def we_msg(self: str = 'null', emp_list: str = 'null', msg: str = 'null'):
    """
    【从自有消息接口推送企业微信消息】\n
    :param  self : str 推送的地址；
    :param  emp_list : str 推送的对象(如：“用户1,用户2”)；
    :param  msg : str 消息体；
    :return  输出结果；
    """
    try:
        if null(self) == 'N' or null(msg) == 'N' or null(emp_list) == 'N':
            return '入参异常：请传入 self、msg、emp_list 不为空的数据 ...'
        else:
            import json
            import urllib.request
            # 企业微信推送接口的内容
            con = {"empCode": emp_list, "message": msg}
            print(con)
            new_msg = json.dumps(con).encode('utf-8')
            req = urllib.request.Request(self, new_msg)
            req.add_header('Content-Type', 'application/json')
            we_mse = urllib.request.urlopen(req)
            return we_mse
    except EnvironmentError as err:
        return '发生异常：%s' % err


# 企业微信推送（外部服务）
def wek_msg(self: str = 'null', msg_type: str = 'text', msg: str = 'null'):
    """
    【推送企业微信机器人消息】\n
    注：每个机器人发送的消息不能超过20条/分钟。\n
    :param  self : str 企业微信配置机器人webhook地址；
    :param  msg_type : str 消息类型(text/markdown/image/file),暂时只支持text/markdown；
    :param  msg : str 推送的消息内容；
    :return  输出结果；
    """
    try:
        if null(self) == 'N' or null(msg) == 'N':
            return '入参异常：请传入 self、msg 不为空的数据 ...'
        import json
        import urllib.request
        if msg_type == 'text' or msg_type == 'TEXT' or msg_type == 'Text':
            # 企业微信text推送接口的内容
            con = {"msgtype": 'text', "text": {"content": msg}}
            print(con)
            new_msg = json.dumps(con).encode('utf-8')
            req = urllib.request.Request(self, new_msg)
            req.add_header('Content-Type', 'application/json')
            we_mse = urllib.request.urlopen(req)
            return we_mse
        if msg_type == 'markdown' or msg_type == 'MARKDOWN' or msg_type == 'Markdown':
            # 企业微信text推送接口的内容
            con = {"msgtype": 'markdown', "markdown": {"content": msg}}
            print(con)
            new_msg = json.dumps(con).encode('utf-8')
            req = urllib.request.Request(self, new_msg)
            req.add_header('Content-Type', 'application/json')
            we_mse = urllib.request.urlopen(req)
            return we_mse
    except EnvironmentError as err:
        return '发生异常：%s' % err
