Having issues? Don't worry, it happens! Here are some common troubleshooting steps:

## "Command not found"

This usually means you're not using the development shell.
This shell provides you access to necessary commands and packages for the project.

How-to: [Starting the Development Environment](https://github.com/Zaczero/openstreetmap-ng/wiki/Contributing:-Getting-Started#2-starting-the-development-environment)

## "No such file or directory"

This often means you're in the wrong folder.
Make sure you're in the main project folder (the one with the `shell.nix` file) before running any commands.

## "No such file or directory" + uvloop, during application startup

If you see this error when starting the application and you're in the main folder, it might mean some helper services aren't running yet.

The application talks to a database through a special unix socket in the `data/postgres_unix` folder. If the database isn't running, this socket won't be there, resulting in the FileNotFoundError.

How-to: [Starting the Services](https://github.com/Zaczero/openstreetmap-ng/wiki/Contributing:-Getting-Started#3-starting-the-services)

## JavaScript files don't refresh in the browser

There might be a compilation error in the JavaScript code.
Check the `data/supervisor/watch-js.log` file or run the `dev-logs-watch-js` command for details.

## Visual Studio Code: "Git: `pre-commit` not found. Did you forget to activate your virtualenv?"

If you use WSL on Windows you need to install the [WSL extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl). Then reopen the editor using the `code .` command in the WSL terminal. You will need to [configure git](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup):
```bash
$ git config --global user.name "John Doe"
$ git config --global user.email johndoe@example.com
```
It is recommended to [set up creditential manager](https://code.visualstudio.com/docs/remote/troubleshooting#_sharing-git-credentials-between-windows-and-wsl).

## Other problems

If you're still having trouble, check the log files in the `data/supervisor` folder for clues about what might be going wrong.

## Need more help?

Feel free to [ask questions](https://github.com/Zaczero/openstreetmap-ng/issues)! We're a friendly community and happy to help you get started 😊.