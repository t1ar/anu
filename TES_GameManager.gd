extends Node

var tes_hero_data: HeroData = preload("res://battle_entity/hero/dataHero/cirno.tres")
var tes_enemy_data: EnemyData = preload("res://battle_entity/enemy/dataEnemy/enemy_is_bad.tres")

var tes_hero_data2: HeroData = preload("res://battle_entity/hero/dataHero/chiruno2.tres")
var tes_enemy_data2: EnemyData = preload("res://battle_entity/enemy/dataEnemy/baddes_enemy_of_all.tres")

var tes_hero_data3: HeroData = preload("res://battle_entity/hero/dataHero/chironu.tres")
var tes_enemy_data3: EnemyData = preload("res://battle_entity/enemy/dataEnemy/enemy_is_very_verybad.tres")

var active_hero_data: Array[HeroData] = []
var group_enemy_data: Array[EnemyData] = []
var scene_path: String = "res://battle/script/battle_scene.tscn"
var battle_instance: Node

func _ready() -> void:
	active_hero_data.append(tes_hero_data)
	#active_hero_data.append(tes_hero_data2)
	active_hero_data.append(tes_hero_data3)
	
	
	group_enemy_data.append(tes_enemy_data)
	#group_enemy_data.append(tes_enemy_data2)
	#group_enemy_data.append(tes_enemy_data3)
	#$field_scene.show()

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func start_battle() -> void:
	var cur_battle_scene: PackedScene = load(scene_path)
	battle_instance = cur_battle_scene.instantiate()
	add_child(battle_instance)
	var heros_group: Array[Hero]
	var enemies_group: Array[Enemy]
	
	for h in active_hero_data:
		heros_group.append(h.spawn() as Hero)
	
	for e in group_enemy_data:
		enemies_group.append(e.spawn() as Enemy)
	
	BattleManager.setup(heros_group, enemies_group)

func end_battle():
	battle_instance.queue_free()
	battle_instance = null
	pass
