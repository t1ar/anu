@tool
class_name AddDefense
extends Defense

@export var defense_flat: int = 50
@export var defense_multiplier: float = 1.0
var defense_added: int

func _validate_property(property: Dictionary) -> void:
	if property.name == "affect_type":
		affect_type = "Static"
		property.usage |= PROPERTY_USAGE_READ_ONLY

func execute_affect(targets: Array[BattleEntity]) -> void:
	
	#defense_added = defense_flat * defense_multiplier * entity_multiplier or smth
	pass

#example for static, AddDefense 
func revert_affect(target: BattleEntity) -> void:
	#target.data.stat.defense -= defense_added
	pass
