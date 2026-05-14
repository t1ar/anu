@abstract
class_name Offense
extends Affect

enum Target { SINGLE_ENEMY, ALL_ENEMIES }

@export var target_type: Target = Target.SINGLE_ENEMY

func resolve_targets(caster: BattleEntity, all_entities: Array[BattleEntity]) -> Array[BattleEntity]:
	var enemies := all_entities.filter(func(e: BattleEntity): return e.team != caster.team)
	match target_type:
		Target.SINGLE_ENEMY:  return []  # BattleManager handles await
		Target.ALL_ENEMIES:   return enemies
	return []

func get_target_key() -> String:
	return Target.find_key(target_type) 
