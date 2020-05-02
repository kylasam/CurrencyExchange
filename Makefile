hello: venv
	$(VENV)/python src/bin/h_get_currency_xchng.py


.PHONY: test
test: venv
	$(VENV)/python -m unittest tests/test_unit_h_get_currency_xchng.py
	$(VENV)/python -m unittest tests/test_integration_h_get_currency_xchng.py


include Makefile.venv
Makefile.venv:
	curl \
		-o Makefile.fetched \
		-L "https://github.com/kylasam/Makefile.venv/raw/v2020.02.26/Makefile.venv"
	echo "e0aeebe87c811fd9dfd892d4debb813262646e3e82691e8c4c214197c4ab6fac *Makefile.fetched" \
		&& mv Makefile.fetched Makefile.venv
