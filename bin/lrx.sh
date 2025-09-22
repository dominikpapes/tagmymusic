#!/bin/bash
source 	~/.tagmymusic/.venv/bin/activate
pip install -r requirements.txt
python3 ~/.tagmymusic/lrx.py ~/Music/.lyrics
deactivate
