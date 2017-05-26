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
#include "model2.h"
#include "Globals.h"
#include "utility.h"
#include "Parameter.h"
#include "defs.h"

extern short NoEmptyWord;


GLOBAL_PARAMETER2(int,Model2_Dump_Freq,"MODEL 2 DUMP FREQUENCY","t2","dump frequency of Model 2",PARLEV_OUTPUT,0);

model2::model2(model1& m,amodel<PROB>&_aTable,amodel<COUNT>&_aCountTable): 
  model1(m),aTable(_aTable),aCountTable(_aCountTable)
{  }

void model2::initialize_table_uniformly(sentenceHandler& sHandler1){
  // initialize the aTable uniformly (run this before running em_with_tricks)
  int n=0;
  sentPair sent ;
  sHandler1.rewind();
   while(sHandler1.getNextSentence(sent)){
    Vector<WordIndex>& es = sent.eSent;
    Vector<WordIndex>& fs = sent.fSent;
    WordIndex l = es.size() - 1;
    WordIndex m = fs.size() - 1;
    n++;
    if(1<=m&&aTable.getValue(l,m,l,m)<=PROB_SMOOTH)
      {
	PROB uniform_val = 1.0 / (l+1) ;
	for(WordIndex j=1; j <= m; j++)
	  for(WordIndex i=0; i <= l; i++)
	    aTable.setValue(i,j, l, m, uniform_val);
      }
  }
}

int model2::em_with_tricks(int noIterations)
{
  double minErrors=1.0;int minIter=0;
  string modelName="Model2",shortModelName="2";
  time_t it_st, st, it_fn, fn;
  string tfile, afile, number, alignfile, test_alignfile;
  int pair_no = 0;
  bool dump_files = false ;
  ofstream of2 ;
  st = time(NULL) ;
  sHandler1.rewind();
  cout << "\n==========================================================\n";
  cout << modelName << " Training Started at: " << ctime(&st) << " iter: " << noIterations << "\n";
  for(int it=1; it <= noIterations ; it++){
    pair_no = 0;
    it_st = time(NULL) ;
    cout << endl << "-----------\n" << modelName << ": Iteration " << it << '\n';
    dump_files = (Model2_Dump_Freq != 0) && ((it % Model2_Dump_Freq) == 0) && !NODUMPS;
    number = "";
    int n = it;
    do{
      number.insert((size_t)0, 1, (char)(n % 10 + '0'));
    } while((n /= 10) > 0);
    tfile = Prefix + ".t" + shortModelName + "." + number ;
    afile = Prefix + ".a" + shortModelName + "." + number ;
    alignfile = Prefix + ".A" + shortModelName + "." + number ;
    test_alignfile = Prefix + ".tst.A" + shortModelName + "." + number ;
    aCountTable.clear();
    initAL();
    em_loop(perp, sHandler1, dump_files, alignfile.c_str(), trainViterbiPerp, false);
    if( errorsAL()<minErrors )
      {
	minErrors=errorsAL();
        minIter=it;
      }
    if (testPerp && testHandler)
      em_loop(*testPerp, *testHandler, dump_files, test_alignfile.c_str(), *testViterbiPerp, true); 
    if (dump_files&&OutputInAachenFormat==1)
      tTable.printCountTable(tfile.c_str(),Elist.getVocabList(),Flist.getVocabList(),1);
    tTable.normalizeTable(Elist, Flist);
    aCountTable.normalize(aTable);
    cout << modelName << ": ("<<it<<") TRAIN CROSS-ENTROPY " << perp.cross_entropy()
	 << " PERPLEXITY " << perp.perplexity() << '\n';
     if (testPerp && testHandler)
       cout << modelName << ": ("<<it<<") TEST CROSS-ENTROPY " << (*testPerp).cross_entropy()
	    << " PERPLEXITY " << (*testPerp).perplexity() 
	    << '\n';
     cout << modelName << ": ("<<it<<") VITERBI TRAIN CROSS-ENTROPY " << trainViterbiPerp.cross_entropy()
	 << " PERPLEXITY " << trainViterbiPerp.perplexity() << '\n';
    if (testPerp && testHandler)
       cout << modelName << ": ("<<it<<") VITERBI TEST CROSS-ENTROPY " << testViterbiPerp->cross_entropy()
	    << " PERPLEXITY " << testViterbiPerp->perplexity() 
	    << '\n';
    if (dump_files)
      {
	if(OutputInAachenFormat==0)
	  tTable.printProbTable(tfile.c_str(),Elist.getVocabList(),Flist.getVocabList(),OutputInAachenFormat);
	aCountTable.printTable(afile.c_str());
      }
    it_fn = time(NULL) ;
    cout << modelName << " Iteration: " << it<< " took: " << difftime(it_fn, it_st) << " seconds\n";
  } // end of iterations 
  aCountTable.clear();
  fn = time(NULL) ;
  cout << endl << "Entire " << modelName << " Training took: " << difftime(fn, st) << " seconds\n";
  //  cout << "tTable contains " << tTable.getHash().bucket_count() 
  //     << " buckets and  " << tTable.getHash().size() << " entries." ;
  cout << "==========================================================\n";
  return minIter;
}

void model2::load_table(const char* aname){
  /* This function loads the a table from the given file; use it
     when you want to load results from previous a training without
     doing any new training.
     NAS, 7/11/99
  */
  cout << "Model2: loading a table \n";
  aTable.readTable(aname);
}


void model2::em_loop(Perplexity& perp, sentenceHandler& sHandler1, 
		     bool dump_alignment, const char* alignfile, Perplexity& viterbi_perp, 
		     bool test)
{
  massert( aTable.is_distortion==0 );
  massert( aCountTable.is_distortion==0 );
  WordIndex i, j, l, m ;
  double cross_entropy;
  int pair_no=0 ;
  perp.clear();
  viterbi_perp.clear();
  ofstream of2;
  // for each sentence pair in the corpus
  if (dump_alignment||FEWDUMPS )
    of2.open(alignfile);
  sentPair sent ;

  vector<double> ferts(evlist.size());
  
  sHandler1.rewind();
  while(sHandler1.getNextSentence(sent)){
    Vector<WordIndex>& es = sent.eSent;
    Vector<WordIndex>& fs = sent.fSent;
    const float so  = sent.getCount();
    l = es.size() - 1;
    m = fs.size() - 1;
    cross_entropy = log(1.0);
    Vector<WordIndex> viterbi_alignment(fs.size());
    double viterbi_score = 1;
    for(j=1; j <= m; j++){
      Vector<LpPair<COUNT,PROB> *> sPtrCache(es.size(),0); // cache pointers to table 
      // entries  that map fs to all possible ei in this sentence.
      PROB denom = 0.0;
      PROB e = 0.0, word_best_score = 0;
      WordIndex best_i = 0 ; // i for which fj is best maped to ei
      for(i=0; i <= l; i++){
	sPtrCache[i] = tTable.getPtr(es[i], fs[j]) ;
	if (sPtrCache[i] != 0 &&(*(sPtrCache[i])).prob > PROB_SMOOTH ) 
	  e = (*(sPtrCache[i])).prob * aTable.getValue(i,j, l, m) ;
	else e = PROB_SMOOTH * aTable.getValue(i,j, l, m);
	denom += e ;
	if (e > word_best_score){
	  word_best_score = e ;
	  best_i = i ;
	}
      }
      viterbi_alignment[j] = best_i ;
      viterbi_score *= word_best_score; ///denom ;
      cross_entropy += log(denom) ;
      if (denom == 0){
	if (test)
	  cerr << "WARNING: denom is zero (TEST)\n";
	else 
	  cerr << "WARNING: denom is zero (TRAIN)\n";
      }      
      if (!test){
	if(denom > 0){	  
	  COUNT val = COUNT(so) / (COUNT) double(denom) ;
	  for( i=0; i <= l; i++){
	    PROB e(0.0);
	    if (sPtrCache[i] != 0 &&  (*(sPtrCache[i])).prob > PROB_SMOOTH)
	      e = (*(sPtrCache[i])).prob ;
	    else e = PROB_SMOOTH  ;
	    e *= aTable.getValue(i,j, l, m);
	    COUNT temp = COUNT(e) * val ;
	    if( NoEmptyWord==0 || i!=0 )
	      if (sPtrCache[i] != 0) 
		(*(sPtrCache[i])).count += temp ;
	      else 	      
		tTable.incCount(es[i], fs[j], temp);	    
	    aCountTable.getRef(i,j, l, m)+= temp ; 
	  } /* end of for i */
	} // end of if (denom > 0)
      }// if (!test)
    } // end of for (j) ;
    sHandler1.setProbOfSentence(sent,cross_entropy);
    perp.addFactor(cross_entropy, so, l, m,1);
    viterbi_perp.addFactor(log(viterbi_score), so, l, m,1);
    if (dump_alignment||(FEWDUMPS&&sent.sentenceNo<1000) )
      printAlignToFile(es, fs, Elist.getVocabList(), Flist.getVocabList(), of2, viterbi_alignment, sent.sentenceNo, viterbi_score);
    addAL(viterbi_alignment,sent.sentenceNo,l);
    pair_no++;
  } /* of while */
  sHandler1.rewind();
  perp.record("Model2");
  viterbi_perp.record("Model2");
  errorReportAL(cout,"IBM-2");
}





