import json
from mutagen.oggvorbis import OggVorbis
from pathlib import Path
import os, os.path
import errno
from fractions import Fraction
import glob, shutil
import hashlib
import random

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

def seed_from_string(s: str) -> int:
    digest = hashlib.sha256(s.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")  # 64-bit seed


bs_map_json = {}
bs_info_json = {}
at_map_json = {}

base_directory = Path(__file__).parent
bs_directory = base_directory / "examples" / "BS" / "4d2be (1-800 - Alice)"
bs_map_file_path = bs_directory / "EasyStandard.dat"
bs_info_file_path = bs_directory / "Info.dat"

with open(bs_map_file_path, 'r') as bs_map_file:
    bs_map_json = json.load(bs_map_file)
with open(bs_info_file_path, 'r') as bs_info_file:
    bs_info_json = json.load(bs_info_file)

at_song_file_name = bs_info_json["_songName"] + " - " + bs_info_json["_songAuthorName"] + " " + bs_info_json["_songSubName"] + ".ogg"
beats_per_measure = 4  # TODO: un-hardcode?
at_map_output_json = {
    "metadata": {
        "custom": True,
        "authorID": {
            "platformID": "OC",
            "displayName": bs_info_json["_levelAuthorName"],
        },
        "songID": "BEAT SABER IMPORT",
        "title": bs_info_json["_songName"],
        "artist": bs_info_json["_songAuthorName"],
        "koreography": {
            "m_FileID": 0,
            "m_PathID": 0
        },
        "descriptor": "",
        "sceneName": "Universal",
        "avgBPM": bs_info_json["_beatsPerMinute"],
        "tempoSections": [{
                "startTimeInSeconds": 4.0,
                "beatsPerMeasure": beats_per_measure,
                "beatsPerMinute": bs_info_json["_beatsPerMinute"],
                "doesStartNewMeasure": False
            }, {
                "startTimeInSeconds": 4.001,
                "beatsPerMeasure": beats_per_measure,
                "beatsPerMinute": bs_info_json["_beatsPerMinute"],
                "doesStartNewMeasure": True
            }
        ],
        "songEventTracks": [],
        "songFilename": at_song_file_name,
        "firstBeatTimeInSeconds": 0.0,
        "songShortStartTimeInSeconds": 0,
        "songShortStopTimeInSeconds": 0,
        "songShortLengthInSeconds": 0,
        "songStartFadeTime": 0,
        "songEndFadeTime": 0,
        "previewStartInSeconds": 30.0,
        "previewDurationInSeconds": 10.0,
        "songStartBufferInSeconds": 0.0,
        "choreoJSONs": [],
        "animClips": [],
        "speed": 0.0,
        "quantizeSize": 0.10000000149011612,
        "includeInArcades": True,
        "supportedModalitySets": 2,
        "drumMedSFX": "",
        "drumMaxSFX": ""
    }
}
at_map_output_json["choreographies"] = {}
at_map_output_json["choreographies"]["list"] = []
at_map_output_json["choreographies"]["list"].append({})
at_map_output_json["choreographies"]["list"][0]["header"] = {
                    "id": "cust_beat_saber_map",
                    "descriptor": "",
                    "name": "Easy",  # TODO: this is the difficulty name; take it from the filename OR Info.dat on beat saber
                    "metadata": "",
                    "spawnAheadTime": {  # TODO: is the the JD of the map?
                        "beat": 8,
                        "numerator": 0,
                        "denominator": 1
                    },
                    "gemSpeed": 18.0,  # TODO: should probably grab from Info.dat - "_noteJumpMovementSpeed"
                    "gemRadius": 1.0,
                    "handRadius": 0.27000001072883608,
                    "animClipPath": "",
                    "buildVersion": "",
                    "requiredModalities": 2,
                    "choreoType": 0
                }
at_map_output_json["choreographies"]["list"][0]["data"] = {"events": []}
at_events = at_map_output_json["choreographies"]["list"][0]["data"]["events"]


song_file = bs_directory / bs_info_json["_songFilename"]
song_length = OggVorbis(song_file).info.length
at_map_output_json["metadata"]["songEndTimeInSeconds"] = song_length  # TODO; also, can we just not have these numbers? would they be inferred?
at_map_output_json["metadata"]["songFullLengthInSeconds"] = song_length  # TODO; also, can we just not have these numbers? would they be inferred?

bs_x_range = 3  # left-most centre to right-most in-line
bs_y_range = 2  # bottom-most centre to top-most centre in-line
at_x_range = 2.5  # TODO: player customisable
at_y_range = 1.5  # TODO: player customisable
at_y_min = 0.3  # TODO: player customisable
x_scale = at_x_range / bs_x_range
y_scale = at_y_range / bs_y_range
x_wobble_factor = 0.1  # TODO: player customisable
y_wobble_factor = 0.1  # TODO: player customisable
x_wobble = x_scale * x_wobble_factor
y_wobble = y_scale * y_wobble_factor
offsets = [  # remember the y axis is flipped here - top is at bottom, bottom is on top
    [(-x_scale*3/2, at_y_min + y_scale/2),   (-x_scale/2, at_y_min + y_scale/2),   (x_scale/2, at_y_min + y_scale/2),   (x_scale*3/2, at_y_min + y_scale/2)],
    [(-x_scale*3/2, at_y_min + y_scale*3/2), (-x_scale/2, at_y_min + y_scale*3/2), (x_scale/2, at_y_min + y_scale*3/2), (x_scale*3/2, at_y_min + y_scale*3/2)],
    [(-x_scale*3/2, at_y_min + y_scale*5/2), (-x_scale/2, at_y_min + y_scale*5/2), (x_scale/2, at_y_min + y_scale*5/2), (x_scale*3/2, at_y_min + y_scale*5/2)],
]
random.seed(seed_from_string(at_song_file_name))
for e in bs_map_json["colorNotes"]:
    beat = e["b"]
    f = Fraction(beat).limit_denominator(beats_per_measure)
    whole_beat = f.numerator // f.denominator
    remainder = f - whole_beat
    x_pos, y_pos = offsets[e["y"]][e["x"]]  # TODO: do we want to add a randomness factor to this? just so they don't all look exactly the same positioned
    x_pos += x_wobble * (random.random() * 2 - 1)
    y_pos += y_wobble * (random.random() * 2 - 1)
    at_events.append(
        {
            "type": (1 if e["c"] == 0 else 2),  # TODO
            "hasGuide": False,
            "time": {
                "beat": whole_beat,
                "numerator": remainder.numerator,
                "denominator": remainder.denominator
            },
            "beatDivision": 2,
            "position": {
                "x": x_pos,
                "y": y_pos,
                "z": 0.0
            },
            "subPositions": [],
            "broadcastEventID": 0
        }
    )
    # print(at_events)


"""
https://bsmg.wiki/mapping/map-format/beatmap.html explains the meanings:
{
    "b": 5,
    "x": 2,
    "y": 0,
    "a": 0,
    "c": 1,
    "d": 1 
}
"""


# Save outputs
output_dir = base_directory / "output"
with safe_open_w(output_dir / (bs_info_json["_songAuthorName"] + " - " + bs_info_json["_songName"] + " " + bs_info_json["_songSubName"] + " - " + bs_info_json["_levelAuthorName"] + ".ats")) as output_file:
    output_file.write(json.dumps(at_map_output_json))

shutil.copy2(song_file, output_dir / at_song_file_name)

