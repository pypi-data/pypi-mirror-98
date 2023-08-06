$env:Path += ";C:\Python39"
$env:Path += ";C:\Program Files\Git\bin"

python -m pip install setuptools
python -m pip install wheel
python setup.py test
