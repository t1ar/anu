class_name EntityStat
extends Resource

@export var level: int = 1
@export_group("Base Stats (Level 1)", "base_")
@export var base_health: int = 1000
@export var base_mana: int = 100
@export var base_strength: int = 30 
@export var base_defense: int = 30
@export var base_speed: int = 100
@export var base_luck: int = 100

@export_group("Growth Rates")
@export var health_growth: float = 1.1
@export var mana_growth: float = 1.05
@export var strength_growth: float = 1.08
@export var defense_growth: float = 1.08
@export var speed_growth: float = 1.03
@export var luck_growth: float = 1.03

var health: int
var mana: int
var strength: int
var defense: int
var speed: int
var luck: int


func update_to_level() -> void:
	health   = int(base_health   * pow(health_growth,   level - 1))
	mana     = int(base_mana     * pow(mana_growth,     level - 1))
	strength = int(base_strength * pow(strength_growth, level - 1))
	defense  = int(base_defense  * pow(defense_growth,  level - 1))
	speed    = int(base_speed    * pow(speed_growth,    level - 1))
	luck     = int(base_luck     * pow(luck_growth,     level - 1))
