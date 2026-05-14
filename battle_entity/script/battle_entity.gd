class_name BattleEntity
extends Resource

@export_group("Details")
@export var name: String = ""
enum teams { HERO, ENEMY}
@export var team: teams
#@export models, animation, etc

@export_group("", "")
@export var base_stats: EntityStat: 
	set(value):
		base_stats = value
		base_stats.update()
		cur_stats = base_stats.duplicate()
		cur_hp = cur_stats.health
		cur_mp = cur_stats.health

@export var skill_list: Array[Skill] = []

var cur_stats: EntityStat
var cur_hp: int
var cur_mp: int

signal skill_used(caster: BattleEntity, skill: Skill)

func use_skill(skill: Skill) -> void:
	skill_used.emit(self, skill)

func reset_after_battle(full: bool = false) -> void: #reset all stat from buffs, full = include hp & mp
	cur_stats = base_stats.duplicate()
	if full:
		cur_hp = cur_stats.health
		cur_mp = cur_stats.mana
