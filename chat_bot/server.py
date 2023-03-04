# Импортируем созданный нами класс Server
from bot import VkBot
# Получаем из config.py наш api-token


vk_api_token = "vk1.a.gHUK7rOx63S_SO8wmYF4I4bQLF3AOu4l5PnSbdEwn8i0q9VFmlfBWdL8m3dMij4V3KTmfhrnLBBg6E_AnltHfz82dwwibdJhE2j7NvY89UX-fdOLCNuRx6XLmlxnqGN533J478VzfMrhGcjTIfjg0CSIyjodvrw8MBGcbCUeHQ3BQ7tsYVg28cGUwso4_rQx5Rsi5cUcLddztlnfRAU3yg"

server1 = VkBot(vk_api_token, 219109543, "server1")
server1.start()
