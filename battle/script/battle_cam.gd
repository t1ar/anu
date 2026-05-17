extends Camera3D


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	BattleManager.cam_player_turn.connect(change_cam_hero)
	BattleManager.cam_enemy_turn.connect(change_cam_enemy)
	BattleManager.cam_target_selected.connect(point_cam)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass



func change_cam_hero(hero: Hero): #based on cur_entity
	#cam move to hero.position
	pass

func change_cam_enemy(): #based on cur_entity
	#cam move to default pos
	pass

func point_cam(target: Enemy):
	pass
