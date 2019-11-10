#include "sciter-x.h"
#include "sciter-x-window.hpp"

class frame: public sciter::window {
public:
  frame() : window(SW_TITLEBAR | SW_RESIZEABLE | SW_CONTROLS | SW_MAIN | SW_ENABLE_DEBUG) {}

  // map of native functions exposed to script:
  BEGIN_FUNCTION_MAP
    FUNCTION_0("nativeMessage", nativeMessage);
    FUNCTION_0("getArgv", getArgv);
  END_FUNCTION_MAP
  // function expsed to script:
  sciter::string  nativeMessage() { return WSTR("Hello C++ World"); }
  sciter::value   getArgv() {
    std::vector<sciter::string> argv = sciter::application::argv();
    sciter::value arr[argv.size()];
    for( unsigned int i = 0; i < argv.size() ; i++)
      arr[i] = sciter::value(argv[i]);
    return sciter::value::make_array( sciter::application::argv().size(), arr ); }
};

#include "resources.cpp" // resources packaged into binary blob.

int uimain(std::function<int()> run ) {
  // enable features you may need in your scripts:
  SciterSetOption(NULL, SCITER_SET_SCRIPT_RUNTIME_FEATURES,
    ALLOW_FILE_IO |
    ALLOW_SOCKET_IO | // NOTE: the must for communication with Inspector
    ALLOW_EVAL |
    ALLOW_SYSINFO);

  sciter::archive::instance().open(aux::elements_of(resources)); // bind resources[] (defined in "resources.cpp") with the archive

  aux::asset_ptr<frame> pwin = new frame();

  // note: this:://app URL is dedicated to the sciter::archive content associated with the application
  pwin->load( WSTR("this://app/main.html") );
  //or use this to load UI from
  //  pwin->load( WSTR("file:///home/andrew/Desktop/Project/res/main.htm") );

  pwin->expand(true);

  return run();
}
