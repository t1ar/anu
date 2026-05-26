#this is python compiler setting, use directly in files
# from __future__ import annotations , basically stringify all your annotation
# for e.g, def func() -> type(self), now turns to def func() -> "type(self)"
# this is useful if ur lazy like me and dont want to stringify it manually
# only for python 3.13 and below

# used to avoid class undefined typing crash, like:
# for @classmethod, you return itself, but its not defined yet
# or you have conflicting import loop: A need B, B need A

# and use TYPE_CHECKING for if you want to import class for autocompletion
# keep in mind, TYPE_CHECKING is false during run-time, so you would either need
# __future__ to automatically define it for you,
# or just do lazy import, by importing the moment you actually need it

#dataclass to skip typing __init__() for instancing a new object, and also makes a new default def __post_init__()
#field to tell python what to do to the self.fields behaviour, like init, default value, etc 
from dataclasses import dataclass, field 
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from pathlib import Path
from abc import ABC, abstractmethod
from copy import copy #, deepcopy # try to not use deepcopy, very bad for performance, either copy whats needed or instance a new object with the same data
from enum import Enum, auto
from pymitter import EventEmitter as Signal
import random
from functools import cmp_to_key

av_const: float = 10000.0 
game_event = Signal(wildcard=True)
battle_event = Signal()


class BattleState:
    IDLE        = "idle"        # battle not started
    PLAYER_TURN = "selecting"   # player choosing action
    ANIMATING   = "animating"   # skill/attack playing out
    PROGRESSING = "progressing"  # calculate current turns
    RESOLVING   = "resolving"   # trigger damage, deaths
    ENEMY_TURN  = "enemy_turn"  # enemy AI deciding
    # FINISHED    = "finished"


class EVENTS:
    class ENTITY:
        ACTION = "entity.action"            #para = caster, affects, main_target, mp_cost, mp_regen
        DIED = "entity.died"                #para = entity
        HURT = "entity.hurt"                #para = entity
        
    class BATTLE:
        START = "battle.started"
        PAUSE = "battle.pause"

        PLAYER_TURN = "battle.player_turn"  #para = hero
        ENEMY_TURN = "battle.enemy_turn"    #idk if needed

        FINISH_LOSE = "battle.finish_lose"
        FINISH_WIN = "battle.finish_win"

    class ANIMATION:     
        START = "battle.animation.start"    #para = Entity
        FINISH = "battle.animation.finish"  #para = None, for BattleManager to progress

    class UI:

        DAMAGE = "battle.ui.damage"         #para = total_damage
        STATUS = "battle.ui.status"         #para = Heroes, Enemies
        PREDICTION = "battle.ui.prediction" #para = turn_order_pred


#Rule of thumb when declaring class default variable
#Declare Child first, and then Parent
#Or just the Child, NOT THE OTHER WAY AROUND
#In other words, Default first, and then Non-default

# things to mention when making class with @classmethod
# 1. if there is a default value, its optional to init with your own value but not needed
# 2. if there is NOT a default value, you HAVE to assign it
# 3. Lists in Python are mutable, meaning they are shared across instances if initialized poorly. 
#    You must use a factory blueprint to separate them so different objects from the same blueprint stay isolated.
# 4. cls(**args) will need to assign every non-default var, but if the data is for run-time, hide it from __init__
#    meaning: remove it from __init__ parameter, or if you are using @dataclass, use field(init=False)
#
# @dataclass
# class ClassName:
#     varB: bool                                <--- this is non-default value, it must be at the top
#     varA: int = 10                            <--- this is default value
#     varC: list = field(default_factory=list)  <--- this makes list immutable
#     varD: str = field(init=False, default="") <--- this hides it when init, but need a default value
