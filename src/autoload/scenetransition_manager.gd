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
	
	if current_field == null or not is_instance_valid(current_field):
		current_field = get_tree().current_scene
	
	# Now this check will pass perfectly!
	if is_instance_valid(current_field):
		print("SUCCESS: Instantly erasing old field: ", current_field.name)
		current_field.queue_free()
	else:
		print("❌ CRITICAL ERROR: Could not find any active scene to delete!")
	
	var new_field_resource = load(map_data.freefield_path)
	var new_field = new_field_resource.instantiate()
	
	# --- CHANGED: Wipe out the editor placeholder player from the data right here! ---
	_clear_placeholder_player(new_field)
	
	get_tree().root.add_child(new_field)
	
	# ---> FIX #1: Tell Godot this is the new official map
	get_tree().current_scene = new_field 
	current_field = new_field
	
	new_field.add_child(player)
	await get_tree().process_frame

	var marker = _find_spawn(new_field, spawn_point_name)
	if marker:
		player.global_position = marker.global_position
		GameManager.player_position = marker.global_position
		player.reset_rotation(marker)
	else:
		player.global_position = map_data.default_spawn
		GameManager.player_position = map_data.default_spawn

	await get_tree().process_frame
	await player.snap_camera()

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
			
func _find_spawn(field: Node, spawn_name: String) -> Marker3D:
	# recursively find all Marker3D nodes in the new field
	var markers = []
	_collect_markers(field, markers)
	
	for marker in markers:
		if marker.name == spawn_name:
			return marker
	
	if not markers.is_empty():
		push_warning("SceneTransitionManager: spawn '%s' not found, using first available" % spawn_name)
		return markers[0]
	
	push_error("SceneTransitionManager: no spawn points in scene")
	return null
	

func _collect_markers(node: Node, result: Array) -> void:
	if node is Marker3D:
		result.append(node)
	for child in node.get_children():
		_collect_markers(child, result)
