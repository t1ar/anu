class_name BattleEntity
extends Node

var data: EntityData

func _ready() -> void:
	if data == null:   # oi you forgot to set data before add_child()"
		push_error("data not set before add_child() on: " + name)
		return
	data.init_stat()

func _reapply_affect() -> void:
	data.stat = data.base_stat.duplicate()
	for affect in data.active_affects:
		if affect.affect_type == "Tick":
			affect.execute_affect(self)    

func tick_affects() -> void: # 1, trigger, 0, delete
	_reapply_affect()
	var expired: Array[Affect] = []
	for affect: Affect in data.active_affects:
		affect.duration -= 1
		if affect.duration <= 0:
			expired.append(affect)
	
	for affect: Affect in expired:
		data.active_affects.erase(affect)
		

func reset_after_death():
	pass

func reset_after_battle(hp: bool = false, mp: bool = false) -> void: #reset all stat from buffs
	data.cur_stats = data.base_stats.duplicate()
	if hp:
		data.saved_cur_hp = data.cur_stats.health
		data.cur_hp = data.saved_cur_hp
	if mp:
		data.saved_cur_mp = data.cur_stats.mana
		data.cur_mp = data.saved_cur_mp
