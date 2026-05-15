class_name EntityStat
extends Resource

@export var level: int = 1

@export_group("Base Stats (Level 1)")
@export var health: int = 1000
@export var mana: int = 100
@export var strength: int = 30 
@export var defense: int = 30
@export var speed: int = 100
@export var luck: int = 100

@export_group("Growth Rates")
@export var health_growth: float = 1.1
@export var mana_growth: float = 1.05
@export var strength_growth: float = 1.08
@export var defense_growth: float = 1.08
@export var speed_growth: float = 1.03
@export var luck_growth: float = 1.03

var AV: float
var shield_hp: int = 0

func update() -> void: #used off-battle or when starting battle
	health   = int(health   * pow(health_growth,   level - 1))
	mana     = int(mana     * pow(mana_growth,     level - 1))
	strength = int(strength * pow(strength_growth, level - 1))
	defense  = int(defense  * pow(defense_growth,  level - 1))
	speed    = int(speed    * pow(speed_growth,    level - 1))
	luck     = int(luck     * pow(luck_growth,     level - 1))
	AV = BattleManager.av_const / speed
