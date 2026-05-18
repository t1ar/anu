# BGMManager.gd — Autoload
extends Node

var _player_a: AudioStreamPlayer
var _player_b: AudioStreamPlayer
var _active: AudioStreamPlayer

var current_stream: AudioStream = null
var _field_stream: AudioStream = null
var _field_position: float = 0.0

const DEFAULT_FADE := 1.0

func _ready() -> void:
	_player_a = AudioStreamPlayer.new()
	_player_b = AudioStreamPlayer.new()
	_player_a.bus = "BGM"
	_player_b.bus = "BGM"
	add_child(_player_a)
	add_child(_player_b)
	_active = _player_a

	#GameManager.battle_started.connect(_on_battle_started)
	#GameManager.battle_ended.connect(_on_battle_ended)


# ── public API ─────────────────────────────────────────
func play(stream: AudioStream, fade_in: float = DEFAULT_FADE) -> void:
	if current_stream == stream:
		return

	current_stream = stream
	_active.stream = stream
	_active.volume_db = linear_to_db(0.0)
	_active.play()

	if fade_in > 0.0:
		await _fade_player(_active, 0.0, 1.0, fade_in)


func stop(fade_out: float = DEFAULT_FADE) -> void:
	if fade_out > 0.0:
		await _fade_player(_active, 1.0, 0.0, fade_out)
	_active.stop()
	current_stream = null


func crossfade(stream: AudioStream, duration: float = DEFAULT_FADE) -> void:
	if current_stream == stream:
		return

	var incoming = _player_b if _active == _player_a else _player_a
	var outgoing = _active

	incoming.stream = stream
	incoming.volume_db = linear_to_db(0.0)
	incoming.play()

	_fade_player(outgoing, 1.0, 0.0, duration)
	await _fade_player(incoming, 0.0, 1.0, duration)

	outgoing.stop()
	_active = incoming
	current_stream = stream


func set_pitch(pitch: float) -> void:
	_player_a.pitch_scale = pitch
	_player_b.pitch_scale = pitch


# ── battle BGM swap ────────────────────────────────────
func _on_battle_started(enemy_group) -> void:
	save_position()
	var battle_bgm = null
	if enemy_group and enemy_group.battle_bgm:
		battle_bgm = enemy_group.battle_bgm
	elif GameManager.current_map_data and GameManager.current_map_data.bgm_track:
		battle_bgm = GameManager.current_map_data.bgm_track  # fallback
	if battle_bgm:
		crossfade(battle_bgm)


func _on_battle_ended(_result: Dictionary) -> void:
	resume_field()


func save_position() -> void:
	_field_stream = current_stream
	_field_position = _active.get_playback_position()


func resume_field() -> void:
	if not _field_stream:
		return
	crossfade(_field_stream)
	await get_tree().create_timer(0.1).timeout
	_active.seek(_field_position)


# ── internal ───────────────────────────────────────────
func _fade_player(
	player: AudioStreamPlayer,
	from_vol: float,
	to_vol: float,
	duration: float
) -> Signal:
	var tween = create_tween()
	tween.tween_method(
		func(v: float): player.volume_db = linear_to_db(v),
		from_vol,
		to_vol,
		duration
	)
	return tween.finished
