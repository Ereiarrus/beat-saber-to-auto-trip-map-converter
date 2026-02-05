import argparse
import errno
import hashlib
import json
import os
import os.path
import random
import shutil
import string
import zipfile
from fractions import Fraction
from pathlib import Path
from typing import Any

import pyrfc6266
import requests
from mutagen.oggvorbis import OggVorbis


def random_id(length: int = 64):
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


# Taken from https://stackoverflow.com/a/600612/119527
def mkdir_p(path: str) -> None:
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def safe_open_w(path: os.PathLike[str] | str, mode: str = "w"):
    """Open "path" for writing, creating any parent directories as needed."""
    mkdir_p(os.path.dirname(path))
    return open(path, mode)


def seed_from_string(s: str) -> int:
    digest = hashlib.sha256(s.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")  # 64-bit seed


def converter(
    bsr_code: str,
    at_output_dir: Path,
    at_x_range: float,
    at_y_range: float,
    at_y_min: float,
    at_njs_multiplier: float,
    bs_arrows_as_directionals: bool,  # TODO (c4)
    bs_bombs_as_walls: bool,  # TODO (c2)
    bs_stacks_as_drums: bool,  # TODO (c3)
    x_wobble_factor: float,
    y_wobble_factor: float,
    base_directory: Path,
    beatsaver_api_url: str,
) -> None:
    map_metadata_response = requests.get(
        f"{beatsaver_api_url}/maps/ids/{bsr_code}"
    )
    map_metadata_response.raise_for_status()
    map_metadata = map_metadata_response.json()[bsr_code]
    map_download_url: str = map_metadata["versions"][0]["downloadURL"]
    map_downloads_dir: Path = base_directory / "downloaded"
    map_response = requests.get(map_download_url)
    map_response.raise_for_status()
    map_filename = pyrfc6266.requests_response_to_filename(map_response)
    map_zipfile_location = map_downloads_dir / map_filename
    with safe_open_w(map_zipfile_location, "wb") as file:
        file.write(map_response.content)
    map_folder_dir = map_downloads_dir / Path(map_filename).stem
    with zipfile.ZipFile(map_zipfile_location, "r") as zip_ref:
        zip_ref.extractall(map_folder_dir)
    os.remove(map_zipfile_location)

    bs_downloaded_maps_dir: Path = map_folder_dir
    bs_info_file_path: Path = bs_downloaded_maps_dir / "Info.dat"
    bs_info_json: dict[str, Any]
    with open(bs_info_file_path) as bs_info_file:
        bs_info_json = json.load(bs_info_file)

    _difficultyBeatmaps = bs_info_json["_difficultyBeatmapSets"][0][
        "_difficultyBeatmaps"
    ]
    difficulty_files: list = [
        _difficultyBeatmaps[i]["_beatmapFilename"]
        for i in range(len(_difficultyBeatmaps))
    ]

    at_song_file_name: str = (
        bs_info_json["_songName"]
        + " - "
        + bs_info_json["_songAuthorName"]
        + " "
        + bs_info_json["_songSubName"]
        + ".ogg"
    )
    random.seed(seed_from_string(at_song_file_name))

    beats_per_measure: int = 4  # TODO (5)
    at_map_output_json: dict[str, Any] = {
        "metadata": {
            "custom": True,
            "authorID": {
                "platformID": "OC",
                "displayName": bs_info_json["_levelAuthorName"],
            },
            "songID": random_id(64),
            "title": bs_info_json["_songName"],
            "artist": bs_info_json["_songAuthorName"],
            "koreography": {"m_FileID": 0, "m_PathID": 0},
            "descriptor": "",
            "sceneName": "Universal",
            "avgBPM": bs_info_json["_beatsPerMinute"],
            "tempoSections": [
                {
                    "startTimeInSeconds": 4.0,
                    "beatsPerMeasure": beats_per_measure,
                    "beatsPerMinute": bs_info_json["_beatsPerMinute"],
                    "doesStartNewMeasure": False,
                },
                {
                    "startTimeInSeconds": 4.001,
                    "beatsPerMeasure": beats_per_measure,
                    "beatsPerMinute": bs_info_json["_beatsPerMinute"],
                    "doesStartNewMeasure": True,
                },
            ],
            "songEventTracks": [],
            "songFilename": at_song_file_name,
            "firstBeatTimeInSeconds": 0.0,
            "songShortStartTimeInSeconds": 0,
            "songShortStopTimeInSeconds": 0,
            "songShortLengthInSeconds": 0,
            "songStartFadeTime": 0,
            "songEndFadeTime": 0,
            "previewStartInSeconds": bs_info_json["_previewStartTime"],
            "previewDurationInSeconds": bs_info_json["_previewDuration"],
            "songStartBufferInSeconds": 0.0,
            "choreoJSONs": [],
            "animClips": [],
            "speed": 0.0,
            "quantizeSize": 0.10000000149011612,
            "includeInArcades": True,
            "supportedModalitySets": 2,
            "drumMedSFX": "",
            "drumMaxSFX": "",
        },
        "choreographies": {"list": []},
    }
    for j, bs_map_file_name in enumerate(difficulty_files):
        bs_map_file_path: Path = bs_downloaded_maps_dir / bs_map_file_name

        bs_map_json: dict[str, Any] = {}

        with open(bs_map_file_path) as bs_map_file:
            bs_map_json = json.load(bs_map_file)
        at_map_output_json["choreographies"]["list"].append({})
        at_map_output_json["choreographies"]["list"][j]["header"] = {
            "id": "cust_beat_saber_map",
            "descriptor": "",
            "name": _difficultyBeatmaps[j]["_difficulty"],
            "metadata": "",
            "spawnAheadTime": {  # TODO (6)
                "beat": 8,
                "numerator": 0,
                "denominator": 1,
            },
            "gemSpeed": _difficultyBeatmaps[j]["_noteJumpMovementSpeed"]
            * at_njs_multiplier,  # TODO (7)
            "gemRadius": 1.0,
            "handRadius": 0.27000001072883608,
            "animClipPath": "",
            "buildVersion": "",
            "requiredModalities": 2,
            "choreoType": 0,
        }
        at_map_output_json["choreographies"]["list"][j]["data"] = {
            "events": []
        }
        at_events: list[dict[str, Any]] = at_map_output_json["choreographies"][
            "list"
        ][j]["data"]["events"]

        song_file: Path = (
            bs_downloaded_maps_dir / bs_info_json["_songFilename"]
        )
        song_length: float = OggVorbis(song_file).info.length
        at_map_output_json["metadata"]["songEndTimeInSeconds"] = song_length
        at_map_output_json["metadata"]["songFullLengthInSeconds"] = song_length

        bs_x_range: float = (
            3  # left-most centre to right-most in-line; # TODO (c1)
        )
        bs_y_range: float = 2  # bottom-most centre to top-most centre in-line
        x_scale: float = at_x_range / bs_x_range
        y_scale: float = at_y_range / bs_y_range
        x_wobble: float = x_scale * x_wobble_factor
        y_wobble: float = y_scale * y_wobble_factor
        positions: list[
            list[tuple[float, float]]
        ] = [  # remember the y axis is flipped here - top is at bottom, bottom is on top; TODO (c1): this needs to be bigger for maps with >4 lanes
            [
                (-x_scale * 3 / 2, at_y_min + y_scale / 2),
                (-x_scale / 2, at_y_min + y_scale / 2),
                (x_scale / 2, at_y_min + y_scale / 2),
                (x_scale * 3 / 2, at_y_min + y_scale / 2),
            ],
            [
                (-x_scale * 3 / 2, at_y_min + y_scale * 3 / 2),
                (-x_scale / 2, at_y_min + y_scale * 3 / 2),
                (x_scale / 2, at_y_min + y_scale * 3 / 2),
                (x_scale * 3 / 2, at_y_min + y_scale * 3 / 2),
            ],
            [
                (-x_scale * 3 / 2, at_y_min + y_scale * 5 / 2),
                (-x_scale / 2, at_y_min + y_scale * 5 / 2),
                (x_scale / 2, at_y_min + y_scale * 5 / 2),
                (x_scale * 3 / 2, at_y_min + y_scale * 5 / 2),
            ],
        ]
        for e in bs_map_json["colorNotes"]:
            beat: float = e["b"]
            f: Fraction = Fraction(beat).limit_denominator(beats_per_measure)
            whole_beat: int = f.numerator // f.denominator
            remainder: Fraction = f - whole_beat
            x_pos, y_pos = positions[e["y"]][e["x"]]
            x_pos += x_wobble * (random.random() * 2 - 1)
            y_pos += y_wobble * (random.random() * 2 - 1)
            at_events.append(
                {
                    "type": (1 if e["c"] == 0 else 2),  # TODO (conversions)
                    "hasGuide": False,
                    "time": {
                        "beat": whole_beat,
                        "numerator": remainder.numerator,
                        "denominator": remainder.denominator,
                    },
                    "beatDivision": 2,
                    "position": {"x": x_pos, "y": y_pos, "z": 0.0},
                    "subPositions": [],
                    "broadcastEventID": 0,
                }
            )

    # Save outputs
    output_dir: Path = at_output_dir / (
        bs_info_json["_songAuthorName"]
        + " • "
        + bs_info_json["_songName"]
        + " "
        + bs_info_json["_songSubName"]
        + " - "
        + bs_info_json["_levelAuthorName"]
    )
    with safe_open_w(
        output_dir
        / (
            bs_info_json["_songAuthorName"]
            + " - "
            + bs_info_json["_songName"]
            + " "
            + bs_info_json["_songSubName"]
            + " - "
            + bs_info_json["_levelAuthorName"]
            + ".ats"
        )
    ) as output_file:
        output_file.write(json.dumps(at_map_output_json))

    shutil.copy2(song_file, output_dir / at_song_file_name)

    shutil.rmtree(bs_downloaded_maps_dir)


def parse_args_and_run():
    default_base_dir = Path(__file__).parent
    default_at_output = (
        Path.home()
        / "AppData"
        / "LocalLow"
        / "Kinemotik Studios"
        / "Audio Trip"
        / "Songs"
    )
    parser = argparse.ArgumentParser(description="BSR to AT converter")
    parser.add_argument("bsr_code", help="BeatSaver BSR code")
    parser.add_argument(
        "--at-output-dir",
        type=Path,
        default=default_at_output,
        help=f"Output directory (default: {default_at_output})",
    )
    parser.add_argument(
        "--base-directory",
        type=Path,
        default=default_base_dir,
        help=f"Base directory (default: script directory: {default_base_dir})",
    )
    parser.add_argument("--at-x-range", type=float, default=1.5)
    parser.add_argument("--at-y-range", type=float, default=1.05)
    parser.add_argument("--at-y-min", type=float, default=0.4)
    parser.add_argument("--at-njs-multiplier", type=float, default=2.8)
    parser.add_argument(
        "--bs-arrows-as-directionals", type=bool, default=False
    )
    parser.add_argument("--bs-bombs-as-walls", type=bool, default=True)
    parser.add_argument("--bs-stacks-as-drums", type=bool, default=True)
    parser.add_argument("--x-wobble-factor", type=float, default=0.1)
    parser.add_argument("--y-wobble-factor", type=float, default=0.1)
    parser.add_argument(
        "--beatsaver-api-url",
        type=str,
        default="https://api.beatsaver.com/",
    )
    args = parser.parse_args()

    converter(
        bsr_code=args.bsr_code,
        at_output_dir=args.at_output_dir,
        at_x_range=args.at_x_range,
        at_y_range=args.at_y_range,
        at_y_min=args.at_y_min,
        at_njs_multiplier=args.at_njs_multiplier,
        bs_arrows_as_directionals=args.bs_arrows_as_directionals,
        bs_bombs_as_walls=args.bs_bombs_as_walls,
        bs_stacks_as_drums=args.bs_stacks_as_drums,
        x_wobble_factor=args.x_wobble_factor,
        y_wobble_factor=args.y_wobble_factor,
        base_directory=args.base_directory,
        beatsaver_api_url=args.beatsaver_api_url,
    )
