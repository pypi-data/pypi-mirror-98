# -*- coding: utf-8 -*-

"""这里是一些Master的基础API接口。
"""


def GetCommonConfig():
	"""
	获取公共配置netgame_common.json中内容，将该文件内容映射为一个dict。

	Returns:
		dict           配置内容
	"""
	pass


def IsService(serverId):
	# type: (int) -> bool
	"""
	服务器是否是service服。

	Args:
		serverId       int            服务器id

	Returns:
		bool           True表示是service，False不是service
	"""
	pass

