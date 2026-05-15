@abstract
class_name BattleEntity
extends Resource

@export_group("Details")
@export var name: String = ""

enum teams { HERO, ENEMY }
var team: teams
#@export models, animation, etc

@export_group("", "")
@export var skill_list: Array[Skill] = []

@export var base_stats: EntityStat: 
	set(value):
		base_stats = value
		base_stats.update()
		cur_stats = base_stats.duplicate()

@export_storage() var saved_cur_hp: int
@export_storage() var saved_cur_mp: int

var cur_stats: EntityStat
var cur_hp: int = saved_cur_hp
var cur_mp: int = saved_cur_mp
var active_affects: Array[Affect] = []

func _recalculate_stats() -> void:
	cur_stats = base_stats.duplicate()
	for affect in active_affects:
		affect.execute_affect(cur_stats)    

func tick_affects() -> void:
	for affect: Affect in active_affects.duplicate():
		affect.duration -= 1
		if affect.duration <= 0:
			active_affects.erase(affect)
	_recalculate_stats()

func reset_after_battle(hp: bool = false, mp: bool = false) -> void: #reset all stat from buffs
	cur_stats = base_stats.duplicate()
	if hp:
		saved_cur_hp = cur_stats.health
		cur_hp = saved_cur_hp
	if mp:
		saved_cur_mp = cur_stats.mana
		cur_mp = saved_cur_mp
