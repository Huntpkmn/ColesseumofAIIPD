extends Node2D

var MAX_ROUNDS = 50
var num_players = 2
@onready var Player = preload("res://src/player.tscn")
const DISTANCE = 1000
var players = []
var points := {}
var scores := {}
var both_defect_cost = [1,1]
var both_cooperate_cost = [3,3]
var defect_cost = [5,0]
var move_list = []
var is_txt = true
var failed_file = false

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
		
func create_player(player_name,i, actions):
	var table_pos = $Table.position
	var zoomval =  0.7
	$Table/Table.scale = Vector2(0.4*(1/zoomval), 0.4*(1/zoomval))
	var p = Player.instantiate()
	var angle = (2*PI/(num_players))*i

	p.position = table_pos+Vector2.from_angle(angle)*DISTANCE*(1/zoomval)
	players.append(p)
	p.actions = actions
	add_child(p)
	points[p] = 0
	p.set_player_name(player_name)
	var t = get_tree().create_tween()
	t.tween_property(p, "position", table_pos+Vector2.from_angle(angle)*300*(1/zoomval), 1).set_trans(Tween.TRANS_SINE)
	var score_board = preload("res://src/scoreAI.tscn").instantiate()
	score_board.set_player(p)
	scores[p] = score_board
	$OverallScore/Scoreboard/PanelContainer/VBoxContainer.add_child(score_board)
		
func get_file():
	$PlayerUI/PlayerUI/FileDialog.show()
	return await finished_file

func parse_txt(file):
	var a_moves = []
	var b_moves = []
	var player_a = ""
	var player_b = ""
	var lines = file.split("\n", false)
	var in_rounds = false
	var malform_checker =[0,0,0,0,0,0]

	for line in lines:
		line = line.strip_edges()
		if line.begins_with("Both Defect Cost:"):
			var nums = line.split(":")[1].strip_edges().trim_prefix("(").trim_suffix(")").split(",")
			both_defect_cost = [nums[0].to_int(), nums[1].to_int()]
			malform_checker[0] = 1
		elif line.begins_with("Both Cooperate Cost:"):
			var nums = line.split(":")[1].strip_edges().trim_prefix("(").trim_suffix(")").split(",")
			both_cooperate_cost = [nums[0].to_int(), nums[1].to_int()]
			malform_checker[1] = 1
		elif line.begins_with("Single defect cost:"):
			var nums = line.split(":")[1].strip_edges().trim_prefix("(").trim_suffix(")").split(",")
			defect_cost = [nums[0].to_int(), nums[1].to_int()]
			malform_checker[2] = 1
		elif line.begins_with("A:"):
			player_a = line.split(":")[1].strip_edges()
			malform_checker[3] = 1
		elif line.begins_with("B:"):
			player_b = line.split(":")[1].strip_edges()
			malform_checker[4] = 1
		elif line.begins_with("round,"):
			in_rounds = true
			continue
		elif in_rounds and line != "":
			var cols = line.split(",")
			if cols.size() >= 5:
				a_moves.append( convert_text(cols[1]))
				b_moves.append( convert_text(cols[2]))
				malform_checker[5] = 1
	var not_malformed :bool = true
	for val in malform_checker:
		if val == 0:
			not_malformed = false
	if not_malformed:
		MAX_ROUNDS = len(a_moves)
		await create_player(player_a, 0, a_moves)
		await create_player(player_b,1,b_moves)
		await get_tree().create_timer(1).timeout
		return true
	else:
		return false
func convert_text(text):
	if text == "COOPERATE":
		return 1
	elif text == "DEFECT":
		return 0


func _on_start_pressed() -> void:
	$PlayerUI/PlayerUI/Start.hide()
	await get_file()
	if failed_file == true:
		failed_file = false
		return
	#await set_up()
	
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
			var action = null
			if !is_txt:
				action = await p.get_action(players)
			else:
				action = p.actions[i]
				ask_set_arrow(p, players[(players.find(p)+1)%2],action)
				await get_tree().create_timer(0.2).timeout
			actions.append(action)
			
			#await get_tree().create_timer(0.1).timeout
		tweenmod = get_tree().create_tween()
		tweenmod.tween_property($TargetPlayer,"modulate:a", 0, 0.2).set_trans(Tween.TRANS_SINE)
		await get_tree().create_timer(0.2).timeout
		
		var xi = 0
		var yi = 1
		#while xi < len(players):
			#while yi +(len(players)-xi)< len(players):
		var a1 = actions[0]
		var a2 = actions[1]
		if a1 == 0 and a2 == 0:
			points[players[xi]] += both_defect_cost[0]
			points[players[yi]] += both_defect_cost[1]
			pass
		elif a1 == 1 and a2 == 0:
			points[players[xi]] += defect_cost[0]
			points[players[yi]] += defect_cost[1]
			pass
		elif a1 == 0 and a2 == 1:
			points[players[xi]] += defect_cost[0]
			points[players[yi]] += defect_cost[1]
			pass
		elif a1 == 1 and a2 == 1:
			points[players[xi]] += both_cooperate_cost[0]
			points[players[yi]] += both_cooperate_cost[1]
	
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

func ask_set_arrow(originating_player: Node2D, target_player :Node2D, decision):
	var arrow :TextureRect= preload("res://src/arrow.tscn").instantiate()
	arrow.global_position = originating_player.global_position
	arrow.rotation = originating_player.global_position.angle_to_point(target_player.global_position)
	arrow.size.x = originating_player.global_position.distance_to(target_player.global_position)
	if decision == 0:
		arrow.modulate = Color(1.0, 0.0, 0.0, 0.612)
	else:
		arrow.modulate = Color(0.417, 0.604, 0.0, 0.612)
	$Arrows.add_child(arrow)
	




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
	

signal finished_file
func _on_file_dialog_file_selected(path: String) -> void:
	if path and path.ends_with(".txt"):
		var success = await parse_txt(FileAccess.get_file_as_string(path))
		if success:
			failed_file = false
			finished_file.emit()
		else:
			failed_file = true
			finished_file.emit()
	else:
		failed_file = true
		finished_file.emit()
		$PlayerUI/PlayerUI/Start.show()

func _on_button_pressed() -> void:
	get_tree().reload_current_scene()
