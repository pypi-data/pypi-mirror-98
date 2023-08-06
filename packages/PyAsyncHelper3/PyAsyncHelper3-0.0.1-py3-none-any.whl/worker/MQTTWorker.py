
import sys,logging
import PyAsyncHelper3.global_v as global_v
import json,base64
from PyAsyncHelper3.core.Router import GetCommand
from PyAsyncHelper3.core.WorkerBase import WorkerBase
from PyAsyncHelper3.core.Router import GetAction

class MQTTWorker(WorkerBase):
    _priority = -1 #关闭
    @staticmethod
    def on_message(client, userdata, message):
        try:
            msg_str = base64.b64decode(message.payload).decode("utf-8")
            msg_dict = json.loads(msg_str)
            content =json.loads(msg_dict["content"])
            command = content["Command"]
            func = GetCommand(command)
            if func:
                global_v.manager.add_task(func(msg_dict['id'],content))
        except Exception as e:
            logging.error("[+++++]line:{0},Function:{1},Exception:{2}".format(sys._getframe().f_lineno,
                                                                              sys._getframe().f_code.co_name,
                                                                              str(e)))
    @staticmethod
    async def product():
        try:
            # 连接EMQX服务器，host,port,username,password
            mqttHelper = MQTTConnector(global_v.server_host, global_v.server_port, global_v.server_username,
                                       global_v.server_password)
            # 连接回调函数
            mqttHelper.on_connect(None)
            # 消息接收函数
            mqttHelper.on_message(MQTTWorker.on_message)
            # 订阅主题client/1
            mqttHelper.subscribe(global_v.global_channel)
            # 开始运行
            mqttHelper.start()
            # 停止运行
            # mqttHelper.stop()
            global_v.mqttHelper = mqttHelper
            # 汇报自身状态
            # 登录
            item = LoginItem()
            item.GearUserName = global_v.gear_name
            item.GearPassword = global_v.gear_pass
            mqttHelper.publish_to_server(global_v.subscribe_channel, Command.Command_LoginAction, item.to_dict())
        except Exception as e:
            logging.error("[+++++]line:{0},Function:{1},Exception:{2}".format(sys._getframe().f_lineno,
                                                                              sys._getframe().f_code.co_name,
                                                                              str(e)))
