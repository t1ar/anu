#this is python compiler setting, use directly in files
# from __future__ import annotations , basically stringify all your annotation
# for e.g, def func() -> type(self), now turns to def func() -> "type(self)"
# used to avoid class undefined typing crash, like:
# for @classmethod, you return itself, but its not defined yet
# this is useful if ur lazy like me and dont want to stringify it manually
# only for python 3.13 and below
#
# and use TYPE_CHECKING for if you want to import class for autocompletion but avoid import loop

#dataclass to skip typing __init__() for instancing a new object, and also makes a new default def __post_init__()
#field to tell python what to do to the self.fields behaviour, like init, default value, etc 
from dataclasses import dataclass, field 
from typing import List, Dict, Any, TYPE_CHECKING
from pathlib import Path
from abc import ABC, abstractmethod
from copy import deepcopy, copy # try to not use deepcopy, very bad for performance
from enum import Enum, auto
from pymitter import EventEmitter as Signal

av_const: float = 10000.0 
game_event = Signal(wildcard=True)
battle_event = Signal()


class BattleState(Enum):
    IDLE        = "idle"        # battle not started
    SELECTING   = "selecting"   # player choosing action
    ANIMATING   = "animating"   # skill/attack playing out
    PROGRESSING = "progressing"  # calculate current turns
    RESOLVING   = "resolving"   # trigger damage, deaths
    ENEMY_TURN  = "enemy_turn"  # enemy AI deciding
    FINISHED    = "finished"


class EVENTS:
    class ENTITY:
        DIED = "entity.died"
        HURT = "entity.hurt"
        
    class BATTLE:
        STARTED = "battle.started"
        ANIMATION_START = "battle.animation_start"
        ANIMATION_FINISH = "battle.animation_finish"
        ENDED = "battle.ended"

#Rule of thumb when declaring class default variable
#Declare Child first, and then Parent
#Or just the Child, NOT THE OTHER WAY AROUND

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
#     varB: bool                                  <--- this is non-default value, it must be at the top
#     varA: int = 10                              <--- this is default value
#     varC: list = field(default_factory=list)   <--- this makes list immutable 
#     varD: str = field(init=False, default="") <--- this hides it when init, but need a default value
