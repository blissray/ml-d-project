#backend.ai run python:3.6-ubuntu18.04 -c "print('hello world')" -g beta-user

backend.ai run --rm -r cpu=4 -r mem=8g -r cuda.shares=1 python-tensorflow:2.0-py36 ./main.py -g beta-user
