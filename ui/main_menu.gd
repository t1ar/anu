extends Control

const debug_scene = "res://ui/Debug.tscn"

func _on_debug_pressed() -> void:
	EasyTransition.transition_to(debug_scene)

	
