extends Node

var tes_hero_data = preload("res://battle_entity/hero/data/hero1.tres")
var tes_enemy_data = preload("res://battle_entity/enemy/data/enemy1.tres")

var active_hero: Array[Hero] = []
var group_enemy: Array[Enemy] = []

func _ready() -> void:
	var hero_node = tes_hero_data.scene.instantiate()
	add_child(hero_node)
	
	var enemy_node = tes_enemy_data.scene.instantiate()
	add_child(enemy_node)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func start_battle() -> void:
	BattleManager.setup(active_hero, group_enemy)
