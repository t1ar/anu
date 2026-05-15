@abstract
class_name Defense
extends Affect

enum Target { SELF, SINGLE_ALLY, ALL_ALLIES }

@export var target_type: Target = Target.SELF

func resolve_targets(caster: BattleEntity, all_entities: Array[BattleEntity]) -> Array[BattleEntity]:
	var allies := all_entities.filter(func(e: BattleEntity): return e.team == caster.team)
	match target_type:
		Target.SELF:          return [caster]
		Target.SINGLE_ALLY:   return []  # BattleManager handles await
		Target.ALL_ALLIES:    return allies
	return []

func get_target_key() -> String:
	return Target.find_key(target_type) 
