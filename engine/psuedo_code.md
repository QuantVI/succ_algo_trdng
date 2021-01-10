#### event-driven pseudo-code example

while True: 	# Run the loop forever

​	new_event = get_new_event() 	# Get the latest event

​	.# Based on the event type, perform an action

​	if new_event.type == "LEFT_MOUSE_CLICK":

​		open_menu()

​	elif new_event.type == "ESCAPE_KEY_PRESS":

​		quit_game()

​	elif new_event.type == "UP_KEY_PRESS";

​		move_player_north()

​	.# ... and many more events



redraw_screen()	# Update the screen to provide animation

tick(50)	# Wait 50 milliseconds

