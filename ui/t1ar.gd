extends Control

const debug = "res://ui/Debug.tscn"
const test1 = preload("res://src/fields/free/t1ardebug1.tres")

func _on_back_pressed() -> void:
	EasyTransition.transition_to(debug)


func _on_test_1_pressed() -> void:
	get_tree().current_scene.queue_free()
	ScenetransitionManager.transition_to_field(test1,"fromt1ar1")
