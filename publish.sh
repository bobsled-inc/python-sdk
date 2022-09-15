rm -r ./dist/*
python3 -m build
twine upload dist/*