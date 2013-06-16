all:
	python setup.py py2app

debug:
	python setup.py py2app -A

clean:
	rm -rf build dist