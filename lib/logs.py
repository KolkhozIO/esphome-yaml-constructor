import asyncio
import sys
import platform

from bitstring import xrange

from db import models


def get_hash_from_db_logs(db, hash_yaml):
    return db.query(models.Filename).filter(models.Filename.hash_yaml == hash_yaml).first()


async def _read_stream(stream, cb):
    while True:
        line = await stream.readline()
        if line:
            cb(line)
        else:
            break


async def _stream_subprocess(cmd):
    process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, universal_newlines=True)

    await asyncio.wait([
        _read_stream(process.stdout, lambda x: print("STDOUT: %s" % x)),
        _read_stream(process.stderr, lambda x: print("STDERR: %s" % x))
    ])
    return await process.wait()


def execute(cmd):
    loop = asyncio.get_event_loop()
    rc = loop.run_until_complete(_stream_subprocess(cmd))
    loop.close()
    return rc
