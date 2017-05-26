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
#include "NTables.h"
#include <iostream>
#include "defs.h"
#include <fstream>
#include "Parameter.h"

GLOBAL_PARAMETER(double,NTablesFactorGraphemes,"nSmooth","smoothing for fertility parameters (good value: 64): weight for wordlength-dependent fertility parameters",PARLEV_SMOOTH,64.0);
GLOBAL_PARAMETER(double,NTablesFactorGeneral,"nSmoothGeneral","smoothing for fertility parameters (default: 0): weight for word-independent fertility parameters",PARLEV_SMOOTH,0.0);

template <class VALTYPE>
void nmodel<VALTYPE>::printNTable(int noEW, const char* filename, 
				  const Vector<WordEntry>& evlist, 
				  bool actual) const
     // prints the fertility table but with actual sourcce words (not their id)
{
  cerr << "Dumping nTable to: " << filename <<  '\n';  
  ofstream of(filename);
  VALTYPE p ;
  WordIndex k, i ;
  for(i=1; int(i) < noEW; i++){
    if (evlist[i].freq > 0){
      if (actual)
	of << evlist[i].word << ' ' ;
      else 
	of << i << ' ' ;
      for( k=0; k < MAX_FERTILITY; k++){
	p = getValue(i, k);
	if (p <= PROB_SMOOTH) 
	  p = 0;
	of << p << ' ';      
      } 
      of << '\n';
    }
  }
}

template <class VALTYPE>
void nmodel<VALTYPE>::readNTable(const char *filename){
  /* This function reads the n table from a file.
     Each line is of the format:  source_word_id p0 p1 p2 ... pn
     This is the inverse operation of the printTable function.
     NAS, 7/11/99
  */
  ifstream inf(filename);
  cerr << "Reading fertility table from " << filename << "\n";
  if(!inf){
    cerr << "\nERROR: Cannot open " << filename <<"\n";
    return;
  }

  VALTYPE prob;
  WordIndex tok, i;
  int nFert=0;
  while(!inf.eof()){
    nFert++;
    inf >> ws >> tok;
    if (tok > MAX_VOCAB_SIZE){
      cerr << "NTables:readNTable(): unrecognized token id: " << tok
    <<'\n';
    exit(-1);
  }
    for(i = 0; i < MAX_FERTILITY; i++){
      inf >> ws >> prob;
      getRef(tok, i)=prob;
    }
  }
  cerr << "Read " << nFert << " entries in fertility table.\n";
  inf.close();
}

template class nmodel<COUNT>;
//template class nmodel<PROB>;
