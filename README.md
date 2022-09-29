# F1 Telemetry WIP

This project uses Electron and React to create a desktop application that shows live telemetry from the F1 22 game.

Current working branch is 22udp, which is working on switching from the 2020 udp spec to the 22 spec



devnote: run npm run dev to run in electron
does not automatically create the python server right now, although can be setup by uncommenting the code in electron.js and using "pyinstaller -F server.py" in order to create the server executable
