extends Node2D

var ai_name := "Null"
var color = Color8(0,0,0)
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	
	var hash = ai_name.hash()
	var r = (hash & 0xFF0000) >> 16
	var g = (hash & 0x00FF00) >> 8
	var b = hash & 0x0000FF
	$Character/Label.set_text(ai_name)
	color = Color8(r,g,b)
	$Character/ColorBox.texture.get_gradient().set_color(0,color)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
