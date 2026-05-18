class_name EntityCondition
extends Resource

var advance: float = 0.0
var delay: float = 0.0
var shield_hp: int = 0
var damage_reduction: float = 0.0 #range 0 -> 0.9
var sleepy: bool = false #skip turn when self.action
var exhausted: bool = false #cant use skill that consume mp
var unseen: bool = false #cant be single-targeted
