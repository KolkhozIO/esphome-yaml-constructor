import asyncio


async def _read_stream(stream, cb):
    while True:
        line = await stream.read(256)
        if line:
            cb(line)
        else:
            break


async def _stream_subprocess(cmd):
    process = await asyncio.create_subprocess_exec(*cmd,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)


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


print(execute("esphome compile ./uploaded_files/test.yaml"))
