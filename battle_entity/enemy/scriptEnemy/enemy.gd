class_name Enemy
extends BattleEntity


func _ready() -> void:
	super._ready()
	data.team = EntityData.Teams.ENEMY
