@tool
class_name CreateShield
extends Defense

@export var shield_hp_flat: int = 170
@export var shield_multiplier: float = 1.0

func _validate_property(property: Dictionary) -> void:
	if property.name == "affect_type":
		affect_type = "Static"
		property.usage |= PROPERTY_USAGE_READ_ONLY

func execute_affect(targets: Array[BattleEntity]) -> void:
	pass

func revert_affect(targets: Array[BattleEntity]) -> void:
	pass
