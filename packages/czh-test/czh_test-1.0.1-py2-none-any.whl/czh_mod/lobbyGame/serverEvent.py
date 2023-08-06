# -*- coding: utf-8 -*-

"""
事件的定义。
"""

class ServerEvent:
		"""
		master成功连接到当前服务器事件.

		Event Function Args:
			isConnect      int            1代表连接建立，0代表连接中断
			serverId       int            当前lobby/game服务器id

		"""
		MasterConnectStatusEvent = "MasterConnectStatusEvent"

		"""
		强制关闭当前服务器时会触发本事件。只应用于引擎，不建议开发者使用。

		"""
		MasterForceShutDownEvent = "MasterForceShutDownEvent"

		"""
		优雅关闭当前服务器时会触发本事件。只应用于引擎，不建议开发者使用。

		"""
		MasterGraceShutDownEvent = "MasterGraceShutDownEvent"

		"""
		引擎重新加载配置后触发此事件。

		"""
		ReloadCommonConfigEvent = "ReloadCommonConfigEvent"

		"""
		玩家登录到lobby/game过程中，获取玩家在线锁事件。事件触发时，玩家还处于开始登录阶段，
	还没有下载行为包，且没有在地图中出生。在线锁实质是redis中记录的玩家在线信息，redis key格式
	是“user:online: + netease uid”，它是个hash表，包含两个hash key:serverid,proxyid。

		Event Function Args:
			uid            int            玩家的netease uid，玩家的唯一标识
			serverId       int            当前服务器id
			proxyId        int            当前客户端连接的proxy服务器id

		"""
		ServerGetPlayerLockEvent = "ServerGetPlayerLockEvent"

		"""
		创建玩家对象过程中，设置玩家出生位置时触发本事件。

		Event Function Args:
			userId         int            玩家的netease uid
			dimensionId    int            玩家出生dimension，支持修改
			posx           int            玩家出生位置，支持修改
			posy           int            玩家出生位置，支持修改
			posz           int            玩家出生位置，支持修改
			deltax         int            玩家motion位置，初始值为存档中的数据。若修改了posx/posy/posz，则建议设置为0。
			deltay         int            玩家motion位置，初始值为存档中的数据。若修改了posx/posy/posz，则建议设置为0。
			deltaz         int            玩家motion位置，初始值为存档中的数据。若修改了posx/posy/posz，则建议设置为0。
			rotx           int            玩家的rot，初始值为存档中的数据，支持修改
			roty           int            玩家的rot，初始值为存档中的数据，支持修改
			ret            bool           是否需要修改玩家初始位置，设置为True后其他数据的修改才会生效

		"""
		ServerPlayerBornPosEvent = "ServerPlayerBornPosEvent"

		"""
		玩家下线过程中，释放在redis中的玩家在线锁事件。事件触发时，客户端同服务端断开了连接，玩
	家数据已经保存到地图，玩家已经不存在于mc的世界中。在线锁实质是redis中记录的玩家在线信息，
	redis key格式是“user:online: + netease uid”，它是个hash表，包含两个hash key:serverid,proxyid。

		Event Function Args:
			uid            str            玩家的netease uid，玩家的唯一标识

		"""
		ServerReleasePlayerLockEvent = "ServerReleasePlayerLockEvent"

		"""
		游戏强制关闭过程中，玩家强制下线时触发本事件。事件回调函数需要释放在redis中的
	玩家的在线锁。主要应用于lobby/game官方mod neteaseOnline。

		Event Function Args:
			idx            str            事件唯一id，回调时返回
			uid            str            玩家的netease uid，玩家的唯一标识

		"""
		ServerReleasePlayerLockOnShutDownEvent = "ServerReleasePlayerLockOnShutDownEvent"

		"""
		游戏即将强制关闭触发本事件。事件回调函数需要好清理和存档工作，同时终止或强制join所有异步线程.

		"""
		ServerWillShutDownEvent = "ServerWillShutDownEvent"

		"""
		service与lobby/game的成功建立连接事件。

		Event Function Args:
			serverId       int            service的服务器id

		"""
		ServiceConnectEvent = "ServiceConnectEvent"

		"""
		service与lobby/game断开连接事件。

		Event Function Args:
			serverId       int            service的服务器id

		"""
		ServiceDisconnectEvent = "ServiceDisconnectEvent"

		"""
		service向lobby/game注册module。只应用于引擎，不建议开发者使用。

		Event Function Args:
			serverId       int            service服务器id
			moduleName     str            模块名，是公共配置netgame_common.json中module_names中某个module

		"""
		ServiceRegisterModuleEvent = "ServiceRegisterModuleEvent"

		"""
		触发时机:玩家游戏内购买商品时服务端抛出的事件

		Event Function Args:
			playerId       str            购买商品的玩家实体id

		"""
		StoreBuySuccServerEvent = "StoreBuySuccServerEvent"

		"""
		玩家上线时，引擎读取玩家entity存档数据时触发本事件。
	不建议开发者使用本事件！只有【set_use_database_save】设置使用数据库存档后，本事件才有效。
	触发本事件，开发者需要从存档中读取玩家entity数据，然后通过【query_player_data_result】
	将修改后玩家entity数据设置回引擎。

		Event Function Args:
			idx            str            事件唯一id，【query_player_data_result】会使用到这个id
			playerKey      str            玩家的netease uid，玩家的唯一标识
			dbName         str            数据库存档的前缀，可以通过【set_use_database_save】设置dbname

		"""
		queryPlayerDataEvent = "queryPlayerDataEvent"

		"""
		保存玩家数据事件，玩家下线时也会触发该事件。只有【set_use_database_save】 设置
	useDatabase为True时，本事件才生效。本事件的回调函数
	必须调用【save_player_data_result】函数，把存档状态告知引擎。

		Event Function Args:
			idx            str            引擎回调函数id，【save_player_data_result】会使用这个id
			playerKey      str            玩家的netease uid，玩家的唯一标识

		"""
		savePlayerDataEvent = "savePlayerDataEvent"

		"""
		游戏强制关闭过程中，玩家下线时会触发本事件。另外，只有【set_use_database_save】 设置
	useDatabase为True时，本事件才生效。本事件的回调函数必须调用
	【save_player_data_result】函数，把存档状态告知引擎。

		Event Function Args:
			idx            str            引擎回调函数id，【save_player_data_result】函数会使用这个id
			playerKey      str            玩家的netease uid，玩家的唯一标识

		"""
		savePlayerDataOnShutDownEvent = "savePlayerDataOnShutDownEvent"

