extends MarginContainer

func set_player(player):
	$Score/VBoxContainer/Name.set_text(player.ai_name)

func set_score(new_score:int):
	$Score/VBoxContainer/Score.set_text(str(new_score))
