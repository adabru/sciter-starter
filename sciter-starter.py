#!/usr/bin/python

import os, requests, sys, subprocess, shutil, tarfile

def download_file(url, dest):
  def showprogress(i, n, prefix='', size=60):
    x = int(i / n * size)
    sys.stdout.write("%s[%s%s] %i%% %i/%i\r" % (prefix, "#"*x, "."*(size-x), 100*i/n, i, n))
    sys.stdout.flush()

  response = requests.get(url, stream=True)
  # estimate size (~110MB) if not given
  size = int(response.headers.get('Content-Length', '110000000').strip())
  written = 0
  file = []
  update_counter = 0
  with open(os.path.expanduser(dest), 'wb') as file:
    for buf in response.iter_content(chunk_size=1024):
      if buf:
        file.write(buf)
        written += len(buf)
        update_counter += 1
        if update_counter % 100 == 0:
          showprogress(written, size, 'Download %s' % (url))
    showprogress(written, size, 'Download %s' % (url))
  print('Download comnplete.')

def updatesdk():
  remote_sha1 = subprocess.run('git ls-remote https://github.com/c-smile/sciter-sdk master'.split(' '), capture_output=True, text=True).stdout.split('\t')[0]
  download = False
  if not os.path.exists( os.path.expanduser('~/.sciter/sciter-sdk_sha1') ):
    print('No sciter sdk found.')
    download = True
  else:
    local_sha1 = 0
    with open( os.path.expanduser('~/.sciter/sciter-sdk_sha1') ) as file:
      local_sha1 = file.read()
    if local_sha1 != remote_sha1:
      print('Local sciter sdk out of date, downloading newer one...')
      download = True
    else:
      print('Local sdk is up to date.')
  if download:
    download_file('https://api.github.com/repos/c-smile/sciter-sdk/tarball/%s' % (remote_sha1), os.path.expanduser('~/.sciter/sciter-sdk.tar.gz'))
    print('Extracting downloading...')
    with tarfile.open( os.path.expanduser('~/.sciter/sciter-sdk.tar.gz') ) as tar:
      # extract top-level folder
      def members():
        for member in tar.getmembers():
          if '/' in member.path:
            member.path = '/'.join(member.path.split('/')[1:])
            yield member
      tar.extractall(members=members(), path=os.path.expanduser('~/.sciter/sciter-sdk'))
    with open( os.path.expanduser('~/.sciter/sciter-sdk_sha1'), 'wb' ) as file:
      file.write(remote_sha1.encode('utf8'))
    print('Extraction complete.')
    print('Update complete.')

def init_template():
  if len(os.listdir()) > 0:
    print('The current working directory is not empty, aborting!')
    exit()
  print('copy Tupfile')
  shutil.copyfile(os.path.expanduser('~/.sciter/Tupfile'), 'Tupfile')
  print('copy build-linux')
  shutil.copytree(os.path.expanduser('~/.sciter/build-linux'), 'build-linux')
  print('copy build-win')
  shutil.copytree(os.path.expanduser('~/.sciter/build-win'), 'build-win')
  print('copy ui')
  shutil.copytree(os.path.expanduser('~/.sciter/ui'), 'ui')
  print('copy main.cpp')
  shutil.copyfile(os.path.expanduser('~/.sciter/main.cpp'), 'main.cpp')
  print('init tup build system')
  subprocess.run('tup init'.split(' '))
  if len(sys.argv) >= 4 and sys.argv[2] == '--ide' and sys.argv[3] == 'vscode':
    print('copy .vscode')
    shutil.copytree(os.path.expanduser('~/.sciter/ide/vscode'), '.vscode')

def preview():
  path = len(sys.argv) >= 3 and sys.argv[2] or './ui/main.html'
  if not os.path.exists( path ):
    print('The file %s does not exist.' % (path))
    exit()
  subprocess.run( [os.path.expanduser('~/.sciter/sciter-sdk/bin.gtk/x64/scapp'), path] )

def inspector():
  subprocess.run( [os.path.expanduser('~/.sciter/sciter-sdk/bin.gtk/x64/inspector')] )

def build():
  subprocess.run('tup -jupdater.full_deps=1'.split(' '))


if len(sys.argv) < 2:
  print(('usage:\n\n   \033[1msciter-starter.py\033[22m (update|init|preview|build)\n\n'
         'update                      Update the sdk.\n'
         'init    [--ide vscode]      Init template in the current working directory. If --ide is given,\n'
         '                            IDE-specific files are created. Currently only vscode is supported.\n'
         'preview [path]              Preview your ui with scapp. Path defaults to ./ui/main.html.\n'
         'inspector                   Start the inspector.\n'
         'build                       Compile your project in a distributable format for windows and linux.\n'
         '\n\n'))
  exit()

if sys.argv[1] == 'update':
  updatesdk()
elif sys.argv[1] == 'init':
  init_template()
elif sys.argv[1] == 'preview':
  preview()
elif sys.argv[1] == 'inspector':
  inspector()
elif sys.argv[1] == 'build':
  build()
