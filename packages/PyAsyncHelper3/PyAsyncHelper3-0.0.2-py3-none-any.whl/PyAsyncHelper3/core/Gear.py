import os,sys
import importlib
from PyAsyncHelper3.core import Global
import inspect
from pyhelper3.YamlHelper import YamlHelper
import os
import PyAsyncHelper3.global_v as global_v
import asyncio
from PyAsyncHelper3.core.AsyncManager import AsyncManager
class Gear(object):
    __init_path = dict()
    __config_path = None
    __open_server = False
    __manager = None
    @staticmethod
    def get_parent_dir(path,parent=1):
        dir_name = path
        while parent > 0 :
            dir_name = os.path.dirname(dir_name)
            parent -=1
        return dir_name
    @staticmethod
    async def init(manager):
        global_v.global_token = ''
        #先初始化配置文件
        if Gear.__config_path:
            Gear.read_config_file(Gear.__config_path)
        if Gear.__open_server:
            Gear.__init_path['PyAsyncHelper3.worker'] = set()
            # 内置启动目录
            Gear.__init_path['PyAsyncHelper3.worker'].add(Gear.get_parent_dir(os.path.dirname(__file__),1)+"\\worker\\")

        for key in Gear.__init_path.keys():
            for path in Gear.__init_path[key]:
                Gear.Register(key,path)

        bit_list = sorted(Global.g_worker_dict.keys())
        bit_list.reverse()
        asyncio.ensure_future(AsyncManager.task_check())
        for key in bit_list:
            for work in Global.g_worker_dict[key]:
                print("[++++++++++++++{}]启动".format(work._type))
                task = manager.add_task(func=work.product,is_thread=True)

    @staticmethod
    def start():
        loop = asyncio.get_event_loop()
        try:
            #启动
            Gear.__manager = AsyncManager(loop)
            asyncio.ensure_future(Gear.init(Gear.__manager))
            # 完成任务就退出
            # loop.run_until_complete()
            # 主循环一直运行
            loop.run_forever()
        except Exception as e:
            print(e)
            # for task in asyncio.Task.all_tasks():
            #     print(task.cancel())
            loop.stop()
        finally:
            loop.close()
    @staticmethod
    def get_manager():
        return Gear.__manager
    @staticmethod
    def set_config_path(config_path):
        Gear.__config_path = config_path
    @staticmethod
    def set_init_path(module,path):
        '''
        设置初始化目录
        :param path:
        :return:
        '''
        if module not in Gear.__init_path.keys():
            Gear.__init_path[module] = set()
        Gear.__init_path[module].add(path)
    @staticmethod
    def open_server():
        Gear.__open_server = True
    @staticmethod
    def read_config_file(config_path):
        '''
        初始化配置文件
        :param config_path:
        :return:
        '''
        # 读取配置文件
        yaml_config = YamlHelper(config_path)
        gear_info = yaml_config.get_data_by_key('gear')
        global_v.gear_name = gear_info['gear_username']
        global_v.gear_pass = gear_info['gear_password']
        global_v.global_channel = 'client/' + global_v.gear_name
        server_info = yaml_config.get_data_by_key('server')
        global_v.server_host = server_info['server_host']
        global_v.server_port = server_info['server_port']
        global_v.server_username = server_info['server_username']
        global_v.server_password = server_info['server_password']
        global_v.subscribe_channel = server_info['subscribe_channel']
    #递归检测插件路径下的所有插件，并将它们存到内存中
    @staticmethod
    def Register(key,path):
        if os.path.isdir(path):
            items = os.listdir(path)
            for item in items:
                if os.path.isdir(os.path.join(path,item)):
                    pass
                else:
                    if item.endswith('.py') and item != '__init__.py':
                        moduleName = item[:-3]
                        #if moduleName not in sys.modules:
                        module = importlib.import_module('{0}.{1}'.format(key,moduleName))
                        #获取模块名称
                        for name, _class in inspect.getmembers(module):
                            if inspect.isclass(_class) and hasattr(_class,'_priority'):
                                priority = _class._priority
                                # 判断是否开启
                                if priority != -1:
                                    # 获取类型
                                    Global.set_worker(priority, _class)
                                    print("{}{}加载成功".format(path, item))

        elif os.path.isfile(path):
            file = os.path.basename(path)
            if file.endswith('.py') and file != '__init__.py':
                moduleName = file[:-3]
                if moduleName not in sys.modules:
                    module = importlib.import_module('{0}.{1}'.format(key,moduleName))
                    print("{}加载成功".format(path))
                    # 获取模块名称
                    for name, _class in inspect.getmembers(module):
                        if inspect.isclass(_class) and hasattr(_class, '_priority'):
                            priority = _class._priority
                            # 判断是否开启
                            if priority != -1:
                                # 获取类型
                                Global.set_worker(priority, _class)

