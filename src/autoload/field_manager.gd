# FieldManager.gd — Autoload
extends Node

# ── player ─────────────────────────────────────────────
var player_node: CharacterBody3D = null
var is_controllable: bool = true

# ── world ──────────────────────────────────────────────
var npcs: Array = []
var interactables: Array = []
var current_zone: EncounterZone = null   # set by the map's EncounterZone node

# ── encounter ──────────────────────────────────────────
var step_counter: int = 0
var encounter_rate: float = 0.15         # overridden per zone

# ── signals ────────────────────────────────────────────
signal player_moved(position: Vector3)
signal encounter_triggered(group: Resource)
signal chest_opened(item: Resource)
signal event_triggered(event_id: String)

# ── lifecycle ──────────────────────────────────────────
func _ready() -> void:
	GameManager.battle_ended.connect(_on_battle_ended)
	GameManager.scene_changed.connect(_on_scene_changed)


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
	current_zone = null
	
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
func on_player_step() -> void:
	if not is_controllable or current_zone == null:
		return

	GameManager.player_position = player_node.global_position
	player_moved.emit(player_node.global_position)

	step_counter += 1
	_tick_encounter()


func _tick_encounter() -> void:
	if current_zone == null or current_zone.enemy_groups.is_empty():
		return

	encounter_rate = current_zone.encounter_rate
	_roll_encounter()


func _roll_encounter() -> void:
	if randf() > encounter_rate:
		return

	# reset step counter on encounter
	step_counter = 0

	var group = current_zone.enemy_groups.pick_random()
	encounter_triggered.emit(group)
	trigger_encounter(group)


func trigger_encounter(group: Resource) -> void:
	lock_player()
	on_map_exit()
	GameManager.start_battle(group)


func set_encounter_zone(zone) -> void:
	current_zone = zone
	encounter_rate = zone.encounter_rate if zone else 0.0
	
func start_dialog(npc_node) -> void:
	pass


func _on_dialog_finished() -> void:
	unlock_player()


func open_chest(chest_node) -> void:
	pass


func trigger_event(event_id: String) -> void:
	lock_player()
	event_triggered.emit(event_id)
	# your cutscene/event system picks this up and calls unlock_player() when done


func _on_battle_ended(result: Dictionary) -> void:
	if result.result == "win" or result.result == "fled":
		# scene_changed fires automatically from GameManager.end_battle,
		# which calls change_scene back to the field map —
		# on_map_ready() handles restoring position and unlocking
		pass
