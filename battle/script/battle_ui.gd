extends Node

#rough blue_print, actual real time UI would need signal on everything

signal choice_action(option: String)
signal choice_skill(option: Skill)
signal choice_item()

func display_UI(hero_group: Array[Hero], enemy_group: Array[Enemy], order: Array[BattleEntity]):
	_display_stats_UI(hero_group, enemy_group)
	_display_order_UI(order)
	pass



func _display_order_UI(order: Array[BattleEntity]):
	#left-side order
	pass

func _display_stats_UI(hero_group: Array[Hero], enemy_group: Array[Enemy]):
	#entities info
	pass

func update_order_UI(new_order: Array[BattleEntity]):
	
	pass


func display_action():
	#action selection, attack, inventory, escape
	#if pressed action element, signal emit and callable
	pass

func _on_display_skill(caster: Hero):
	#skill selection, based on caster
	var selected: Skill
	for skill in caster.skill_list:
		pass
	
	
	
	BattleManager.ui_skill.emit(selected)
	pass

signal skill_used(caster: BattleEntity, skill: Skill)

func use_skill(caster: BattleEntity, skill: Skill) -> void:
	skill_used.emit(caster, skill)

func _on_display_item(inventory):
	#item selection, based on inventory
	pass

func change_cam(pos: int = 0): #based on cur_entity
	if pos == -1: #default pos, for enemy (not in hero_list)
		pass
	
	if pos == 0: #mid
		pass
	
	if pos == 1: #right
		pass
	
	if pos == 2: #left
		pass
