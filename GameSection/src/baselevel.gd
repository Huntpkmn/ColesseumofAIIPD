extends Node2D

var num_players = 2
@onready var Player = preload("res://src/player.tscn")
const DISTANCE = 1000
var players = []

signal round_count_change(new_amount)
var round_count=0:
	set(new_round_count):
		round_count = new_round_count
		round_count_change.emit(round_count)

func _ready() -> void:
	round_count_change.connect($UI/UI.change_counter)
	pass

func set_up():
	var table_pos = $Table.position
	var zoomval =  1
	$Table/Table.scale = Vector2(0.4*(1/zoomval), 0.4*(1/zoomval))
	$Camera2D.zoom = Vector2(zoomval,zoomval)
	for i in range(num_players):
		var p = Player.instantiate()
		var angle = (2*PI/(num_players))*i

		p.position = table_pos+Vector2.from_angle(angle)*DISTANCE*(1/zoomval)
		players.append(p)
		add_child(p)
		var t = get_tree().create_tween()
		t.tween_property(p, "position", table_pos+Vector2.from_angle(angle)*300*(1/zoomval), 1).set_trans(Tween.TRANS_SINE)


func _on_start_pressed() -> void:
	set_up()
	$PlayerUI/PlayerUI/Start.hide()
