extends Node2D

var MAX_ROUNDS = 50
var num_players = 3
@onready var Player = preload("res://src/player.tscn")
const DISTANCE = 1000
var players = []
var points := {}
var scores := {}

signal round_count_change(new_amount)
var round_count=0:
	set(new_round_count):
		round_count = new_round_count
		round_count_change.emit(round_count)

func _ready() -> void:
	round_count_change.connect($OverallScore/UI.change_counter)
	pass

func set_up():
	var table_pos = $Table.position
	var zoomval =  0.7
	$Table/Table.scale = Vector2(0.4*(1/zoomval), 0.4*(1/zoomval))
	#$Camera2D.zoom = Vector2(zoomval,zoomval)
	for i in range(num_players):
		var p = Player.instantiate()
		var angle = (2*PI/(num_players))*i

		p.position = table_pos+Vector2.from_angle(angle)*DISTANCE*(1/zoomval)
		players.append(p)
		add_child(p)
		points[p] = 0
		$PlayerUI/PlayerUI/LineEdit.show()
		p.set_player_name(await get_name)
		var t = get_tree().create_tween()
		t.tween_property(p, "position", table_pos+Vector2.from_angle(angle)*300*(1/zoomval), 1).set_trans(Tween.TRANS_SINE)
		var score_board = preload("res://src/scoreAI.tscn").instantiate()
		score_board.set_player(p)
		scores[p] = score_board
		$OverallScore/Scoreboard/PanelContainer/VBoxContainer.add_child(score_board)

func _on_start_pressed() -> void:
	$PlayerUI/PlayerUI/Start.hide()
	await set_up()
	
	game_loop()
	

func game_loop():
	
	$OverallScore.show()
	var changer = randi_range(-int(MAX_ROUNDS*0.05),int(MAX_ROUNDS*0.05))
	for i in range(MAX_ROUNDS+changer):
		
		round_count +=1
		var actions = []
		var tweenmod = get_tree().create_tween()
		$TargetPlayer.global_position = $Table.global_position
		tweenmod.tween_property($TargetPlayer,"modulate:a", 1, 0.5).set_trans(Tween.TRANS_SINE)
		
		for p in players:
			var tween = get_tree().create_tween()
		
			tween.tween_property($TargetPlayer,"position", p.global_position, 0.3).set_trans(Tween.TRANS_SINE)
			#tween.parallel().tween_property($TargetPlayer,"scale", p.position, 0.2)
			var action = await p.get_action(players)
			actions.append(action)
			
			#await get_tree().create_timer(0.1).timeout
		tweenmod = get_tree().create_tween()
		tweenmod.tween_property($TargetPlayer,"modulate:a", 0, 0.2).set_trans(Tween.TRANS_SINE)
		await get_tree().create_timer(0.2).timeout
		var xi = 0
		var yi = 0
		while xi < len(players):
			while yi+(len(players)-xi) < len(players):
				if actions[xi] == 0 and actions[yi] == 0:
					points[players[xi]] += 1
					points[players[yi]] += 1
					pass
				elif actions[xi] == 1 and actions[yi] == 0:
					points[players[xi]] += 0
					points[players[yi]] += 5
					pass
				elif actions[xi] == 0 and actions[yi] == 1:
					points[players[xi]] += 5
					points[players[yi]] += 0
					pass
				elif actions[xi] == 1 and actions[yi] == 1:
					points[players[xi]] += 3
					points[players[yi]] += 3
				yi+=1
			xi+=1
		update_score_board(points)

func update_score_board(new_points):
	var temp_points = new_points.values()
	var i = 0
	for p in players:
		scores.get(p).set_score(temp_points[i])
		i += 1

func ask_decision():
	$PlayerUI/PlayerUI/Cooperate.show()
	$PlayerUI/PlayerUI/Defect.show()
	return await answer




signal answer(answer)
func _on_cooperate_pressed() -> void:
	$PlayerUI/PlayerUI/Cooperate.hide()
	answer.emit(true)


func _on_defect_pressed() -> void:
	$PlayerUI/PlayerUI/Defect.hide()
	answer.emit(false)

signal get_name(new_name:String)
func _on_line_edit_text_submitted(new_text: String) -> void:
	$PlayerUI/PlayerUI/LineEdit.hide()
	$PlayerUI/PlayerUI/LineEdit.clear()
	get_name.emit(new_text)
	
