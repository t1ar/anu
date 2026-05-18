extends Control

const t1ar = "res://ui/t1ar.tscn"
const MainMenu = "res://ui/MainMenu.tscn"

func _on_t1ar_pressed() -> void:
	EasyTransition.transition_to(t1ar)

func _on_back_pressed() -> void:
	EasyTransition.transition_to(MainMenu)
