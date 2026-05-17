class_name GameManager
extends Node
#not game manager, this is what GameManager would call when starting battle
#FOR CAM < use &x_scene/cam.make_current() to switch cams
var tes_hero_data: HeroData = preload("res://battle_entity/hero/dataHero/cirno.tres")
var tes_enemy_data: EnemyData = preload("res://battle_entity/enemy/dataEnemy/enemy_is_bad.tres")

var active_hero_data: Array[HeroData] = []
var group_enemy_data: Array[EnemyData] = []
var cur_battle_scene: PackedScene = "res://battle/script/battle_scene.tscn"

func _ready() -> void:
	active_hero_data.append(tes_hero_data)
	group_enemy_data.append(tes_enemy_data)
	$field_scene.show()


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func start_battle(heros_data: Array[HeroData], enemies_data: Array[EnemyData], scene: PackedScene) -> void:
	var heros_group: Array[Hero]	
	var enemies_group: Array[Enemy]
	
	for h in heros_data:
		var hero = h.spawn() as Hero
		heros_group.append(hero)
		scene.add_child(hero)
	$battle_anim/Entities
	for e in enemies_data:
		var enemy = e.spawn() as Enemy
		enemies_group.append(enemy)
		$battle_scene.add_child(enemy)
	
	BattleManager.setup(heros_group, enemies_group, scene)

func finish_battle():
	pass


func _on_button_pressed() -> void:
	$battle_scene.show()
	$field_scene.hide()
	start_battle(active_hero_data, group_enemy_data)
