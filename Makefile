multitude:
	@PYTHONPATH=multitude-cli python -m multitude-cli

watch:
	@watch -t -c -n1 PYTHONPATH=multitude-cli python -m multitude-cli

