class_name BattleUI
extends CanvasLayer

#rough blue_print, actual real time UI would need signal on everything

#signal choice_action(option: String) # for idk, might be useless
signal choice_skill(option: Skill) # for prediction
signal choice_item() # for prediction
signal skill_used(caster: BattleEntity, skill: Skill) #confirmed used skill

#scene signal
signal scene_enemy_skill(caster: Enemy, skill: Skill) #display scene with keys, 
signal scene_player_skill(caster: Hero, skill: Skill)
signal scene_player_item(caster: Hero) #, item: Item)


func _ready() -> void:
	
	
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


func use_skill(caster: BattleEntity, skill: Skill) -> void:
	skill_used.emit(caster, skill)

func _on_display_item(inventory):
	#item selection, based on inventory
	pass


#for camera movement
#func move_camera_to(target_position: Vector2, duration: float = 1.0):
	#var tween = create_tween()
	#tween.tween_property(self, "position", target_position, duration)
	#tween.set_trans(Tween.TRANS_SINE) # Gives a smooth ease-in/out
