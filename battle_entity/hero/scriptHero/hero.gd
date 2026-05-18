class_name Hero
extends BattleEntity


func _ready() -> void:
	super._ready()
	data.team = EntityData.Teams.HERO

func level_up():
	pass
