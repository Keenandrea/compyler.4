
.PHONY: help scanner clean

.DEFAULT: help
help:
	@echo "Program Invocation (Python 2.7):"
	@echo "	python main.py"
	@echo "	python main.py [file]"
	@echo "	python main.py < [file].fs19"

clean:
	rm -rf *.pyc
