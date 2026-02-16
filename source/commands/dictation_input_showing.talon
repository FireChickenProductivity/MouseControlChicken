tag: user.mouse_control_chicken_dictation_input_showing
-

chicken choose <user.mouse_control_chicken_dictation_input>$: 
    user.mouse_control_chicken_set_dictation_input_dialogue_text(mouse_control_chicken_dictation_input)

accept [input]:
    user.mouse_control_chicken_accept_dictation_input()

(cancel|reject) [input]:
    user.mouse_control_chicken_cancel_dictation_input()