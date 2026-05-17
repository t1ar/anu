# Combatant.gd
class_name Combatant
extends RefCounted

var actor_name: String
var max_hp: int
var current_hp: int
var max_mp: int
var current_mp: int
var attack: int
var defense: int
var speed: int
var skills: Array = []          # Array[SkillResource]
var status_effects: Array = []  # Array[StatusEffect]

func setup(data: ActorResource) -> void:
	actor_name = data.actor_name
	max_hp = data.max_hp
	current_hp = max_hp
	max_mp = data.max_mp
	current_mp = max_mp
	attack = data.attack
	defense = data.defense
	speed = data.speed
	skills = data.skills.duplicate()

func is_alive() -> bool:
	return current_hp > 0

func take_damage(amount: int) -> void:
	current_hp = max(0, current_hp - amount)

func heal(amount: int) -> void:
	current_hp = min(max_hp, current_hp + amount)

func tick_status_effects() -> void:
	for effect in status_effects:
		effect.tick(self)
	status_effects = status_effects.filter(func(e): return not e.is_expired())

func get_best_action():
	# enemies just pick their highest-power skill they can afford
	var affordable = skills.filter(func(s): return current_mp >= s.mp_cost)
	if affordable.is_empty():
		return skills[0]  # basic attack fallback
	affordable.sort_custom(func(a, b): return a.power > b.power)
	return affordable[0]
