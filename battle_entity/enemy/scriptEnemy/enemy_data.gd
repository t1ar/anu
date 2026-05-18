class_name EnemyData
extends EntityData

@export var exp_gain: int = 30

func _init() -> void:
	team = EnemyData.Teams.ENEMY
