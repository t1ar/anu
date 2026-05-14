extends Node
var active_hero: Array[BattleEntity] = [load("res://battle_entity/data/hero/Entity1.tres")]
var group_enemy: Array[BattleEntity] = [load("res://battle_entity/data/enemy/Entity2.tres")]
#var scene, etc

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func start_battle() -> void:
	BattleManager.setup(active_hero, group_enemy)
