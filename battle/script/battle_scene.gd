extends Node

@onready var entities = $battle_anim/Entities


func _ready():
	BattleManager.scene_spawned_entity.connect(_on_entity_spawned)
	BattleManager.battle_cleanup.connect(_cleanup)

func _on_entity_spawned(entity_group: Array[BattleEntity]):
	for e in entity_group:
		entities.add_child(e)

func _cleanup():
	pass
