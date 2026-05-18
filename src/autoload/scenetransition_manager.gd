extends Node

var player_scene : PackedScene = preload("res://src/entities/chars/PlayerField.tscn")

var current_field: Node = null
var current_map_data: MapData 
var is_transitioning: bool = false

func transition_to_field(map_data: MapData, spawn_point_name: String) -> void:
	if is_transitioning:
		print("DEBUG: Blocked a duplicate transition call!")
		return 
		
	is_transitioning = true
	EasyTransition.cover() 
	await get_tree().create_timer(0.5).timeout
	
	current_map_data = map_data
	
	#if current_map_data.bgm_track != null:
	#	AudioManager.play_music(current_map_data.bgm_track)
	
	var player = get_tree().get_first_node_in_group("Player")
	
	if player == null:
		player = player_scene.instantiate()
	else:
		var old_parent = player.get_parent()
		if old_parent:
			old_parent.remove_child(player)
	
	if is_instance_valid(current_field):
		current_field.queue_free()
	
	var new_field_resource = load(map_data.freefield_path)
	var new_field = new_field_resource.instantiate()
	
	# --- CHANGED: Wipe out the editor placeholder player from the data right here! ---
	_clear_placeholder_player(new_field)
	
	get_tree().root.add_child(new_field)
	
	# ---> FIX #1: Tell Godot this is the new official map
	get_tree().current_scene = new_field 
	current_field = new_field
	
	new_field.add_child(player)
	
	
	var spawn_container = new_field.get_node_or_null("SpawnPoints")
	if spawn_container:
		var marker = spawn_container.get_node_or_null(spawn_point_name)
		if marker is Marker3D:
			player.global_position = marker.global_position
			player.global_rotation.y = marker.global_rotation.y
			
	# ---> FIX #2: Force the player's camera to turn back on!
	# (Make sure to use the exact name of your Camera3D node here)
	var player_camera = player.get_node_or_null("Camera3D")
	if player_camera:
		player_camera.make_current()
		
	if player.has_method("snap_camera"):
		player.snap_camera()
	
	EasyTransition.uncover()
	await get_tree().create_timer(0.5).timeout
	is_transitioning = false
	
func _clear_placeholder_player(node: Node) -> void:
	if node == null:
		return
	for child in node.get_children():
		if child.is_in_group("Player"):
			node.remove_child(child)
			child.free() # Instantly erase it from engine memory
		else:
			_clear_placeholder_player(child) # Keep scanning deeper down the scene tree
