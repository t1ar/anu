class_name Skill
extends Resource

@export_group("Details")
@export var skill_name: String = ""

@export_enum("Physical_Attack", "Magical_Attack", "Effect") var icon_type: String = "Physical_Attack"
@export_enum("Physical", "Magic") var element: String = ""
@export_enum( "SELF", "SINGLE_ALLY", "ALL_ALLIES", "SINGLE_ENEMY", "ALL_ENEMIES" ) var main_target: String = "SELF"
#actual target the skill points to for cam

@export_range(0, 100) var success_rate: int = 100
@export_range(0, 50) var mp_cost: int = 15
@export_range(0, 50) var mp_regen: int = 0
@export var scene: PackedScene
@export_enum("Static", "Cinematic") var scene_type: String = "Static"

@export_group("Affect(s)")
@export var Offensive: Array[Offense] = []:
	set(value):
		Offensive = value
		_update_affect_list()

@export var Defensive: Array[Defense] = []:
	set(value):
		Defensive = value
		_update_affect_list()

@export var Supportive: Array[Support] = []:
	set(value):
		Supportive = value
		_update_affect_list()


var affect_list: Array[Affect] = []

func _update_affect_list() -> void:
	affect_list.assign(Offensive + Defensive + Supportive)
