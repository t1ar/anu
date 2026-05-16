class_name BattleEntity
extends Node

var data: EntityData

func _ready() -> void:
	if data == null:   # oi you forgot to set data before add_child()"
		push_error("data not set before add_child() on: " + name)
		return
	data.init_stat()


#func _recalculate_stats() -> void:
	#cur_stats = base_stats.duplicate()
	#for affect in active_affects:
		#affect.execute_affect(cur_stats)    

#func tick_affects() -> void:
	#for affect: Affect in active_affects.duplicate():
		#affect.duration -= 1
		#if affect.duration <= 0:
			#active_affects.erase(affect)
	#_recalculate_stats()

#func reset_after_battle(hp: bool = false, mp: bool = false) -> void: #reset all stat from buffs
	#cur_stats = base_stats.duplicate()
	#if hp:
		#saved_cur_hp = cur_stats.health
		#cur_hp = saved_cur_hp
	#if mp:
		#saved_cur_mp = cur_stats.mana
		#cur_mp = saved_cur_mp
