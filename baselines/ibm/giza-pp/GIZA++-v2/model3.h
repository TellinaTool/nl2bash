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
#ifndef _model3_h
#define _model3_h 1
#include <cassert>
#include <iostream>
#include <algorithm>
#include <functional>
#include <map>
#include <set>
#include "Vector.h"
#include <utility>


#include <ctime>
#include <fstream>
#include <cmath>
#include "MoveSwapMatrix.h"
#include "TTables.h"
#include "ATables.h"
#include "NTables.h"
#include "getSentence.h"
#include "defs.h"
#include "model2.h"
#include "Perplexity.h"
#include "transpair_model3.h"
#include "transpair_modelhmm.h"
#include "alignment.h"
#include "vocab.h"
#include "D4Tables.h"
#include "AlignTables.h"

class model3 : public model2
{
public:
  amodel<PROB>   dTable;
  amodel<COUNT>  dCountTable;

  PROB p0,p1;
  double p0_count, p1_count ;

  nmodel<PROB>  nTable;
  nmodel<COUNT> nCountTable;
  hmm*h;

public:
  void setHMM(hmm*_h){h=_h;}
  model3(model2& m2);
  ~model3();
  // methods
  void transfer(sentenceHandler&, bool, Perplexity&, Perplexity&,bool updateT=1);
  void transferSimple(sentenceHandler&, bool, Perplexity&, Perplexity&,bool updateT=1);
  void load_tables(const char *nfile, const char *dfile, const char *p0file);
  
  void em(int, sentenceHandler&);
  int viterbi(int, int, int,int);
    
private:
  LogProb prob_of_special(Vector<WordIndex>&, 
			  Vector<WordIndex>&, 
			  tmodel<COUNT, PROB>&, 
			  Vector<WordIndex>&, 
			  Vector<WordIndex>&);

  LogProb prob_of_target_and_alignment_given_source(Vector<WordIndex>&, 
						  Vector<WordIndex>&, 
						  tmodel<COUNT, PROB>&, 
						  Vector<WordIndex>&, 
						  Vector<WordIndex>&);
  LogProb prob_of_target_given_source(tmodel<COUNT, PROB>&, 
				    Vector<WordIndex>&, 
				    Vector<WordIndex>&);

  LogProb scoreOfMove(Vector<WordIndex>&, Vector<WordIndex>&, 
		    Vector<WordIndex>&, Vector<WordIndex>&, 
		    tmodel<COUNT, PROB>&, WordIndex, WordIndex);

  LogProb scoreOfSwap(Vector<WordIndex>&, Vector<WordIndex>&, 
		      Vector<WordIndex>&, tmodel<COUNT, PROB>&, int, int);
  
  void hillClimb(Vector<WordIndex>&, Vector<WordIndex>&, 
		 Vector<WordIndex>&, Vector<WordIndex>&, 
		 LogProb&, tmodel<COUNT, PROB>&, int, int);

  void findBestAlignment(Vector<WordIndex>&, Vector<WordIndex>&, 
			 Vector<WordIndex>&, Vector<WordIndex>&, 
			 LogProb&,int , int);


  void findAlignmentsNeighborhood( Vector<WordIndex>&, 
				   Vector<WordIndex>&, 
				   LogProb&align_total_count, 
				   alignmodel&neighborhood, 
				   int, int);
  void collectCountsOverAlignement(const Vector<WordIndex>& es, 
				   const Vector<WordIndex>& fs, 
				   const Vector<WordIndex>&, 
				   LogProb , float count);
  LogProb viterbi_model2(const transpair_model3&ef,   alignment&output, int pair_no,int i_peg = -1 , int j_peg = -1 )const;
  LogProb _viterbi_model2(const transpair_model2&ef,   alignment&output, int i_peg = -1 , int j_peg = -1 )const;
  LogProb viterbi_model2(const transpair_modelhmm&ef, alignment&output, int pair_no,int i_peg = -1 , int j_peg = -1 )const;

 private:
  void estimate_t_a_d(sentenceHandler& sHandler1, Perplexity& perp1, Perplexity& perp2,bool simple, bool dump_files,bool updateT);
  void viterbi_loop(Perplexity&, Perplexity&, sentenceHandler&, bool, const char*,bool,string model);

  template<class MODEL_TYPE, class A,class B>
  void viterbi_loop_with_tricks(Perplexity&, Perplexity&, sentenceHandler&, 
						      bool, const char*,  bool, string model, bool final,A*d4m,B*d5m);

};

#endif
