extends Node

var tes_hero_data: HeroData = preload("res://battle_entity/hero/dataHero/cirno.tres")
var tes_enemy_data: EnemyData = preload("res://battle_entity/enemy/dataEnemy/enemy_is_bad.tres")

var active_hero_data: Array[HeroData] = []
var group_enemy_data: Array[EnemyData] = []
var scene_path: String = "res://battle/script/battle_scene.tscn"
var battle_instance: Node

func _ready() -> void:
	active_hero_data.append(tes_hero_data)
	group_enemy_data.append(tes_enemy_data)
	$field_scene.show()


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func start_battle(heros_data: Array[HeroData], enemies_data: Array[EnemyData]) -> void:
	var cur_battle_scene: PackedScene = load(scene_path)
	battle_instance = cur_battle_scene.instantiate()
	add_child(battle_instance)
	var heros_group: Array[Hero]
	var enemies_group: Array[Enemy]
	
	BattleManager.setup(heros_group, enemies_group)

func end_battle():
	battle_instance.queue_free()
	battle_instance = null
	pass


func _on_button_pressed() -> void:
	$battle_scene.show()
	$field_scene.hide()
	start_battle(active_hero_data, group_enemy_data)
