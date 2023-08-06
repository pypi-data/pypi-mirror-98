from pathlib import Path
from os.path import realpath, dirname
from typing import List


HERE = Path(dirname(realpath(__file__)))
ROOT = HERE / "files"
TEXT = ROOT / "text"
IMAGE = ROOT / "image"
AUDIO = ROOT / "audio"
VIDEO = ROOT / "video"


def all():
    return texts() + images() + audios() + videos()


def texts(ext=None) -> List[Path]:
    files = sorted(TEXT.rglob("*"))
    if ext is None:
        return files
    filtered = []
    for fp in files:
        if fp.as_posix().endswith(ext):
            filtered.append(fp)
    return filtered


def images(ext=None) -> List[Path]:
    files = sorted(IMAGE.rglob("*"))
    if ext is None:
        return files
    filtered = []
    for fp in files:
        if fp.as_posix().endswith(ext):
            filtered.append(fp)
    return filtered


def audios(ext=None) -> List[Path]:
    files = sorted(AUDIO.rglob("*"))
    if ext is None:
        return files
    filtered = []
    for fp in files:
        if fp.as_posix().endswith(ext):
            filtered.append(fp)
    return filtered


def videos(ext=None) -> List[Path]:
    files = sorted(VIDEO.rglob("*"))
    if ext is None:
        return files
    filtered = []
    for fp in files:
        if fp.as_posix().endswith(ext):
            filtered.append(fp)
    return filtered
