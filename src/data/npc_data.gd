extends Resource
class_name NPCData

@export_group("Identity")
@export var npc_id: String
@export var display_name: String 

@export_group("Data")
@export var dialouge_file: Resource
@export var model_tscn: PackedScene
