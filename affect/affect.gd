@abstract
class_name Affect
extends Resource

@export var affect_name: String = ""
@export var affect_description: String = ""
@export_enum("Static", "Tick") var affect_type: String = "Static"
#ADD THIS FOR STATIC ONLY FOR INSPECTOR
#func _validate_property(property: Dictionary) -> void:
	#if property.name == "affect_type":
		#affect_type = "Static"
		#property.usage |= PROPERTY_USAGE_READ_ONLY

#Static + duration 0: one-time, executed on apply, removed next tick, no revert
#Static + duration > 0: applied once, persists for N turns, revert on expiry (shield, stat buff)
#Tick + duration > 0: re-executed every turn until expired (DoT, HoT)

@export_range(0, 10) var duration: int = 0  # 0 = one time use

# runtime saved
var caster: BattleEntity # used for skill multiplier, etc
#var target: BattleEntity # used for Static + duration, Defense or Support Only, declare inside subclass

#used in BattleManager for applying affect
func apply_to(caster_: BattleEntity, targets: Array[BattleEntity]) -> void:
	for t: BattleEntity in targets:
		var copy: Affect = duplicate()
		copy.caster = caster_
		t.data.active_affects.append(copy) #dupe to each entity, avoid data override
		if affect_type == "Static":
			copy.execute_affect([t])

#when executing / reverting affect, use parameter.data.cur_stat to access it

#explicitly used in Support, only support affect speed, turn manipulation, sleepy, etc
func predict_affect(caster: BattleEntity, targets: Array[BattleEntity]) -> void:
	push_error("predict_affect() not implemented in: " + get_script().get_global_name())

#used in BattleEntity or apply_to for updating target's data / stat
func execute_affect(targets: Array[BattleEntity]) -> void:
	push_error("execute_affect() not implemented in: " + get_script().get_global_name())

#used in BattleManager for removing static affect
func revert_affect(target: BattleEntity) -> void:
	push_error("revert_affect() not implemented in: " + get_script().get_global_name())

#used in BattleManager for applying affect
func resolve_targets(caster: BattleEntity, all_entities: Array[BattleEntity]) -> Array[BattleEntity]:
	push_error("resolve_targets() not implemented in: " + get_script().get_global_name())
	return []

#used in BattleManager for applying affect
func get_target_key() -> String:
	push_error("get_target_key() not implemented in: " + get_script().get_global_name())
	return ""
