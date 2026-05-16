extends Node

const av_const: float = 10000.0
var Heros_list: Array[Hero]
var Enemies_list: Array[Enemy]

var all_entities: Array[BattleEntity]
var alive_entities: Array[BattleEntity]

var order_entities: Array[BattleEntity]
var cur_entity: BattleEntity

var turn_order_current: Array[BattleEntity]
var turn_order_prediction: Array[BattleEntity]
var target_entities: Array[BattleEntity]

var finished: bool = false
var exp_gain: int = 0

#cam signal
signal cam_target_selected(entity: BattleEntity) #target camera direction, emit from UI
signal cam_current_turn(hero_idx: int) #display UI for hero and set pos, 0: mid, 1: right, 2: left, -1: default (not in Hero_list)

#scene signal
signal scene_entity_skill(caster: BattleEntity, skill: Skill)
#signal scene_enemy_skill(caster: Enemy, skill: Skill) #display scene with Entity + skill / item, 
#signal scene_player_skill(caster: Hero, skill: Skill) # fixed pos (can change if u want)
signal scene_player_item(caster: Hero) #, item: Item)
signal scene_finished_anim

#ui signal

signal ui_selected_affect(affects: Array[Affect]) # both 
#signal ui_skill(skill: Skill)
#signal ui_inventory(caster: Hero)
signal ui_escape
signal prediction_changed
signal stats_updated

#calls when entering battle
#also input player.inventory to connect
#and current turn to camera
func setup(Hero_group: Array[Hero], Enemy_group: Array[Enemy]) -> void:
	Heros_list = Hero_group
	Enemies_list = Enemy_group
	all_entities = Hero_group + Enemy_group
	alive_entities = all_entities.filter(func(e: BattleEntity): return e.cur_hp > 0)
	
	#connect inventory, its not here yet
	
	cam_current_turn.connect(BattleUI.change_cam)
	BattleUI.skill_used.connect(_on_skill_used)
	
	
	BattleUI.display_UI(Hero_group, Enemy_group, turn_order_current)

func cleanup() -> void:
	#disconnect inventory
	cam_current_turn.disconnect(BattleUI.change_cam)
	BattleUI.skill_used.disconnect(_on_skill_used)

func _update_turn_order():
	pass

func progress() -> void:
	if finished:
		cleanup()
	order_entities = alive_entities.duplicate()
	order_entities.sort_custom(func(a: BattleEntity, b: BattleEntity): return a.cur_stats.AV < b.cur_stats.AV )
	cur_entity = order_entities[0]
	cur_entity.tick_affects()
	
	cam_current_turn.emit(Heros_list.find(cur_entity)) #change cam
	
	if cur_entity in Heros_list:
		BattleUI.display_action(cur_entity)
	else:
		#ai movement
		pass
	
	
	


func _on_item_used() -> void: #item: Item
	#get_target(item.affect_list)
	pass

func _on_skill_used(skill: Skill) -> void:
	#get_target(skill.affect_list)
	pass


func _predict_order(affect: Support):
	pass

func get_target(item_or_skill: Array[Affect]) -> void:
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
		affect.apply_to(targets)
		
		if affect is Support:
			_predict_order(affect)
	
	stats_updated.emit()

func _apply_affect(affect: Affect, target: BattleEntity) -> void:
	pass


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
