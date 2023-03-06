# async def _read_stream(stream):
#     while True:
#         line = stream.readline()
#         if line:
#             yield line
#         else:
#             break


# async def _stream_subprocess(cmd):
#     process = await asyncio.create_subprocess_shell(cmd,
#                                                     stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)

    # line = await asyncio.wait([
    #     _read_stream(process.stdout)
    # ])
    # line = _read_stream(process.stdout)
    # async for line in _read_stream(process.stdout):
    #     print(line)
    #     yield line
    # print(line)
    # return line
    # return _read_stream(process.stdout)


# def execute(cmd):
#     loop = asyncio.get_event_loop()
#     rc = loop.run_until_complete(_stream_subprocess(cmd))
#     print(rc)
#     loop.close()
#     return rc


# print(execute("esphome compile ../tests/testone.yaml"))
# asyncio.run(_stream_subprocess("esphome compile ../tests/testone.yaml"))

