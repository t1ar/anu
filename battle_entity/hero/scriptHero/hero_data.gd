class_name HeroData
extends EntityData

@export var current_exp: int = 0

@export_storage() var exp_to_lvl_up: int = 100
@export_storage() var is_dead: bool = false

func _init() -> void:
	team = EntityData.Teams.HERO
