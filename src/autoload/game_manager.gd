extends Node

# ── enums ──────────────────────────────────────────────
enum GameMode { FIELD, BATTLE, MENU, CUTSCENE }

# ── game state ─────────────────────────────────────────
var current_mode: GameMode = GameMode.FIELD
var party: Array = []           # Array[PartyMember]
var gold: int = 0
var play_time: float = 0.0
var story_flags: Dictionary = {}
var current_map: String = ""
var player_position: Vector3 = Vector3.ZERO

# ── internal ───────────────────────────────────────────
var _field_return_map: String = ""
var _field_return_pos: Vector3 = Vector3.ZERO
@onready var _transition: ColorRect = $TransitionOverlay

# ── signals (global bus) ───────────────────────────────
signal game_mode_changed(mode: GameMode)
signal battle_started(enemy_group: Resource)
signal battle_ended(result: Dictionary)
signal party_updated()
signal gold_changed(new_amount: int)
signal scene_changed(path: String)

# ── lifecycle ──────────────────────────────────────────


func _process(delta: float) -> void:
	if current_mode == GameMode.FIELD:
		play_time += delta

# ── scene / mode control ──────────────────────────────
func change_scene(path: String) -> void:
	await _fade_out()
	get_tree().change_scene_to_file(path)
	current_map = path
	scene_changed.emit(path)
	await _fade_in()

func start_battle(enemy_group: Resource) -> void:
	_field_return_map = current_map
	_field_return_pos = player_position
	current_mode = GameMode.BATTLE
	game_mode_changed.emit(current_mode)
	battle_started.emit(enemy_group)
	await change_scene("res://scenes/battle/Battle.tscn")

func end_battle(result: Dictionary) -> void:
	current_mode = GameMode.FIELD
	game_mode_changed.emit(current_mode)
	battle_ended.emit(result)
	await change_scene(_field_return_map)
	# FieldManager listens for battle_ended and repositions player

func game_over() -> void:
	await change_scene("res://scenes/ui/GameOver.tscn")

# ── party / gold helpers ───────────────────────────────
func add_gold(amount: int) -> void:
	gold += amount
	gold_changed.emit(gold)

func set_flag(key: String, value = true) -> void:
	story_flags[key] = value

func get_flag(key: String, default = false):
	return story_flags.get(key, default)

# ── save / load ────────────────────────────────────────


func new_game() -> void:
	party.clear()
	gold = 0
	play_time = 0.0
	story_flags.clear()
	await change_scene("res://scenes/field/OpeningMap.tscn")

# ── transition helpers ─────────────────────────────────
func _fade_out() -> void:
	var tween = create_tween()
	tween.tween_property(_transition, "modulate:a", 1.0, 0.3)
	_transition.visible = true
	await tween.finished

func _fade_in() -> void:
	var tween = create_tween()
	tween.tween_property(_transition, "modulate:a", 0.0, 0.3)
	await tween.finished
	_transition.visible = false
