class_name EntityData
extends Resource

@export_group("Details")
@export var character_name: String = ""
@export var backstory: String = ""
@export var scene: PackedScene

@export_group("", "")
@export var skill_list: Array[Skill] = []

@export var base_stat: EntityStat #static reference, update level for save file

@export_storage var saved_cur_hp: int
@export_storage var saved_cur_mp: int
@export_storage var is_initialized: bool = false 

var cur_hp: int
var cur_mp: int

enum Teams { HERO, ENEMY }
var team: Teams

var stat: EntityStat #run-time update
var stat_prediction: EntityStat

var AV: float

#all stat(tick) affect here, add, subr, mulp each turn
var active_affects: Array[Affect] = []

#all special(static) affect here, turn manipulation, shield, etc
var shield_hp: int = 0
var damage_reduction: float = 0.0 #range 0 -> 0.9
var sleepy: bool = false #skip turn when self.action
var exhausted: bool = false #cant use skill that consume mp
var unseen: bool = false #cant be single-targeted

func init_stat() -> void:
	base_stat.update_to_level()
	stat = base_stat.duplicate()
	stat.update_to_level()
	
	AV = BattleManager.av_const / stat.speed
	
	if not is_initialized: # first time only — set from max
		saved_cur_hp = stat.health
		saved_cur_mp = stat.mana
		is_initialized = true
	cur_hp = saved_cur_hp
	cur_mp = saved_cur_mp

func spawn() -> BattleEntity:
	var node: BattleEntity = scene.instantiate()
	node.data = self
	return node
