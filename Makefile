.PHONY: test-unit
test-unit:
	PYTHONPATH=./src:./tests pytest -s tests/unit

.PHONY: test-integration
test-integration:
	PYTHONPATH=./src:./tests pytest -s tests/integration
