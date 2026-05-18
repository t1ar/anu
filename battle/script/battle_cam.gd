extends Node3D #extends as cam

#signal skill_preview(caster: Hero, option: Skill, target: Enemy)
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	BattleManager.cam_player_turn.connect(change_cam_hero) #when still in action select
	BattleManager.cam_enemy_turn.connect(change_cam_enemy)
	#$"../battle_ui".skill_preview
	#$"../battle_ui".item_preview

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass



func change_cam_hero(hero: Hero): #based on cur_entity
	#cam move to hero.position
	pass

func change_cam_enemy(): #based on cur_entity
	#cam move to default pos
	pass
