extends CharacterBody3D

# ── constants ──────────────────────────────────────────
const WALK_SPEED := 3.0
const RUN_SPEED := 9.0
const GRAVITY := 20.0
const STEP_DISTANCE := 1.5 

# ── state ──────────────────────────────────────────────
var _distance_accumulator: float = 0.0
var _facing_direction: Vector3 = Vector3.FORWARD
var _interactable_in_range = null

var mouse_sensitivity: float = 0.2

var min_yaw: float = 0
var max_yaw: float = 360

var min_pitch: float = -89.9
var max_pitch: float = 50

@onready var model: Node3D = $Tempbox
@onready var pcam: PhantomCamera3D = $PhantomCamera3D

func _ready() -> void:
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	await get_tree().process_frame
	
func _unhandled_input(event) -> void:
  # Trigger whenever the mouse moves.
	if event is InputEventMouseMotion and Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
		var pcam_rotation_degrees: Vector3

		# Assigns the current 3D rotation of the SpringArm3D node - to start off where it is in the editor.
		pcam_rotation_degrees = pcam.get_third_person_rotation_degrees()

		# Change the X rotation.
		pcam_rotation_degrees.x -= event.relative.y * mouse_sensitivity
			
		# Clamp the rotation in the X axis so it can go over or under the target.
		pcam_rotation_degrees.x = clampf(pcam_rotation_degrees.x, min_pitch, max_pitch)

		# Change the Y rotation value.
		pcam_rotation_degrees.y -= event.relative.x * mouse_sensitivity
			
		# Sets the rotation to fully loop around its target, but without going below or exceeding 0 and 360 degrees respectively.
		pcam_rotation_degrees.y = wrapf(pcam_rotation_degrees.y, min_yaw, max_yaw)
			
		# Change the SpringArm3D node's rotation and rotate around its target.
		pcam.set_third_person_rotation_degrees(pcam_rotation_degrees)

func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y -= GRAVITY * delta
		
	var speed = WALK_SPEED
	var input_dir = _get_input_direction()
	if input_dir != Vector3.ZERO :
		if Input.is_action_pressed("run") :
			speed = RUN_SPEED 
	#if Input.is_action_pressed("run") else WALK_SPEED

	if input_dir != Vector3.ZERO:
		# move relative to camera facing
		var cam_basis = _get_camera_basis()
		var move_dir = (cam_basis * input_dir).normalized()
		move_dir.y = 0.0

		velocity.x = move_dir.x * speed
		velocity.z = move_dir.z * speed
		_facing_direction = move_dir

		# rotate model to face movement direction
		model.rotation.y = lerp_angle(
			model.rotation.y,
			atan2(move_dir.x, move_dir.z),
			delta * 12.0
		)

		_tick_step(delta)
	else:
		velocity.x = move_toward(velocity.x, 0.0, speed)
		velocity.z = move_toward(velocity.z, 0.0, speed)
		#anim.play("idle")

	move_and_slide()

func _input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		if Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
			Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
		else:
			Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)


func _get_input_direction() -> Vector3:
	return Vector3(
		Input.get_axis("move_left", "move_right"),
		0.0,
		Input.get_axis("move_forward", "move_back")
	)


func _get_camera_basis() -> Basis:
	var y_rotation = pcam.get_third_person_rotation().y
	return Basis(Vector3.UP, y_rotation)

# ── step counter (feeds encounter system) ─────────────
func _tick_step(delta: float) -> void:
	_distance_accumulator += velocity.length() * delta
	if _distance_accumulator >= STEP_DISTANCE:
		_distance_accumulator = 0.0
		#FieldManager.on_player_step()
