@tool
extends CharacterBody3D
class_name NPC

@export var npc_data : NPCData:
	set(value):
		npc_data = value
		_update_model()

var active_model: Node3D

func _ready() -> void:
	# 2. EDITOR CHECK: Are we in the Godot Editor, or playing the game?
	if Engine.is_editor_hint():
		# We are in the editor! Just show the model and stop.
		_update_model()
		return
		
	# --- NORMAL GAMEPLAY LOGIC BELOW ---
	if npc_data == null:
		return
		
	# Check Quest Flags
		
	# If they passed the flag check, load their model for the game
	_update_model()

func _update_model() -> void:
	# Step A: Delete the old model (if you swapped the NPC Data)
	if active_model != null:
		active_model.queue_free()
		active_model = null
		
	# Step B: Spawn the new model
	if npc_data != null and npc_data.model_tscn != null:
		active_model = npc_data.model_tscn.instantiate()
		add_child(active_model)
		
func interact() -> void:
	print("sukses")
