project('myapp', 'cpp')
sciterinclude = include_directories('/home/adabru/desktop/sciter/include')

if meson.get_cross_property('platform') == 'linux'
  dependencies = [
    dependency('gtk+-3.0'),
    meson.get_compiler('cpp').find_library('libsciter-gtk', dirs: '/home/adabru/desktop/sciter/bin.gtk/x64'),
    meson.get_compiler('cpp').find_library('dl')
  ]
elif meson.get_cross_property('platform') == 'windows'
  dependencies = []
  add_project_link_arguments('-municode', language:'cpp')
endif

executable(
  'myapp',
  meson.get_cross_property('src'),
  dependencies : dependencies,
  include_directories : sciterinclude
)
