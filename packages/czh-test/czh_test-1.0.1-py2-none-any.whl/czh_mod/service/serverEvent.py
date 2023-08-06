# -*- coding: utf-8 -*-

"""
事件的定义。
"""

class ServerEvent:
		"""
		service公共配置netgame_common.json发生变化时触发。比如新增或删服服务器。

		"""
		NetGameCommonConfChangeEvent = "NetGameCommonConfChangeEvent"

		"""
		lobby/game/proxy成功建立连接时触发。

		Event Function Args:
			serverId       int            服务器id
			protocolVersionint            协议版本号

		"""
		ServerConnectedEvent = "ServerConnectedEvent"

		"""
		lobby/game/proxy断开连接时触发。

		Event Function Args:
			serverId       int            服务器id

		"""
		ServerDisconnectEvent = "ServerDisconnectEvent"

		"""
		lobby/game/proxy状态发生变化时触发。

		Event Function Args:
			服务器id的字符串str            服务器状态。服务器状态如下：‘1’ 就绪状态，‘2’ 停止状态，‘3’ 准备状态。服务器状态为'1'时，服务器才可用，其他状态下，服务器不可用。

		"""
		UpdateServerStatusEvent = "UpdateServerStatusEvent"

