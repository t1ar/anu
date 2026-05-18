extends Area3D
class_name TriggerZone

# The data file containing the path to the next map, music, etc.
@export var target_map_data: MapData 

# The exact name of the Marker3D where the player should appear
@export var target_spawn_point: String 

func _ready() -> void:
	# Connect the built-in signal to our custom function
	body_entered.connect(_on_body_entered)
	
func _on_body_entered(body: Node) -> void:
	# Make sure only the player triggers the transition (not enemies or NPCs)
	print(" DOOR TRIGGERED BY: ", body.name, " in group Player? ", body.is_in_group("Player"))
	if body.is_in_group("Player"):
		# Call your global Autoload to handle the loading and EasyTransition visuals
		ScenetransitionManager.transition_to_field(target_map_data, target_spawn_point)
