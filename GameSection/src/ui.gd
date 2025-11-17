extends Control


func _ready() ->void:
	pass

func change_counter(count:int):
	$Counter.set_text(str(count))
