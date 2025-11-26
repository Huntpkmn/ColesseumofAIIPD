extends Node2D

var strategy : AIStrategy
var ai_name := "Null"
var color = Color8(0,0,0)
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass

func set_up():
	var hash = ai_name.hash()
	var r = (hash & 0xFF0000) >> 16
	var g = (hash & 0x00FF00) >> 8
	var b = hash & 0x0000FF
	$Character/Label.set_text(ai_name)
	color = Color8(r,g,b)
	$Character/ColorBox.texture.get_gradient().set_color(0,color)

func get_action(players)->int:
	var items = []
	for i in range(len(players)):
		var item = 0
		if players[i] == self:
			item = 1
			continue
		item = await get_tree().get_first_node_in_group("main").ask_decision()
		#CHange color here as well
		item = 1 if item else 0
		if item == 0:
			$Character/Decision.color = Color(1.0, 0.0, 0.0, 0.612)
		else:
			$Character/Decision.color = Color(0.417, 0.604, 0.0, 0.612)
		$Character/Decision.show()
		items.append(item)
	return items


func set_player_name(new_name:String):
	ai_name = new_name
	set_up()
