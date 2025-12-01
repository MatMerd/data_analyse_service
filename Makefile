SRC_FOLDERS=data_analyse_project

lint:
	ruff check $(SRC_FOLDERS)
#	TODO крашится с новыми изменениями, пришлось выключить
#	flakeheaven lint $(SRC_FOLDERS)
	mypy $(SRC_FOLDERS)
	@make lint-format

format:
	ruff format $(SRC_FOLDERS)

fix:
	ruff check $(SRC_FOLDERS) --fix

lint-format:
	ruff format $(SRC_FOLDERS) --check

gen-env-templates:
	PYTHONPATH=. settings-doc generate --class  $(SRC_FOLDERS).settings.AppSettings --output-format dotenv > .env.template
	PYTHONPATH=. settings-doc generate --class  $(SRC_FOLDERS).settings._dev.DevAppSettings --output-format dotenv > .env.dev.template

start-server:
	python -m $(SRC_FOLDERS) server
