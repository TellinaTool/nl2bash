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
#ifndef _model1_h
#define _model1_h 1

#include <cassert>
 
#include <iostream>
#include <sstream>
#include <algorithm>
#include <functional>
#include <map>
#include <set>
#include <utility>

#include <ctime>
#include <fstream>
#include <cmath>
#include <cstdio>

#include "Vector.h"
#include "vocab.h"
#include "TTables.h"
#include "getSentence.h"
#include "Perplexity.h"
#include "vocab.h"
#include "Dictionary.h"

extern int NumberOfVALIalignments;

class report_info{
 protected:
  Perplexity& perp;
  sentenceHandler& sHandler1;
  Perplexity* testPerp;
  sentenceHandler* testHandler;
  Perplexity& trainViterbiPerp; 
  Perplexity* testViterbiPerp;
  report_info(Perplexity& _perp,
	      sentenceHandler& _sHandler1,
	      Perplexity* _testPerp,
	      sentenceHandler* _testHandler,
	      Perplexity& _trainViterbiPerp,
	      Perplexity* _testViterbiPerp)
    : perp(_perp),sHandler1(_sHandler1),testPerp(_testPerp),testHandler(_testHandler),trainViterbiPerp(_trainViterbiPerp),testViterbiPerp(_testViterbiPerp)
    {}
};

class model1 : public report_info{
public:
  string efFilename;
  vcbList&  Elist ;
  vcbList&  Flist ;
  double eTotalWCount ; // size of source copus in number of words
  double fTotalWCount ; // size of target corpus in number of words 
  int noEnglishWords;
  int noFrenchWords;
  tmodel<COUNT, PROB>&tTable;
  Vector<WordEntry>& evlist ;
  Vector<WordEntry>& fvlist ;
public:
  int ALmissing,ALtoomuch,ALeventsMissing,ALeventsToomuch;
  int ALmissingVALI,ALtoomuchVALI,ALeventsMissingVALI,ALeventsToomuchVALI;
  int ALmissingTEST,ALtoomuchTEST,ALeventsMissingTEST,ALeventsToomuchTEST;
  model1 (const char* efname, vcbList& evcblist, vcbList& fvcblist,tmodel<COUNT, PROB>&_tTable,Perplexity& _perp,
	      sentenceHandler& _sHandler1,
	      Perplexity* _testPerp,
	      sentenceHandler* _testHandler,
	      Perplexity& _trainViterbiPerp,
	      Perplexity* _testViterbiPerp);
  void initialize_table_uniformly(sentenceHandler& sHandler1);
  int em_with_tricks(int noIterations, 
		      bool seedModel1, Dictionary& dictionary, bool useDict);
  void load_table(const char* tname);
  void readVocabFile(const char* fname, Vector<WordEntry>& vlist, int& vsize, 
		     int& total);
  inline Vector<WordEntry>& getEnglishVocabList(void)const {return Elist.getVocabList();};
  inline Vector<WordEntry>& getFrenchVocabList(void)const  {return Flist.getVocabList();};
  inline double getETotalWCount(void) const {return eTotalWCount;};
  inline double getFTotalWCount(void) const {return fTotalWCount;};
  inline int getNoEnglishWords(void) const  {return noEnglishWords;};
  inline int getNoFrenchWords(void)  const {return noFrenchWords;};
  inline tmodel<COUNT, PROB>& getTTable(void) {return tTable;};
  inline string& getEFFilename(void) {return efFilename;};
 private:
  void em_loop(int it,Perplexity& perp, sentenceHandler& sHandler1, bool seedModel1, bool , const char*, Dictionary& dictionary, bool useDict, 
	       Perplexity& viterbiperp, bool=false);
  friend class model2;
  friend class hmm;
 public:
  void addAL(const Vector<WordIndex>& viterbi_alignment,int pair_no,int l)
    {
      if( pair_no<=int(ReferenceAlignment.size()) )
	{
	  //cerr << "AL: " << viterbi_alignment << " " << pair_no << endl;
	  ErrorsInAlignment(ReferenceAlignment[pair_no-1],viterbi_alignment,l,ALmissing,ALtoomuch,ALeventsMissing,ALeventsToomuch,pair_no);
	  if( pair_no<=NumberOfVALIalignments )
	    ErrorsInAlignment(ReferenceAlignment[pair_no-1],viterbi_alignment,l,ALmissingVALI,ALtoomuchVALI,ALeventsMissingVALI,ALeventsToomuchVALI,pair_no);
	  if( pair_no>NumberOfVALIalignments )
	    ErrorsInAlignment(ReferenceAlignment[pair_no-1],viterbi_alignment,l,ALmissingTEST,ALtoomuchTEST,ALeventsMissingTEST,ALeventsToomuchTEST,pair_no);
	}
    }
  void initAL()
    {ALmissingVALI=ALtoomuchVALI=ALeventsMissingVALI=ALeventsToomuchVALI=ALmissingTEST=ALtoomuchTEST=ALeventsMissingTEST=ALeventsToomuchTEST=ALmissing=ALtoomuch=ALeventsMissing=ALeventsToomuch=0;}
  double errorsAL()const
    {
      if( ALeventsMissingVALI+ALeventsToomuchVALI )
	return (ALmissingVALI+ALtoomuchVALI)/double(ALeventsMissingVALI+ALeventsToomuchVALI);
      else
	return 0.0;
    }
  void errorReportAL(ostream&out,string m)const
    {
      if( ALeventsMissing+ALeventsToomuch )
	out << "alignmentErrors (" << m << "): " 
	    << 100.0*(ALmissing+ALtoomuch)/double(ALeventsMissing+ALeventsToomuch) 
	    << " recall: " << 100.0*(1.0-ALmissing/double(ALeventsMissing))
	    << " precision: " << 100.0*(1.0-ALtoomuch/double(ALeventsToomuch))
	    << " (missing:" << ALmissing << "/" << ALeventsMissing << " " << ALtoomuch 
	    << " " << ALeventsToomuch << ")\n";
      if( ALeventsMissingVALI+ALeventsToomuchVALI )
	out << "alignmentErrors VALI (" << m << "): " 
	    << 100.0*(ALmissingVALI+ALtoomuchVALI)/double(ALeventsMissingVALI+ALeventsToomuchVALI) 
	    << " recall: " << 100.0*(1.0-ALmissingVALI/double(ALeventsMissingVALI))
	    << " precision: " << 100.0*(1.0-ALtoomuchVALI/double(ALeventsToomuchVALI))
	    << " (missing:" << ALmissingVALI << "/" << ALeventsMissingVALI << " " << ALtoomuchVALI 
	    << " " << ALeventsToomuchVALI << ")\n";
      if( ALeventsMissingTEST+ALeventsToomuchTEST )
	out << "alignmentErrors TEST(" << m << "): " 
	    << 100.0*(ALmissingTEST+ALtoomuchTEST)/double(ALeventsMissingTEST+ALeventsToomuchTEST) 
	    << " recall: " << 100.0*(1.0-ALmissingTEST/double(ALeventsMissingTEST)) 
	    << " precision: " << 100.0*(1.0-ALtoomuchTEST/double(ALeventsToomuchTEST))
	    << " (missing:" << ALmissingTEST << "/" << ALeventsMissingTEST << " " << ALtoomuchTEST 
	    << " " << ALeventsToomuchTEST << ")\n";
      
    }
};

#endif
