rm -rf ./docs
mkdir docs
cd _docs
make clean
make html
rm -rf 
cp -R _build/html/* ../docs