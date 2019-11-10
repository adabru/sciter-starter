#!/usr/bin/python

import os, requests, sys, subprocess

def download_file(url, dest):
  def showprogress(i, n, prefix='', size=60):
    x = int(i / n * size)
    sys.stdout.write("%s[%s%s] %i%% %i/%i\r" % (prefix, "#"*x, "."*(size-x), 100*i/n, i, n))
    sys.stdout.flush()

  response = requests.get(url, stream=True)
  # estimate size (~105MB) if not given
  size = int(response.headers.get('Content-Length', '105000000').strip())
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
    with open( os.path.expanduser('~/.sciter/sciter-sdk_sha1'), 'wb' ) as file:
      file.write(remote_sha1.encode('utf8'))
    print('')

updatesdk()
