import subprocess

from settings import UPLOADED_FILES_PATH


def test_xxx(mocker):
    cmd = f"esphome compile .{UPLOADED_FILES_PATH}testone.yaml"
    mocker.spy(subprocess, 'call')
    subprocess.call(cmd)
    assert subprocess.call.call_count == 1