@abstract
class_name Affect
extends Resource

@export var affect_name: String = ""
@export var affect_description: String = ""
@export_enum("Static", "Tick") var affect_type: String = "Static" 
#Static -> shield, buffs, anything that stays
#Tick -> DoT, HoT, anything that gets re-executed each turn
@export_range(0, 10) var duration: int = 0  # 0 = one time use

func apply_to(targets: Array[BattleEntity]) -> void:
	for t in targets:
		t.active_effects.append(duplicate())

func execute_affect(target: BattleEntity) -> void:
	push_error("execute_affect() not implemented in: " + get_script().get_global_name())

func resolve_targets(caster: BattleEntity, all_entities: Array[BattleEntity]) -> Array[BattleEntity]:
	push_error("resolve_targets() not implemented in: " + get_script().get_global_name())
	return []

func get_target_key() -> String:
	push_error("get_target_key() not implemented in: " + get_script().get_global_name())
	return ""
