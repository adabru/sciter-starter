# Sciter-Starter

Sciter-Starter tries to provide the simplest possible way to setup a sciter project that is developed on linux and targets windows and linux.

## Installation

To install execute following command:

```
curl -o- https://raw.githubusercontent.com/adabru/sciter-starter/master/install.sh | bash
```

The script clones the sciter-starter repository to ~/.sciter and adds the python-script `sciter-starter.py` to your ~/bin folder. Alternatively, you can paste its contents into your terminal:

```sh
TMPDIR=$(mktemp -d)
wget -O $TMPDIR/master.tar.gz https://codeload.github.com/adabru/sciter-starter/tar.gz/master
tar -xzf $TMPDIR/master.tar.gz
mv $TMPDIR/sciter-starter-master ~/.sciter
cp ~/.sciter/sciter-starter.py ~/bin
```

## IDE

The template works without any IDE, i.e. just with a text editor. Though, for debugging, code hints and "go to definition" IDE settings are needed. You can specify an IDE during template initialization, currently only vscode is supported. Of course you can setup your own IDE. The file `Tupfile` can give you hints on which settings to apply.

## Get Started

This section is a little tutorial on how to start coding with sciter-sdk and this helper-package. After installing sciter-starter, you should be able to run `sciter-starter.py` from your command line. If not, please look through the installation steps a second time or open an issue.

Now open your terminal at a completely empty folder. When you run `sciter-starter.py` without arguments, a help text is written to the terminal with usage information. If this is your first project with sciter-starter or you want to update to the most recent sdk-version, run `sciter-starter.py update` to download the most recent sciter-sdk-version as released by c-smile. Only the most recent version is kept and stored at `~/.sciter/sciter-sdk`.

The download will be about 100-200MB. When the download has finished, run `sciter-starter.py --ide vscode` inside your empty folder to copy the template into your folder. If you use another ide than vscode, omit the ide option and submit a feature request on this repo's issues section for your specific IDE or a pull request (if you can ;).

After you initialized your folder, you can preview your gui-app with the program `scapp`, provided by the sciter-sdk. So type `sciter-starter.py preview` and your app will show up in its beauty!

When you distribute your app, you can either just put your html files with the `scapp` program into one folder (see https://sciter.com/scapp/ for more details) or compile your app with dynamic linking to sciter. If you wrote c++ code, you can't use the `scapp` program and must compile your app. If you have money, you can also buy sciter's static libraries to create one standalone executable file. But you can also have full functionality and sell your program without buying anything. To compile your program, run `sciter-starter.py build`. This command will create the executables and copy the needed libraries to the folders `build-linux` and `build-win`.

To distribute your app, you need to zip the app/app.exe and all *.so/*.dll and send them to whoever you like. On linux you need to specify the the LD_LIBRARY_PATH environment variable to enable loading the shared library, e.g. with the command `LD_LIBRARY_PATH=./build-linux/. ./build-linux/app`.

To rebuild your app after you made changes, you just need to rerun `sciter-starter.py build`. You can also manually run `tup` instead. But if you updated your sciter-sdk version you either need to run `sciter-starter.py build` again or `tup -jupdater.full_deps=1`.

Now that you can preview your app (`sciter-starter.py preview`) and build it (`sciter-starter.py build`), let us make a change to the current program.

Open the file `ui/main.html` and change the text `Hello world!` to `Hello universe!`. Save and run `sciter-starter.py preview`.

Open the file `ui/style.css`, add the line `color: red;` to the body section and restart the preview.

Now let's add code so that we can reload the page by pressing `Ctrl`+`R`. For that we need to use [TIScript](https://sciter.com/developers/sciter-docs/script/). TIScript is a Javascript-similar language that is specialized for using sciter. It needs some time to get familiar with but it has the advantages over Javascript which a specialized language typically have. If you want to find out how to write some function, you can inspect sciter's offline manual or its website with a decent amount of information. You start the offline manual by running `sciter-starter.py manual` and pressing the help button. The online documenation is on <https://sciter.com>. You can find tutorials, articles and, probably most importantly, [sciter's forums](https://sciter.com/forums/). If you don't find your answer, you will usually get a reply in the forums really fast. Alternatively you can post your question on [stackoverflow](https://stackoverflow.com) using the tag `sciter`.

To add page reload on `Ctrl`+`R`, we add following section to our main.html:

```
<script type="text/tiscript">
  event keydown ( evt ) {
    if (evt.ctrlKey && String.fromCharCode(evt.keyCode).toLowerCase() == 'r')
      view.load(this.url())
  }
</script>
```

You have to browse sciter's webpage to find out all information you need for writing this piece of code. After that, restart `sciter-starter.py preview` and try out to make changes to your html file and reloading the page with `ctrl`+`r`.

To debug the code we use sciter's inspector. Start it with `sciter-starter.py inspector`. Then focus the app preview and press `ctrl`+`shift`+`i` to connect with the inspector. Furthermore you can use `stdout.println` statements to output debug information from your code.


Now let's make a change to our C++ code. To do so, add the following code to your main.html:

```
function self.ready() {
  // calling native method defined in main.cpp
  $(body).text = view.nativeMessage();
}
```

The function nativeMessage is defined in main.cpp . Change the string "Hello C++ World" to "Hello C++ universe!". To use your own main.cpp instead of sciter's scapp, you have to compile it. Run `sciter-starter.py build`. That will compile the linux and windows binaries. Run your linux build with `LD_LIBRARY_PATH=./build-linux/. ./build-linux/app`

This tutorial was partly compiled from sciter's official [tutorials](https://sciter.com/tutorials/).

## About

A more complete templating repository can be found on: <https://github.com/ramon-mendes/SciterBootstrap> . Please use that if it suits your needs. This tool is meant to be used on Linux to create a project-template that uses the [sciter-sdk](https://sciter.com) and can be compiled for windows (via mingw) and linux.

This tool depends on python, python-requests, tup, mingw-w64-gcc, curl, wget, git.

Credits go to c-smile for developing the sciter framework which gives us the power to develop web-apps with a low resource footprint.