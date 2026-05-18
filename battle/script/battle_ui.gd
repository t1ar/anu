extends CanvasLayer

#UI act as a waiting point when Player's turn

#send to BattleManager 
signal battle_action_preview(caster: Hero, affect: Array[Affect], target: BattleEntity)
signal battle_action_confirm(caster: Hero, affect: Array[Affect], target: BattleEntity)

#send to cam
signal cam_target_selected(entity: BattleEntity) #target camera direction, idk if needed
signal cam_player_select_all_allies #idk if needed

#send to scene/anim
signal scene_skill_list_init(skill_list: Array[Skill]) #init all hero's skill
signal scene_skill_idle(caster: Hero, skill: Skill) #caster for pos, for when previewing the skill
signal scene_skill_confirm(caster: BattleEntity, targets: Array[BattleEntity])
#signal item not here yet, WIP


func _ready() -> void:
	#BattleManager CONNECT TO BATTLEMANAGER
	pass


func display_UI(hero_group: Array[Hero], enemy_group: Array[Enemy], order: Array[BattleEntity]):
	_display_stats_UI(hero_group, enemy_group)
	_display_order_UI(order)
	#any other that is always visible, etc..
	pass



func _display_order_UI(order: Array[BattleEntity]):
	#left-side order
	pass

func _display_stats_UI(hero_group: Array[Hero], enemy_group: Array[Enemy]):
	#entities info
	pass

func update_order_UI(new_order: Array[BattleEntity]):
	
	pass


func display_action(caster: Hero):
	#action selection, attack, inventory, escape
	#if pressed action element, signal emit and callable
	_on_display_skill(caster)
	pass

func _on_display_skill(caster: Hero):
	#skill selection, based on caster
	var selected: Skill
	for skill in caster.skill_list:
		pass
	
	

	BattleManager.ui_selected_affect.emit(selected)
	pass



func _on_display_item(inventory):
	#item selection, based on inventory
	pass


#for camera movement
#func move_camera_to(target_position: Vector2, duration: float = 1.0):
	#var tween = create_tween()
	#tween.tween_property(self, "position", target_position, duration)
	#tween.set_trans(Tween.TRANS_SINE) # Gives a smooth ease-in/out
