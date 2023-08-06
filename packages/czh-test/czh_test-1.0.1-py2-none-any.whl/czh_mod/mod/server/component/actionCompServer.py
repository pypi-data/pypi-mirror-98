# -*- coding: utf-8 -*-

from mod.common.component.baseComponent import BaseComponent

class ActionCompServer(BaseComponent):
    def SetAttackTarget(self, targetId):
        # type: (str) -> bool
        """
        设置仇恨目标
        """
        pass

    def ResetAttackTarget(self):
        # type: () -> bool
        """
        清除仇恨目标
        """
        pass

    def GetAttackTarget(self):
        # type: () -> str
        """
        获取仇恨目标
        """
        pass

    def SetHurtBy(self, attackerId):
        # type: (str) -> bool
        """
        设置上一次攻击自己的实体，即让他认为某个实体刚才对他发起了攻击（虽然实际上没有）。该标记会驱动一些生物行为，例如minecraft:behavior.panic会使生物远离标记的实体，minecraft:angry会使将该标记转为自身的仇恨目标等等。
        """
        pass

    def ResetHurtBy(self):
        # type: () -> bool
        """
        清除上一次攻击自己的实体的标记。该标记的解释见SetHurtBy
        """
        pass

    def GetHurtBy(self):
        # type: () -> str
        """
        获取上一次攻击自己的实体。该标记的解释见SetHurtBy
        """
        pass

    def SetMobKnockback(self, xd=0.1, zd=0.1, power=1.0, height=1.0, heightCap=1.0):
        # type: (float, float, float, float, float) -> None
        """
        设置击退的初始速度，需要考虑阻力的影响
        """
        pass

