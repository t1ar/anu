extends Node

var Heros_list: Array[BattleEntity]
var Enemies_list: Array[BattleEntity]
var all_entities: Array[BattleEntity]
var alive_entities: Array[BattleEntity]
var order_entities: Array[BattleEntity]
var pred_entities: Array[BattleEntity]
var cur_entity: BattleEntity

signal target_selected(entity: BattleEntity)

#also input player.inventory (if needed)
func setup(Hero_list: Array[BattleEntity], Enemy_list: Array[BattleEntity]) -> void:
	Heros_list = Hero_list
	Enemies_list = Enemy_list
	all_entities = Hero_list + Enemy_list
	alive_entities = all_entities
	for entity in all_entities:
		entity.skill_used.connect(_on_skill_used)

func cleanup() -> void:
	for entity in all_entities:
		entity.skill_used.disconnect(_on_skill_used)

#func _ready() -> void:
	#pass

#func _process(delta: float) -> void:
	#pass

func progress() -> void:
	pass


func _on_skill_used(caster: BattleEntity, skill: Skill) -> void:
	var targets: Array[BattleEntity]
	for a in skill.affect_list:
		targets = a.resolve_targets(caster, alive_entities)
		if targets.is_empty():
			var key: String = a.get_target_key()
			targets = await _pick_target_single(caster, key)
		a.apply_to(targets)


func _pick_target_single(caster: BattleEntity, type: String) -> Array[BattleEntity]:
	if caster in Heros_list:
		var picked := await _player_pick(caster, type)
		return [picked]
	else: 
		return [_ai_pick(caster)]

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

func _ai_pick(caster: BattleEntity) -> BattleEntity:
	var picked: BattleEntity
	
	
	return picked
