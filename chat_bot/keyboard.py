from vk_api.keyboard import VkKeyboard, VkKeyboardColor




def make_keyboard(keyboard_settings, button_data, keybord_type='mine'):
    keyboard = VkKeyboard(**keyboard_settings)
    i = 0
    for name in button_data:
        print(i)
        print(name[0])
        keyboard.add_callback_button(
            label=name[0],
            color=VkKeyboardColor.PRIMARY,
            payload={'type': name[0]},
        )
        if i < len(button_data)-1:
            keyboard.add_line()
            i += 1
    if keybord_type != 'mine':
        keyboard.add_line()
        keyboard.add_callback_button(
            label='Назад',
            color=VkKeyboardColor.NEGATIVE,
            payload={'type': 'mine'}
        )
    return keyboard
