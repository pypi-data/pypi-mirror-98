python setup.py sdist bdist_wheel
cd dist
pip uninstall aiotcloud
pip install aiotcloud-2.0.0-py3-none-any.whl
cd ..
rm -r dist