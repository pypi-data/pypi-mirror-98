# Async Cmd2

Async extension to a famous [Cmd2](https://github.com/python-cmd2/cmd2) library.

Cmd2 permanently occupies the main thread which is a problem if you plan to receive callbacks on the main thread 
(e.g., by Bluetooth stack Bleak) 

## Pip installation

BoolTest is available via `pip`:

```
pip3 install ph4-acmd2
```

## Local installation

From the local dir:

```
pip3 install --upgrade --find-links=. .
```

## Usage

```python
import asyncio
import ph4acmd2

class CmdLineApp(ph4acmd2.Cmd):
    async def main(self):
        await self.acmdloop()
        print("Cmdloop finished now")

if __name__ == '__main__':
    app = CmdLineApp()
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(app.main())
```

## Limitations

We use [asyncio.lool.add_reader](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.add_reader) to read 
from the stdin and process the commands thus it is not currently possible to ue readline features such as auto-complete or
ctrl-r, UP-arrow for previous commands, etc...

Readline occupies main thread in a blocking way, so it is not compatible with runloop model running on the main thread
and executing coroutines. 

In order to use readline it needs to add async support. A potential workaround could be to access terminal in async way
e.g., submit short coroutine monitoring the terminal state to simulate readline library. However, it is not tested.  
