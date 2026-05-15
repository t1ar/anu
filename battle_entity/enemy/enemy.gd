class_name Enemy
extends BattleEntity

@export var exp_gain: int = 30

func _init() -> void:
	team = BattleEntity.teams.ENEMY
