"""Async and await example using subprocesses

Note:
    Requires Python 3.6.
"""

import os
import sys
import time
import platform
import asyncio


async def run_command_shell(command):
    """Run command in subprocess (shell)

    Note:
        This can be used if you wish to execute e.g. "copy"
        on Windows, which can only be executed in the shell.
    """
    # Create subprocess
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT)

    # Status
    print('Started:', command, '(pid = ' + str(process.pid) + ')')

    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()

    # Progress
    if process.returncode == 0:
        print('Done:', command, '(pid = ' + str(process.pid) + ')')
    else:
        print('Failed:', command, '(pid = ' + str(process.pid) + ')')

    # Result
    result = stdout.decode().strip()

    # Real time print
    print(result)

    # Return stdout
    return result


def make_chunks(l, n):
    """Yield successive n-sized chunks from l.

    Note:
        Taken from https://stackoverflow.com/a/312464
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def run_asyncio_commands(tasks, max_concurrent_tasks=0):
    """Run tasks asynchronously using asyncio and return results

    If max_concurrent_tasks are set to 0, no limit is applied.

    Note:
        By default, Windows uses SelectorEventLoop, which does not support
        subprocesses. Therefore ProactorEventLoop is used on Windows.
        https://docs.python.org/3/library/asyncio-eventloops.html#windows
    """

    all_results = []

    if max_concurrent_tasks == 0:
        chunks = [tasks]
    else:
        chunks = make_chunks(l=tasks, n=max_concurrent_tasks)

    for tasks_in_chunk in chunks:
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)

        commands = asyncio.gather(*tasks_in_chunk)  # Unpack list using *
        results = loop.run_until_complete(commands)
        all_results += results
        loop.close()
    return all_results


if __name__ == '__main__':

    start = time.time()

    cmd = "esphome compile ../tests/testone.yaml"

    tasks = []
    tasks.append(run_command_shell(cmd))

    # # Shell execution example
    # tasks = [run_command_shell('copy c:/somefile d:/new_file')]

    # # List comprehension example
    # tasks = [
    #     run_command(*command, get_project_path(project))
    #     for project in accessible_projects(all_projects)
    # ]

    results = run_asyncio_commands(tasks, max_concurrent_tasks=20)  # At most 20 parallel tasks
    print('Results:', results)

    end = time.time()
    rounded_end = ('{0:.4f}'.format(round(end - start, 4)))
    print('Script ran in about', str(rounded_end), 'seconds')
