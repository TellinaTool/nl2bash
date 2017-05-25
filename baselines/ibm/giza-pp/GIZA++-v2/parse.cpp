/*

EGYPT Toolkit for Statistical Machine Translation
Written by Yaser Al-Onaizan, Jan Curin, Michael Jahr, Kevin Knight, John Lafferty, Dan Melamed, David Purdy, Franz Och, Noah Smith, and David Yarowsky.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, 
USA.

*/

/* FJO 01/2001: completely reorganized parameter processing */

#include <sstream>
#include <string>
#include <fstream>
#include "defs.h"
#include "utility.h"
#include "Globals.h"
#include "D4Tables.h"
#include "D5Tables.h"
#include "ATables.h"
#include "Parameter.h"

extern bool ONLYALDUMPS;

void parseConfigFile (char * fname )
  // This functions reads in the configuration file to set up some run-time
  // parameters. The parameters are global variables that are defined in 
  // main.cc and used all over the place in the program
  // The format of the configuration file can be explained in the following way
  // FORMAT:
  // the character '\n' separates lines ..
  // lines that start with "//" (skipping over white spaces are considered 
  // as comments and will be ignored.
  // Any other line is considered as an attribute setting instruction and it 
  // is divided into haves (separated by a colon ":"). The first half is the
  // attribute value which consists of the concatenation of all non-white space
  // tokens before the colon. These tokens will have spaces eseparating them.
  // The attribute vlue is the first token after the colon (any thing after 
  // it will be ignored ;
  // For example :
  // if the configuration file has the following entry:
  //
  // NO.   ITERATIONS   MODEL 2 :	10
  //
  // then the attribute is "NO. ITERATIONS MODEL 2" , and the attribute value
  // is "10"  (these do not include the quotation marks).

{

  string line, word, attrib, attribval ;
  ifstream Config_File(fname);
  if(!Config_File){
    cerr << "ERROR:  Cannot open configuration file " << fname << "!\n" ;
    exit(1);
  }

  cout << "The following options are from the config file and will be overwritten by any command line options.\n";
  
  while(getline(Config_File, line)){

    istringstream buffer(line);
    word = attrib = attribval = "" ;
    buffer >> word  ;
    if (word != "//"){ // if line does not start with "//" (i.e. not a comment)
      attrib = word ;
      while((buffer >> word) && (word != ":")){
	attrib += " " + word ;
      }      
      if(!(buffer >> attribval))
	{
	  istringstream buffer2(line);
	  buffer2>>attrib;
	  buffer2>>attribval;
	}

      // This# is where (1) the configuration file is defined and
      //               (2) parsing of its attributes occurs.
      
      if(attrib == "t FILE"){
	t_Filename = attribval;
	cout << "\tt file:  " << t_Filename << '\n';
      }
      else if(attrib ==  "a FILE"){
	a_Filename = attribval;
	cout << "\ta file:  " << a_Filename << '\n';
      }
      else if(attrib == "d FILE"){
	d_Filename = attribval;
	cout << "\td file:  " << d_Filename << '\n';
      }
      else if(attrib == "n FILE"){
	n_Filename = attribval;
	cout << "\tn file:  " << n_Filename << '\n';
      }
      else if(attrib == "p0 FILE"){
	p0_Filename = attribval;
	cout << "\tp0 file:  " << p0_Filename << '\n';
      }
      else if ( line == ""){}
      else if(  !makeSetCommand(attrib,attribval,getGlobalParSet(),2) )
	cerr << "ERROR: Unrecognized attribute :" << attrib << '\n';
    }
  }
}


void parseArguments(int argc, char *argv[])
{
  int arg = 1;

  if(!strcmp(argv[1], "--h") || !strcmp(argv[1], "--help")){
    printHelp();
    exit(0);
  }
  if( argv[1][0]=='-' )
    arg=0;
  else
    parseConfigFile(argv[1]);
  while(++arg<argc){
    if( strlen(argv[arg])>2 && argv[arg][0]=='-' && argv[arg][1]=='-' )
      {
	if( !makeSetCommand(argv[arg]+1,"1",getGlobalParSet(),2))
	  cerr << "WARNING: ignoring unrecognized option:  "<< argv[arg] << '\n' ;  
      }
    else if( arg+1<argc && !makeSetCommand(argv[arg],argv[arg+1],getGlobalParSet(),2))
      cerr << "WARNING: ignoring unrecognized option:  "<< argv[arg] << '\n' ;  
    else
      {
	arg++;
      }
  }
  if( OPath.length() )
    OPath+="/";
  Prefix = (OPath + Prefix);
  LogFilename = (OPath + LogFilename);
  printGIZAPars(cout);
}

