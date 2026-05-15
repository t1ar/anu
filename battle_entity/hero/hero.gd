class_name Hero
extends BattleEntity


@export var exp: int = 0


@export_storage() var exp_to_lvl_up: int = 100
@export_storage() var is_dead: bool = false


func _init() -> void:
	team = BattleEntity.teams.HERO

func level_up():
	pass
