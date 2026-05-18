extends Node3D


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	$"../battle_ui".idle_skill #CONNECT TO BATTLEUI, AFTER ANIM FINISH, SIGNAL BATTLEMANAGER
	
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func _play_skill_loop():
	pass

func _play_skill_to():
	pass
	
func _play_item_to():
	pass

func _on_anim_finished():
	BattleManager.battle_progress
