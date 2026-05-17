extends Resource
class_name MapData

@export var map_id: String           # e.g., "forest_01"
@export var display_name: String     # e.g., "Whispering Woods"
@export var is_safe_zone: bool = false
@export var bgm_track: AudioStream
@export_file("*.tscn") var freefield_path: String 
@export_file("*.tscn") var battlefield_path: String
