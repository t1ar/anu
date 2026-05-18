extends Control

const debug = "res://ui/Debug.tscn"
const test1 = "res://src/fields/t1ardebug1.tres"

func _on_back_pressed() -> void:
	EasyTransition.transition_to(debug)


func _on_test_1_pressed() -> void:
	pass # Replace with function body.
