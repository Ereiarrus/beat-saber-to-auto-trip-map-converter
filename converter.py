import json
from pathlib import Path
import os, os.path
import errno
import glob, shutil

# Taken from https://stackoverflow.com/a/600612/119527
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')



bs_map_json = {}
bs_info_json = {}
at_map_json = {}

base_directory = Path(__file__).parent
bs_directory = base_directory / "examples" / "BS" / "4d2be (1-800 - Alice)"
bs_map_file_path = bs_directory / "EasyStandard.dat"
bs_info_file_path = bs_directory / "Info.dat"
# at_map_file_path = base_directory / "examples" / "AT" / "Yakuza 0 • Friday Night - Jenolin" / "Yakuza 0 - Friday Night - Jenolin.ats"

with open(bs_map_file_path, 'r') as bs_map_file:
    bs_map_json = json.load(bs_map_file)
with open(bs_info_file_path, 'r') as bs_info_file:
    bs_info_json = json.load(bs_info_file)
# with open(at_map_file_path, 'r') as at_map_file:
#     at_map_json = json.load(at_map_file)

at_map_output_json = {}


# Save outputs
output_dir = base_directory / "output"
with safe_open_w(output_dir / (bs_info_json["_songAuthorName"] + " - " + bs_info_json["_songName"] + " " + bs_info_json["_songSubName"] + " - " + bs_info_json["_levelAuthorName"] + ".ats")) as output_file:
    output_file.write(json.dumps(at_map_output_json))

shutil.copy2(
        bs_directory / bs_info_json["_songFilename"], 
        output_dir / (bs_info_json["_songName"] + " - " + bs_info_json["_songAuthorName"] + " " + bs_info_json["_songSubName"] + ".ogg")
)

