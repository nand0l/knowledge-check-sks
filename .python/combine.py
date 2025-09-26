import os
from pathlib import Path

base_folder = Path(__file__).parent.resolve()
app_root_folder = os.path.dirname(base_folder)
src_folder = os.path.join(app_root_folder, 'src')
audiolinks = os.path.join(src_folder, 'audiolinks2.js')
csv_file = os.path.join(src_folder, 'output.csv')


