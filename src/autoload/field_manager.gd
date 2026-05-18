# FieldManager.gd — Autoload
extends Node

# ── player ─────────────────────────────────────────────
var player_node: CharacterBody3D = null
var is_controllable: bool = true

# ── world ──────────────────────────────────────────────
var npcs: Array = []
var interactables: Array = []
#var current_zone: EncounterZone = null   # set by the map's EncounterZone node

# ── encounter ──────────────────────────────────────────
var step_counter: int = 0
var encounter_rate: float = 0.15         # overridden per zone

# ── signals ────────────────────────────────────────────
#signal player_moved(position: Vector3)
#signal encounter_triggered(group: Resource)
#signal chest_opened(item: Resource)
#signal event_triggered(event_id: String)

# ── lifecycle ─────────────────────────────────────────


func _on_scene_changed(_path: String) -> void:
	# wait one frame for the new scene to finish instantiating
	await get_tree().process_frame
	on_map_ready()


func on_map_ready() -> void:
	# find the player in the new scene
	player_node = get_tree().get_first_node_in_group("player")

	# collect NPCs and interactables
	npcs = get_tree().get_nodes_in_group("npc")
	interactables = get_tree().get_nodes_in_group("interactable")

	# restore position after battle or teleport
	if GameManager.player_position != Vector3.ZERO:
		restore_position()

	unlock_player()


func on_map_exit() -> void:
	# save position before leaving
	if player_node:
		GameManager.player_position = player_node.global_position
	lock_player()
	npcs.clear()
	interactables.clear()
	#current_zone = null
	
func lock_player() -> void:
	is_controllable = false
	if player_node:
		player_node.set_process_input(false)
		player_node.set_physics_process(false)


func unlock_player() -> void:
	is_controllable = true
	if player_node:
		player_node.set_process_input(true)
		player_node.set_physics_process(true)


func teleport(target_pos: Vector3, map_path: String = "") -> void:
	lock_player()
	if map_path != "" and map_path != GameManager.current_map:
		GameManager.player_position = target_pos
		GameManager.change_scene(map_path)
	else:
		# same map, just move
		player_node.global_position = target_pos
		GameManager.player_position = target_pos
		unlock_player()


func restore_position() -> void:
	if player_node and GameManager.player_position != Vector3.ZERO:
		player_node.global_position = GameManager.player_position
		
# Back in FieldManager.gd




func trigger_encounter(group: Resource) -> void:
	lock_player()
	on_map_exit()
	GameManager.start_battle(group)
