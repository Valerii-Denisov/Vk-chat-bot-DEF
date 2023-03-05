start:
	poetry run chat_bot

install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

upgrade:
	python3 -m pip uninstall vk_chat_bot_def
	poetry build
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 chat_bots
