class_name Skill
extends Resource

@export_group("Details")
@export var skill_name: String = ""
@export var scene: PackedScene

@export_group("Affect(s)")
@export var Offense: Array[Offense] = []
@export var Defense: Array[Defense] = []
@export var Support: Array[Support] = []

var affect_list: Array[Affect] = Offense + Defense + Support
