# -*- coding: utf-8 -*-

"""这里是Service的一些接口
"""


def GetCommonConfig():
	"""
	获取公共配置netgame_common.json中内容，将该文件内容映射为一个dict。

	Returns:
		dict           配置内容
	"""
	pass


def GetServerId():
	"""
	获取服务器id。

	Returns:
		int            服务器id，对应netgame_common.json中配置的serverid
	"""
	pass


def GetServiceConfig():
	"""
	获取service配置，该配置对应公共配置netgame_common.json中servicelist下对应service的配置。

	Returns:
		dict           配置内容
	"""
	pass


def StartRecordEvent():
	"""
	开始启动大厅服/游戏服与功能服之间的脚本事件收发包统计，启动后调用[StopRecordEvent()](#StopRecordEvent)即可获取两个函数调用之间引擎收发包的统计信息

	Returns:
		bool           执行结果
	"""
	pass


def StopRecordEvent():
	"""
	停止大厅服/游戏服与功能服之间的脚本事件收发包统计并输出结果，与[StartRecordEvent()](#StartRecordEvent)配合使用，输出结果为字典，具体见示例

	Returns:
		dict           收发包信息，具体见示例，假如没有调用过StartRecordEvent，则返回为None
	"""
	pass

