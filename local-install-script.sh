#! /bin/bash

# These lines must be manually performed for some reason:
# virtualenv --python=python3.6 --system-site-packages <name>
# source <name>/bin/activate

# These following lines can be run automatically:
echo '-----------------0/5'
clear
echo '-----------------3.1/5'
pip3 install -r requirements.txt
echo '-----------------3.2/5'
pip3 install scipy sklearn pandas matplotlib nltk
echo '-----------------3.2/5'
pip3 install --upgrade tensorflow-gpu
echo '-----------------4/5'
python -c 'import matplotlib; print("----------(matplotlib import success)")'
echo '-----------------5/5'
pip3 install ipython ipykernel
pip3 install jupyter
