@abstract
class_name Affect
extends Resource

@export var duration: int = 0  # 0 = instant

func apply_to(targets: Array[BattleEntity]) -> void:
	pass


func resolve_targets(caster: BattleEntity, all_entities: Array[BattleEntity]) -> Array[BattleEntity]:
	return []

func get_target_key() -> String:
	return ""
