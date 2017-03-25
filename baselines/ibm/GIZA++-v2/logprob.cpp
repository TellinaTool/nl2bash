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

//  Routines to perform integer exponential arithmetic.
//  A number x is represented as n, where x = b**n.
//  It is assumed that b > 1, something like b = 1.001;

#include "logprob.h"
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <string>
double *LogProb::ntof  = NULL; // Tables will be initialized
int   *LogProb::addtbl = NULL; // in Initialize function.
int   *LogProb::subtbl = NULL; //

const int    LogProb::max_2byte_integer =  32767;
const int    LogProb::min_2byte_integer = -32768;
const double LogProb::b      = 1.001;   // a logarithm basis
const double LogProb::logb2  = log(b);
//const int    LogProb::nmax   = round(78.0E0 * log(1.0E1) / logb2);
const int    LogProb::nmax   = round(300.0E0 * log(1.0E1) / logb2);
const int    LogProb::nmin   = -nmax;
const int    LogProb::tblbnd = round(log((b-1.0E0)/2.0E0)/logb2);
const int    LogProb::zeron  = round(pow(-2, 23));
const int    LogProb::onen   = 0;
const int    LogProb::infn   = onen - zeron;

const int LogProb::initialized = LogProb::Initialize();
const LogProb LogProb::zero(0);
const LogProb LogProb::one(1);
const LogProb LogProb::minus2(1e-2);
const LogProb LogProb::minus4(1e-4);
const LogProb LogProb::minus6(1e-6);
const LogProb LogProb::minus8(1e-8);
const LogProb LogProb::minus10(1e-10);
const LogProb LogProb::minus12(1e-12);
const LogProb LogProb::minus14(1e-14);
const LogProb LogProb::minus16(1e-16);

// static table initialization function
int LogProb::Initialize()
{
  int nbytes = sizeof(double)*(nmax-nmin+1) + sizeof(int)*(0-tblbnd+1);
  std::cerr << nbytes << " bytes used for LogProb tables (C++ version)\n";
  ntof   = new double[nmax-nmin+1];
  addtbl = new int[-tblbnd+1];
  subtbl = new int[-tblbnd+1];

  //  char filename[257];
  //  string filename ;
  //  ifstream ifs;
  //  ifs.open(filename.c_str());
  //  if (!ifs)
  //    {
  int i;
  std::cerr << "Building integer logs conversion tables\n";
  ntof[0] = 0 ;
  
  for (i=nmin+1; i<=nmax; ++i) 
    {
      double x = i;
      ntof[i-nmin] = exp(x*logb2);
      
    }
  for (i=tblbnd; i<=0; ++i) 
    {
      double x = 1.0 + pow(b, i);
      addtbl[i-tblbnd] = round(log(x)/logb2);
    }
  double sqrtb = exp(0.5*logb2);
  for (i=0; i<=-tblbnd; ++i) 
    {
      double x = sqrtb * pow(b, i) - 1.0;
      subtbl[i] = round(log(x)/logb2);
    }
  //      if (toolsRoot)
  //	{
  //      ofstream ofs(filename.c_str());
  //      if (!ofs)
  //	cerr << "Could not write LogProb data to " << filename << endl;
  //      else
  //	{
  //	  ofs.write((const char *)ntof, sizeof(double) * (nmax-nmin+1));
  //	  ofs.write((const char *)addtbl, sizeof(int) * (-tblbnd+1));
  //	  ofs.write((const char *)subtbl, sizeof(int) * (-tblbnd+1));
  //	}
  //    }
  //    }
  //  else
  //    {
  //      ifs.read((char *)ntof,   sizeof(double) * (nmax - nmin + 1));
  //      ifs.read((char *)addtbl, sizeof(int) * (-tblbnd+1));
  //      ifs.read((char *)subtbl, sizeof(int) * (-tblbnd+1));
  //    }
  return 1;
}

void LogProb::FreeTables()
{
   delete [] addtbl;
   delete [] subtbl;
   delete [] ntof;
}

//---------------------------------------------------------------------------
//            Aritmetic operators
//---------------------------------------------------------------------------


// Subtract two logarithm numbers. Use the following method:
// b**n - b**m = b**m( b**(n-m) - 1 ), assuming n >= m. 
LogProb& LogProb::operator-=(const LogProb &subs) 
{
  if (subs.logr == zeron)
    return *this;
  int a = logr - subs.logr;
  if (a <= 0)
    {
      if (a < 0)
	{
	  std::cerr << "WARNING(logprob): Invalid arguments to nsub" <<(*this)<< " " << subs << std::endl;
	  //abort();
	}
      logr = zeron;
      return *this;
    }
  if (a > -tblbnd)
    return *this;
  logr = subs.logr + subtbl[a];
  return *this;
}


