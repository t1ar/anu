extends Node #Autoloads, check project settings global var

const av_const: float = 10000.0
var Heros_list: Array[Hero]
var Enemies_list: Array[Enemy]

var all_entities: Array[BattleEntity]
var alive_entities: Array[BattleEntity]
var cur_entity: BattleEntity

var turn_order_current: Array[BattleEntity] #for when wanting to update progress
var turn_order_prediction: Array[BattleEntity] #for UI

var finished: bool = false
var exp_gain: int = 0

signal battle_startup
signal battle_cleanup
signal battle_progress
signal battle_end

#scene signal
signal scene_spawn_enemy(Enemies: Array[Enemy])
signal scene_spawn_hero(Heroes: Array[Hero])
signal scene_enemy_died(enemy: Enemy, new_list: Array[Enemy])
signal scene_startup

#cam signal

signal cam_player_turn(hero: Hero) #display cam for hero and set pos based on hero.position
signal cam_enemy_turn #display cam for enemy_turn
signal cam_finished

#ui signal
signal ui_data(heroes: Array[Hero], enemies: Array[Enemy]) # trigger update for scalable static UI (hp Bar)
#signal ui_target_selected(targets: Array[BattleEntity])
#signal ui_confirmed_action(action: Array[Affect], targets: Array[BattleEntity])
signal ui_cur_hero(hero: Hero)#  whenn confirmed action Hero ui hides via UI's decision
signal ui_prediction_changed(predict: Array[BattleEntity], preview: Array[BattleEntity])
signal ui_stats_changed(all_alive_entity: Array[BattleEntity])

#signal usage flow,
#cam :	gets pos and direction
#ui :	gets data for what to display
#scene:	waits for ui selection
# battle_progress -> cam -> ui await hero turn -> scene await ui -> battle_progress await anim, til finish


#calls when entering battle
func setup(Hero_group: Array[Hero], Enemy_group: Array[Enemy]) -> void:
	battle_end.connect(TesGameManager.end_battle)
	Heros_list = Hero_group
	Enemies_list = Enemy_group
	
	for e: Enemy in Enemy_group:
		exp_gain += (e.data as EnemyData).exp_gain
	
	all_entities.assign(Heros_list + Enemies_list)
	alive_entities.assign(all_entities.filter(func(e: BattleEntity): return e.data.cur_hp > 0))
	
	#connect inventory, its not here yet, or might be useless, just use GameManager data directly
	
	_on_battle_ready()
	_progress()

func _on_battle_ready():  #could be used as wave mechanism too
	battle_startup.emit() #send signal to scene loading screen
	#start animation, placement, etc
	scene_spawn_hero.emit(Heros_list)
	scene_spawn_enemy.emit(Enemies_list) # at the end of spawning enemy, emit startup
	await scene_startup #wait for scene loading screen to finish
	

func _on_force_end_battle() -> void: #battle end premature via escape menu or smthng idk
	finished = true
	battle_cleanup.emit()
	#dont save hero state
	for h in Heros_list:
		h.reset_after_battle()
	for e in Enemies_list:
		e.reset_after_battle(true, true)
	battle_end.emit()
	

func _on_lose_battle() -> void:
	finished = true
	battle_cleanup.emit()
	#for h in Heros_list: should already been reset in _on_entity_dead
		#h.reset_after_death()
	#save hero state
	battle_end.emit()
	

func _on_finish_battle() -> void: #can be used for Escape, or winning
	finished = true
	#disconnect inventory, anything with data cleaned, etc
	battle_cleanup.emit()
	for h in Heros_list:
		h.reset_after_battle()
	for e in Enemies_list:
		e.reset_after_battle(true, true)
	#save hero state
	battle_end.emit()
	

#trigger death_signal from BattleEntity
func _on_entity_died(entity: BattleEntity): 
	alive_entities.erase(entity)
	_update_all_order()
	if entity is Hero:
		
		entity.reset_after_death()
		#Hero doesnt get removed from scene, incase y'all want a reviving spell
	elif entity is Enemy:
		Enemies_list.erase(entity)
		
		entity.reset_after_battle(true, true)
		scene_enemy_died.emit(entity as Enemy, Enemies_list) #remove from scene
	ui_data.emit(Heros_list, Enemies_list) #send lists for update
	ui_stats_changed.emit(alive_entities) #update stat

func _on_entity_hurt(): #might be useless, _update_progress already handle stat changes
	pass

#called via menu during preview skill
func _on_update_prediction_order(affects: Array[Affect], caster: Hero, targets: Array[BattleEntity]) -> void:
	for e in alive_entities:
		e.data_predict = e.data.duplicate(true)
	
	for a: Affect in affects:
		a.predict_affect(caster, targets)
	
	var preview_alive = alive_entities.filter(func(e: BattleEntity):
		return e.data_predict.cur_hp > 0)
	
	var av_pred: Dictionary = {}
	for e in preview_alive:
		av_pred[e] = e.data_predict.AV
	
	var turn_order_preview: Array[BattleEntity] = preview_alive.duplicate(true)
	while turn_order_preview.size() < 10:
		_add_prediction_order(turn_order_preview, av_pred)
	
	ui_prediction_changed.emit(turn_order_prediction, turn_order_preview)

func _get_cur_order(current_alive: Array[BattleEntity]) -> Array[BattleEntity]:
	var new_order: Array[BattleEntity]
	new_order = current_alive.duplicate()
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

func _add_prediction_order(last_prediction: Array[BattleEntity], av_sim: Dictionary) -> void:
	var entities = av_sim.keys()  # derive entity list from the dict itself
	entities.sort_custom(func(a: BattleEntity, b: BattleEntity):
		if av_sim[a] != av_sim[b]:
			return av_sim[a] < av_sim[b]
		
		if a.data.team != b.data.team:
			return a.data.team == EntityData.Teams.HERO
		
		if a.data_predict.stat.luck != b.data_predict.stat.luck:
			return a.data_predict.stat.luck > b.data_predict.stat.luck
		
		return randi() % 2 == 0)
	
	var lowest_av: float = av_sim[entities[0]]
	
	for e in entities:
		av_sim[e] -= lowest_av
	#reset av_sim[0]
	av_sim[entities[0]] = 10000.0 / entities[0].data_predict.stat.speed
	#append on array
	last_prediction.append(entities[0])

func _update_all_order():
	turn_order_current = _get_cur_order(alive_entities)
	
	var av_sim: Dictionary = {}
	for e in turn_order_current:
		av_sim[e] = e.data.AV  # purely local simulation
	
	turn_order_prediction = turn_order_current.duplicate()
	while turn_order_prediction.size() < 10:
		_add_prediction_order(turn_order_prediction, av_sim)

func _update_cam():
	if cur_entity is Hero:
		cam_player_turn.emit(Heros_list.find(cur_entity as Hero)) #change cam
	
	if cur_entity is Enemy:
		cam_enemy_turn.emit()

func _progress() -> void:
	if finished:
		return
	
	_update_all_order()
	ui_prediction_changed.emit(turn_order_prediction)
	
	#debug
	for e in turn_order_prediction:
		print("Prediction for next turn: ", e.data.character_name, " HERO" if e.data.team == 0 else " ENEMY")
	
	cur_entity = turn_order_current[0]
	
	_update_cam()
	
	cur_entity.tick_affects()

	if cur_entity not in alive_entities: #if entity died from tick affect
		_progress() #reset progress, entity doesnt exist,
		return
	
	if cur_entity.data.active_condition.sleepy:
		_update_progress()
		return
	
	#all extra state on entity, idk
	
	await cam_finished #wait for cam choreography , idk if y'all want
	
	if cur_entity is Hero:
		ui_cur_hero.emit(cur_entity as Hero) #tell to UI to show with hero data
	
	#if cur_entity is Hero calls apply_action directly from BattleUI via signal
	if cur_entity is Enemy:
		var skill: Skill = (cur_entity as Enemy).ai_skill_choice()
		var targets: Array[BattleEntity] = (cur_entity as Enemy).ai_target_choice()
		apply_action(cur_entity, targets, skill.affect_list)
	
	await battle_progress # wait for animation finished
	_update_progress()

func _update_progress():
	for i in range(1, turn_order_current.size()):
		turn_order_current[i].data.AV -= cur_entity.data.AV
		turn_order_current[i].data_predict = turn_order_current[i].data.duplicate(true)
	cur_entity.data.reset_av()
	cur_entity.data_predict = cur_entity.data.duplicate(true)
	
	ui_stats_changed.emit(all_entities) #or alive entities, idk 
	_progress()

func apply_action(caster: BattleEntity, targets: Array[BattleEntity], item_or_skill: Array[Affect]):
	for a in item_or_skill:
		a.apply_to(caster, targets)

func _on_item_used() -> void: #item: Item
	#get_target_type(item.affect_list)
	pass

func _on_skill_used(skill: Skill) -> void:
	#get_target_type(skill.affect_list)
	pass

#for ui selection mode
func get_selectable(item_or_skill: Array[Affect], targets: Array[BattleEntity]):
	#first on ui, on either skill or item, get the .main_target type, 
	#if type == "SINGLE" enemy or ally 
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
		#selected = await cam_target_selected
		for e in Enemies:
			e.set_selectable(false)
			
	elif key == "SINGLE_ALLY":
		var Allies = alive_entities.filter(func(e: BattleEntity): return e.team == cur_entity.team)
		for e in Allies:
			e.set_selectable(true)
		#selected = await cam_target_selected
		for e in Allies:
			e.set_selectable(false)

	return selected

func _ai_pick(key: String) -> BattleEntity:
	var picked: BattleEntity
	#ai picking stuff, idk maybe based on aggro, low hp, etc
	
	return picked
