from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def make_keyboard(keyboard_settings, button_data, keyboard_type='mine'):
    keyboard = VkKeyboard(**keyboard_settings)
    i = 0
    for name in button_data:
        print(i)
        print(name)
        keyboard.add_callback_button(
            label=name,
            color=VkKeyboardColor.PRIMARY,
            payload={'type': name},
        )
        if i < len(button_data)-1:
            keyboard.add_line()
            i += 1
    if keyboard_type != 'mine':
        keyboard.add_line()
        keyboard.add_callback_button(
            label='Назад',
            color=VkKeyboardColor.SECONDARY,
            payload={'type': 'mine'}
        )
    keyboard.add_line()
    keyboard.add_callback_button(
        label='Завершить работу',
        color=VkKeyboardColor.NEGATIVE,
        payload={'type': 'close'},
    )
    return keyboard
