
.PHONY: run dev test

run:
	uvicorn src.api.main:app --host 0.0.0.0 --port 8000

dev:
	UVICORN_RELOAD=true uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -q
