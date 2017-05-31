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
#ifndef _model2_h
#define _model2_h 1

#include <cassert>
 
#include <iostream>
#include <algorithm>
#include <functional>
#include <map>
#include <set>
#include "Vector.h"
#include <utility>

#include <fstream>
#include <cmath>
#include <ctime>

#include "TTables.h"
#include "ATables.h" 
#include "getSentence.h"
#include "defs.h"
#include "model1.h"
#include "Perplexity.h"
#include "vocab.h"

class model2 : public model1
{
 public:
  amodel<PROB>&aTable;
  amodel<COUNT>&aCountTable;
 public:
  model2(model1& m1,amodel<PROB>&,amodel<COUNT>&);
  void initialize_table_uniformly(sentenceHandler&);
  int em_with_tricks(int);
  void load_table(const char* aname);
  inline amodel<PROB>& getATable(void) {return aTable;};
  inline amodel<COUNT>& getACountTable(void) {return aCountTable;};
  void em_loop(Perplexity& perp,sentenceHandler& sHandler1, bool dump_files,const char* alignfile, Perplexity&, bool test);
  friend class model3;
};

#endif
