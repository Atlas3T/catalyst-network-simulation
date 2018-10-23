
default: peer_dist_cy

peer_dist_cy: setup.py
	python setup.py build_ext --inplace && rm -Rf build

docpages:
		cd docs
		sphinx-apidoc -fMe -o ./source/ ../simlib/
		make html
		cd ..


