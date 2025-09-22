mv .local ~/
python -m venv ~/.local/share/lrx/.venv
source ~/.local/share/lrx/.venv/bin/activate
pip install -r ~/.local/share/lrx/requirements.txt
deactivate

