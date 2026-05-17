extends Node #Autoloads, check project settings global var

const av_const: float = 10000.0
var Heros_list: Array[Hero]
var Enemies_list: Array[Enemy]

var all_entities: Array[BattleEntity]
var alive_entities: Array[BattleEntity]
var cur_entity: BattleEntity

var turn_order_current: Array[BattleEntity]
var turn_order_prediction: Array[BattleEntity]
var target_entities: Array[BattleEntity]


var finished: bool = false
var exp_gain: int = 0

signal battle_startup
signal battle_cleanup
signal battle_progress
signal battle_player_turn
signal battle_enemy_turn
signal battle_entity_died(entity: BattleEntity)
signal battle_end

#cam signal
signal cam_target_selected(entity: BattleEntity) #target camera direction, idk if needed
signal cam_player_turn(hero: Hero) #display cam for hero and set pos based on hero.position
signal cam_player_select_all_allies
signal cam_enemy_turn #display cam for enemy_turn

#ui signal
signal ui_data(heroes: Array[Hero], enemies: Array[Enemy])
signal ui_target_selected(targets: Array[BattleEntity])
signal ui_confirmed_action(affects: Array[Affect])
signal ui_cur_hero(hero: Hero)
signal ui_prediction_changed(predict: Array[BattleEntity])
signal ui_stats_changed(all_alive_entity: Array[BattleEntity])

#signal usage flow,
#cam :	gets pos and direction
#ui :	gets data for what to display
#scene:	waits for ui selection
# battle_progress -> cam -> ui await hero turn -> scene await ui -> battle_progress, til finish


#calls when entering battle
func setup(Hero_group: Array[Hero], Enemy_group: Array[Enemy]) -> void:
	battle_end.connect(TesGameManager.end_battle)
	Heros_list = Hero_group
	Enemies_list = Enemy_group
	all_entities.assign(Heros_list + Enemies_list)
	alive_entities.assign(all_entities.filter(func(e: BattleEntity): return e.data.cur_hp > 0))
	
	_on_battle_ready()
	
	#connect inventory, its not here yet
	
	
	
	_progress()

func force_end_battle() -> void: #battle end premature via menu or smthng idk
	#dont save hero state
	pass

func _finish_battle() -> void:
	#disconnect inventory, anything with data cleaned, etc
	battle_cleanup.emit()
	
	#save hero state
	battle_end.emit()

func _on_battle_ready():
	battle_startup.emit()
	#start animation, placement, etc
	pass

func _get_order(current_alive: Array[BattleEntity]) -> Array[BattleEntity]:
	var new_order: Array[BattleEntity]
	new_order.assign(current_alive)
	new_order.sort_custom(func(a: BattleEntity, b: BattleEntity):
		if a.data.AV != b.data.AV:
			return a.data.AV < b.data.AV
			
		if a.data.team != b.data.team:
			return a.data.team == EntityData.Teams.HERO
			
		if a.data.stat.luck != b.data.stat.luck:
			return a.data.stat.luck > b.data.stat.luck
			
		return randi() % 2 == 0
	)
	
	return new_order

func _progress() -> void:
	if finished:
		_finish_battle()
		
	cur_entity = _get_order(alive_entities)[0]
	
	if cur_entity is Hero:
		cam_player_turn.emit(Heros_list.find(cur_entity as Hero)) #change cam
		ui_cur_hero.emit(cur_entity)
	
	if cur_entity is Enemy:
		cam_enemy_turn
	
	cur_entity.tick_affects()
	
	if cur_entity.data.cur_hp <= 0:
		if cur_entity is Hero:
			cur_entity.reset_after_death(100, 20)
		if cur_entity is Enemy:
			cur_entity.reset_after_death()
		alive_entities.erase(cur_entity)
		_update_progress()
	
	if cur_entity.data.sleepy:
		_update_progress()
	
	#all extra state on entity,
	
	
	
	
	#if OS.is_debug_build():
		#return  # ← stops after one turn in debug
		
	await battle_progress
	_update_progress()

func _update_progress():
	#send all important UI signal
	ui_stats_changed.emit(alive_entities)
	_progress()


func get_prediction_order(affects: Array[Affect], targets: Array[BattleEntity]):
	var new_prediction
	
	
	ui_prediction_changed.emit(new_prediction)
	pass
	

func on_item_used() -> void: #item: Item
	#get_target(item.affect_list)
	pass

func on_skill_used(skill: Skill) -> void:
	#get_target(skill.affect_list)
	pass

func get_target_type(item_or_skill: Array[Affect]) -> void:
	var targets: Array[BattleEntity]
	var picks: Array[BattleEntity]
	var already_picked: bool = false
	
	for affect in item_or_skill:
		targets = affect.resolve_targets(cur_entity, alive_entities)
		if targets.is_empty() and not already_picked:
			var key: String = affect.get_target_key()
			targets = await _pick_target_single(key)
			picks = targets
			already_picked = true
		else:
			targets = picks
	

func _pick_target_single(key: String) -> Array[BattleEntity]:
	var picked: BattleEntity
	if cur_entity in Heros_list:
		picked = await _player_pick(key)
	else: 
		picked = _ai_pick(key)
	return [picked]

func _player_pick(key: String) -> BattleEntity:
	var selected: BattleEntity
	if key == "SINGLE_ENEMY":
		var Enemies = alive_entities.filter(func(e: BattleEntity): return e.team != cur_entity.team)
		for e in Enemies:
			e.set_selectable(true)
		selected = await cam_target_selected
		for e in Enemies:
			e.set_selectable(false)
			
	elif key == "SINGLE_ALLY":
		var Allies = alive_entities.filter(func(e: BattleEntity): return e.team == cur_entity.team)
		for e in Allies:
			e.set_selectable(true)
		selected = await cam_target_selected
		for e in Allies:
			e.set_selectable(false)

	return selected

func _ai_pick(key: String) -> BattleEntity:
	var picked: BattleEntity
	#ai picking stuff, idk maybe based on aggro, low hp, etc
	
	return picked


func _apply_affect(affect: Affect, target: BattleEntity) -> void:
	pass
