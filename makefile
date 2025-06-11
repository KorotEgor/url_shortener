install:
	curl -LsSf https://astral.sh/uv/install.sh | sh

lint:
	uv run ruff format url_shortener && uv run ruff check url_shortener

commit_lint:
	uv run ruff format url_shortener --check && uv run ruff check url_shortener --exit-non-zero-on-fix

run:
	uv run url_shortener/main.py

init_db:
	uv run python3 /home/kor_egor/url_shortener/url_shortener/db/init_db.py
