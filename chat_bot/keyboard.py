from vk_api.keyboard import VkKeyboard, VkKeyboardColor




def make_keyboard(keyboard_settings, button_data, keybord_type='mine'):
    keyboard = VkKeyboard(**keyboard_settings)
    for name in button_data.keys():
        keyboard.add_callback_button(
            label=name,
            color=VkKeyboardColor.PRIMARY,
            payload={'type': name},
        )
        keyboard.add_line()
    if keybord_type != 'mine':
        keyboard.add_callback_button(
            label='Назад',
            color=VkKeyboardColor.PRIMARY,
            payload={'type': 'mine'}
        )
    return keyboard
