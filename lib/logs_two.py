# import asyncio
#
#
# async def _read_stream(stream):
#     while True:
#         line = await stream.readline()
#         if line:
#             yield line
#         else:
#             break
#
#
# async def _stream_subprocess(cmd):
#     process = await asyncio.create_subprocess_shell(cmd,
#                                                     stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
#
#     # await asyncio.wait([
#     #     _read_stream(process.stdout)
#     # ])
#     line = await _read_stream(process.stdout)
#     print(line)
#     return line
#
#
# def execute(cmd):
#     loop = asyncio.get_event_loop()
#     rc = loop.run_until_complete(_stream_subprocess(cmd))
#     loop.close()
#     print(type(rc))
#     print(rc)
#     return rc
#
#
# print(execute("esphome compile ../tests/testone.yaml"))
