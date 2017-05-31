#include "mystl.h"
#include <iostream>
#include "myassert.h"

#ifndef STANDARD_ASSERT
void myerror(int line,const char *file,const char *expression)
{
  cerr << "(general.h):Assertion failed: '" << expression <<  "' ::: b " 
    << file << ":" << line << endl;
  cout << "(general.h):Assertion failed: '" << expression <<  "' ::: b " 
    << file << ":" << line << endl;
}
void imyerror(int line,const char *file,const char *expression)
{
  cerr << "Error: '" << expression <<  "' ::: in Source " << file 
    << ":" << line << endl;
}

#endif

