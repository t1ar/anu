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
signal start_battle
signal finished_battle
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
	all_entities.assign(Heros_list + Enemies_list)
	alive_entities.assign(all_entities.filter(func(e: BattleEntity): return e.data.cur_hp > 0))
	
	_on_battle_ready()
	
	#connect inventory, its not here yet
	
	cam_current_turn.connect(BattleUI.change_cam)
	BattleUI.skill_used.connect(_on_skill_used)
	
	
	BattleUI.display_UI(Heros_list, Enemies_list, turn_order_current)
	
	
	start_battle.emit()
	_progress()

func cleanup() -> void:
	for e in all_entities:
		e.queue_free()
	#disconnect inventory
	cam_current_turn.disconnect(BattleUI.change_cam)
	BattleUI.skill_used.disconnect(_on_skill_used)
	
	
	finished_battle.emit()

func _on_battle_ready():
	#start animation, placement, etc
	pass

func _update_turn_order():
	pass

func _progress() -> void:
	if finished:
		cleanup()
	order_entities.assign(alive_entities)
	order_entities.sort_custom(func(a: BattleEntity, b: BattleEntity):
		if a.data.AV != b.data.AV:
			return a.data.AV < b.data.AV
			
		if a.data.team != b.data.team:
			return a.data.team == EntityData.Teams.HERO
			
		if a.data.stat.luck != b.data.stat.luck:
			return a.data.stat.luck > b.data.stat.luck
			
		return randi() % 2 == 0
	)
	cur_entity = order_entities[0]
	cur_entity.tick_affects()
	
	cam_current_turn.emit(Heros_list.find(cur_entity as Hero)) #change cam
	
	if cur_entity.data.cur_hp <= 0:
		cur_entity.reset_after_death()
		alive_entities.erase(cur_entity)
		_update_progress()
	
	if cur_entity.data.sleepy:
		_update_progress()
	
	if cur_entity in Heros_list:
		BattleUI.display_action(cur_entity)
	else:
		#ai movement
		pass
	
	
	print("ran succesfully")
	if OS.is_debug_build():
		return  # ← stops after one turn in debug
	_update_progress()

func _update_progress():
	#send all important UI signal
	_progress()


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
