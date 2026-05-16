extends Node


var tes_hero_data: HeroData = preload("res://battle_entity/hero/dataHero/cirno.tres")
var tes_enemy_data: EnemyData = preload("res://battle_entity/enemy/dataEnemy/enemy_is_bad.tres")

var active_hero: Array[Hero] = []
var group_enemy: Array[Enemy] = []

func _ready() -> void:
	var hero_node: Hero = tes_hero_data.scene.instantiate()
	hero_node.data = tes_hero_data
	add_child(hero_node)
	
	var enemy_node: Enemy = tes_enemy_data.scene.instantiate()
	enemy_node.data = tes_enemy_data
	add_child(enemy_node)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func start_battle() -> void:
	BattleManager.setup(active_hero, group_enemy)
