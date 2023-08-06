#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     Router
   Description :
   Author :        admin
   date：          2020/7/30
-------------------------------------------------
   Change Activity:
                   2020/7/30
-------------------------------------------------
"""
import functools,logging,sys

G_Action_Dict = {}
G_Command_Dict = {}
G_Action_Limit_Dict = {}
def Router(command):
    '''
    #定义Router装饰器
    :param f:参数Aaction
    :return:
    '''
    def wrapper(func):
        if command not in G_Command_Dict.keys():
            G_Command_Dict[command] = func
        else:
            raise Exception('{}重复定义'.format(command))
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error("[+++++]line:{0},Function:{1},Exception:{2}".format(sys._getframe().f_lineno,
                                                                                  sys._getframe().f_code.co_name,
                                                                                  str(e)))

        return decorated
    return wrapper

def GetCommand(command):
    ret = None
    if command in G_Command_Dict.keys():
        return G_Command_Dict[command]
    return ret

def Action(action,limit,timeout):
    '''
    #定义Router装饰器
    :param f:参数Aaction
    :return:
    '''
    def wrapper(func):
        if action not in G_Action_Dict.keys():
            G_Action_Dict[action] = func
        else:
            raise Exception('{}重复定义'.format(action))
        if action not in G_Action_Limit_Dict.keys():
            time_dict = {
                "limit":limit,
                "timeout":timeout
            }
            G_Action_Limit_Dict[action] = time_dict
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error("[+++++]line:{0},Function:{1},Exception:{2}".format(sys._getframe().f_lineno,
                                                                                  sys._getframe().f_code.co_name,
                                                                                  str(e)))
        return decorated
    return wrapper

def GetAction(action):
    if action in G_Action_Dict.keys():
        return G_Action_Dict[action]
    return None


import json
def GetActionLimit():
    return G_Action_Limit_Dict

def AddActionLimit(action):
    if action in G_Action_Limit_Dict.keys():
        G_Action_Limit_Dict[action]["limit"] +=1
def DelActionLimit(action):
    if action in G_Action_Limit_Dict.keys():
        G_Action_Limit_Dict[action]["limit"] -=1