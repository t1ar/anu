extends Node


func _ready():
	BattleManager.scene_spawn_hero.connect(_on_hero_spawned)
	BattleManager.scene_spawn_enemy.connect(_on_enemy_spawned)
	BattleManager.battle_entity_died.connect(_on_remove_enemy)
	BattleManager.battle_end.connect(_on_cleanup)

func _on_hero_spawned(hero_group: Array[Hero]):
	if hero_group.size() == 1:
		$battle_anim/Entities.add_child(hero_group[0])
		hero_group[0].global_position = $"Hero_pos/3p-2 or 1p".global_position
	
	elif hero_group.size() == 2:
		$battle_anim/Entities.add_child(hero_group[0])
		hero_group[0].global_position = $"Hero_pos/2p-1".global_position
		$battle_anim/Entities.add_child(hero_group[1])
		hero_group[1].global_position = $"Hero_pos/2p-2".global_position
	
	elif hero_group.size() == 3:
		$battle_anim/Entities.add_child(hero_group[0])
		hero_group[0].global_position = $"Hero_pos/3p-1".global_position
		$battle_anim/Entities.add_child(hero_group[1])
		hero_group[1].global_position = $"Hero_pos/3p-2 or 1p".global_position
		$battle_anim/Entities.add_child(hero_group[2])
		hero_group[2].global_position = $"Hero_pos/3p-3".global_position

func _on_enemy_spawned(enemy_group: Array[Enemy]):
	if enemy_group.size() == 1:
		$battle_anim/Entities.add_child(enemy_group[0])
		enemy_group[0].global_position = $"Enemy_pos/3p-2 or 1p".global_position
	
	elif enemy_group.size() == 2:
		$battle_anim/Entities.add_child(enemy_group[0])
		enemy_group[0].global_position = $"Enemy_pos/2p-1".global_position
		$battle_anim/Entities.add_child(enemy_group[1])
		enemy_group[1].global_position = $"Enemy_pos/2p-2".global_position
	
	elif enemy_group.size() == 3:
		$battle_anim/Entities.add_child(enemy_group[0])
		enemy_group[0].global_position = $"Enemy_pos/3p-1".global_position
		$battle_anim/Entities.add_child(enemy_group[1])
		enemy_group[1].global_position = $"Enemy_pos/3p-2 or 1p".global_position
		$battle_anim/Entities.add_child(enemy_group[2])
		enemy_group[2].global_position = $"Enemy_pos/3p-3".global_position
	
	BattleManager.scene_startup.emit()

func _on_remove_enemy(enemy: Enemy, new_group_enemy: Array[Enemy]):
	enemy.queue_free()
	_reposition_enemy(new_group_enemy)

func _reposition_enemy(enemy_group: Array[Enemy]):
	if enemy_group.size() == 1:
		enemy_group[0].global_position = $"Enemy_pos/3p-2 or 1p".global_position
	
	elif enemy_group.size() == 2:
		enemy_group[0].global_position = $"Enemy_pos/2p-1".global_position
		enemy_group[1].global_position = $"Enemy_pos/2p-2".global_position
	
	elif enemy_group.size() == 3:
		enemy_group[0].global_position = $"Enemy_pos/3p-1".global_position
		enemy_group[1].global_position = $"Enemy_pos/3p-2 or 1p".global_position
		enemy_group[2].global_position = $"Enemy_pos/3p-3".global_position

func _on_cleanup():
	for child in $battle_anim/Entities.get_children():
		child.queue_free()
