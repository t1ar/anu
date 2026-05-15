extends Node

const av_const: int = 10000
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

signal ui_selected_affect(affects: Array[Affect])
signal ui_skill(skill: Skill)
signal ui_inventory(caster: Hero)
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
		BattleUI.display_action()
	else:
		#ai movement
		pass
	
	
	


func _on_item_used(): #item: Item
	#_apply_effect(caster, item.affect_list)
	pass

func _on_skill_used(caster: BattleEntity, skill: Skill) -> void:
	_apply_effect(caster, skill.affect_list)


func _predict_order(affect: Support):
	pass

func _apply_effect(caster: Hero, affect_list: Array[Affect]) -> void:
	var targets: Array[BattleEntity]
	var picks: Array[BattleEntity]
	var already_picked: bool = false
	
	for a in affect_list:
		targets = a.resolve_targets(caster, alive_entities)
		if targets.is_empty() and not already_picked:
			var key: String = a.get_target_key()
			targets = await _pick_target_single(caster, key)
			picks = targets
			already_picked = true
		else:
			targets = picks
		a.apply_to(targets)
		
		if a is Support:
			_predict_order(a)
	
	stats_updated.emit()


func _pick_target_single(caster: BattleEntity, key: String) -> Array[BattleEntity]:
	var picked: BattleEntity
	if caster in Heros_list:
		picked = await _player_pick(caster, key)
	else: 
		picked = _ai_pick(caster, key)
	return [picked]

func _player_pick(caster: BattleEntity, type: String) -> BattleEntity:
	var picked: BattleEntity
	if type == "SINGLE_ENEMY":
		var Enemies = alive_entities.filter(func(e: BattleEntity): return e.team != caster.team)
		for e in Enemies:
			e.set_selectable(true)
		picked = await target_selected
		for e in Enemies:
			e.set_selectable(false)
			
	elif type == "SINGLE_ALLY":
		var Allies = alive_entities.filter(func(e: BattleEntity): return e.team == caster.team)
		for e in Allies:
			e.set_selectable(true)
		picked = await target_selected
		for e in Allies:
			e.set_selectable(false)

	return picked

func _ai_pick(caster: BattleEntity, key: String) -> BattleEntity:
	var picked: BattleEntity
	#ai picking stuff, idk maybe based on aggro, low hp, etc
	
	return picked
