class_name EntityData
extends Resource

@export_group("Details")
@export var character_name: String = ""
@export var backstory: String = ""
@export var scene: PackedScene
@export var eyeshot: Texture2D

@export_group("", "")
@export var skill_list: Array[Skill] = []
#static reference, update level for save file
@export var base_stat: EntityStat = EntityStat.new()

@export_storage var saved_cur_hp: int
@export_storage var saved_cur_mp: int
@export_storage var is_initialized: bool = false 

var cur_hp: int
var cur_mp: int

enum Teams { HERO, ENEMY }
var team: Teams

var stat: EntityStat #run-time update

var AV: float

#all stat(tick) affect here, add, subr, mulp each turn
var active_affects: Array[Affect] = []

#all special(static- One-time appliant) affect here, turn manipulation, shield, etc
var active_condition: EntityCondition = EntityCondition.new()

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
	init_stat()
	node.data = self
	var pred: EntityData = duplicate(false) #dont copy unnecesarry ahh
	#pred.active_affects = active_affects.duplicate(true) #not needed since its always 0 at start
	#pred.active_condition = active_condition.duplicate(true) #not needed since its always 0 at start
	pred.cur_hp = cur_hp
	#pred.cur_mp = cur_mp #not needed, pred only care about hp, AV when sorting
	pred.stat = stat.duplicate()
	pred.stat.speed = stat.speed
	pred.stat.luck = stat.luck
	pred.AV = AV
	node.data_predict = pred #.duplicate(true) doesnt dupe 
	return node

func reset_av() -> float:
	AV = 10000.0 / stat.speed
	AV += AV * active_condition.delay
	AV -= AV * active_condition.advance
	AV = maxf(AV, 0.0)
	return AV
