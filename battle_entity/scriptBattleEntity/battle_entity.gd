class_name BattleEntity
extends Node3D

var data: EntityData
var data_predict: EntityData
var selection_enabled: bool = false

signal is_dead(self_: BattleEntity) #might not be needed, for animation
signal is_hurt(self_: BattleEntity)
signal anim_finished
#all other state for anim

#idk
func _ready() -> void:
	is_dead.connect(BattleManager._on_entity_died)
	is_hurt.connect(BattleManager._on_entity_hurt)

func _reapply_affect() -> void:
	for affect in data.active_affects:
		if affect.affect_type == "Tick" and affect.duration > 0:
			affect.execute_affect([self])


func tick_affects() -> void: # 1, trigger, 0, delete
	_reapply_affect()
	if data.cur_hp <= 0:
		anim_play_die()
		await anim_finished
		is_dead.emit(self)
		return
	var expired: Array[Affect] = []
	for affect: Affect in data.active_affects:
		affect.duration -= 1
		if affect.duration <= 0:
			expired.append(affect)
	
	for affect: Affect in expired:
		if affect.affect_type == "Static" and affect is not Offense:
			affect.revert_affect(self)
		data.active_affects.erase(affect)
	

func reset_after_death(hp: int = 100, mp: int = 20):
	data.cur_stats = data.base_stats.duplicate()
	data.saved_cur_hp = hp
	data.cur_hp = data.saved_cur_hp
	data.saved_cur_mp = mp
	data.cur_mp = data.saved_cur_mp
	

func reset_after_battle(hp: bool = false, mp: bool = false) -> void: #reset all stat from buffs
	data.cur_stats = data.base_stats.duplicate()
	if hp:
		data.saved_cur_hp = data.cur_stats.health
		data.cur_hp = data.saved_cur_hp
	if mp:
		data.saved_cur_mp = data.cur_stats.mana
		data.cur_mp = data.saved_cur_mp


func _on_area_3d_input_event(camera: Node, event: InputEvent, event_position: Vector3, normal: Vector3, shape_idx: int) -> void:
	if event is InputEventMouseButton and event.pressed:
		if selection_enabled:  # only if BattleManager allows it
			BattleManager.entity_selected.emit(self)

func anim_play_hurt():
	pass
	

func anim_play_die():
	pass
