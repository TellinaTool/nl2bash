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
#include "model3.h"
#include "utility.h"
#include "Globals.h"

#define _MAX_FERTILITY 10

double get_sum_of_partitions(int n, int source_pos, double alpha[_MAX_FERTILITY][MAX_SENTENCE_LENGTH_ALLOWED])
{
  int done, init ;
  double sum = 0, prod ;
  int s, w, u, v;
  WordIndex k, k1, i ;
  WordIndex num_parts = 0  ;
  int total_partitions_considered = 0;

  int part[_MAX_FERTILITY], mult[_MAX_FERTILITY];

  done = false ;
  init = true ;    
  for (i = 0 ; i < _MAX_FERTILITY ; i++){
    part[i] = mult[i] = 0 ;
  }
  
  //printf("Entering get sum of partitions\n");
  while(! done){
    total_partitions_considered++;
    if (init){
      part[1] = n ;
      mult[1] = 1 ;
      num_parts = 1  ;  
      init = false ;
    }
    else {
      if ((part[num_parts] > 1) || (num_parts > 1)){
	if (part[num_parts] == 1){
	  s = part[num_parts-1] + mult[num_parts];
	  k = num_parts - 1;
	}
	else {
	  s = part[num_parts];
	  k = num_parts ;
	}
	w = part[k] - 1 ;
	u = s / w ;
	v = s % w ;
	mult[k] -= 1 ;
	if (mult[k] == 0)
	  k1 = k ;
	else k1 = k + 1 ;
	mult[k1] = u ;
	part[k1] = w ;
	if (v == 0){
	  num_parts = k1 ;
	}
	else {
	  mult[k1+1] = 1 ;
	  part[k1+1] = v ;
	  num_parts = k1 + 1;
	}
      } /* of if num_parts > 1 || part[num_parts] > 1 */    
      else {
	done = true ;
      }
    }
    /* of else of if(init) */
    if (!done){
      prod = 1.0 ;
      if (n != 0)
	for (i = 1 ; i <= num_parts ; i++){
	  prod *= pow(alpha[part[i]][source_pos], mult[i]) / factorial(mult[i]) ;
	}
      sum += prod ;
    }
  } /* of while */  
  if (sum < 0) sum = 0 ;
  return(sum) ;
}

void model3::estimate_t_a_d(sentenceHandler& sHandler1, Perplexity& perp, Perplexity& trainVPerp, 
			    bool simple, bool dump_files,bool updateT) 
{
  string tfile, nfile, dfile, p0file, afile, alignfile;
  WordIndex i, j, l, m, max_fertility_here, k ;
  PROB val, temp_mult[MAX_SENTENCE_LENGTH_ALLOWED][MAX_SENTENCE_LENGTH_ALLOWED];
  double cross_entropy;
  double beta, sum, 
      alpha[_MAX_FERTILITY][MAX_SENTENCE_LENGTH_ALLOWED];
  double total, temp, r ;

  dCountTable.clear();
  aCountTable.clear();
  initAL();
  nCountTable.clear() ;
  if (simple)
    nTable.clear();
  perp.clear() ;
  trainVPerp.clear() ;
  ofstream of2;
  if (dump_files){
    alignfile = Prefix +".A2to3";
    of2.open(alignfile.c_str());
  }
  if (simple) cerr <<"Using simple estimation for fertilties\n";
  sHandler1.rewind() ;
  sentPair sent ;
  while(sHandler1.getNextSentence(sent)){
    Vector<WordIndex>& es = sent.eSent;
    Vector<WordIndex>& fs = sent.fSent;
    const float count  = sent.getCount();
    Vector<WordIndex> viterbi_alignment(fs.size());
    l = es.size() - 1;
    m = fs.size() - 1;
    cross_entropy = log(1.0); 
    double viterbi_score = 1 ;
    PROB word_best_score ;  // score for the best mapping of fj
    for(j = 1 ; j <= m ; j++){
      word_best_score = 0 ;  // score for the best mapping of fj	
      Vector<LpPair<COUNT,PROB> *> sPtrCache(es.size(),0);
      total = 0 ;
      WordIndex best_i = 0 ;
      for(i = 0; i <= l ; i++){
	sPtrCache[i] = tTable.getPtr(es[i], fs[j]) ;
	if (sPtrCache[i] != 0 &&  (*(sPtrCache[i])).prob > PROB_SMOOTH) // if valid pointer
	  temp_mult[i][j]= (*(sPtrCache[i])).prob * aTable.getValue(i, j, l, m) ;
	else 
	  temp_mult[i][j] = PROB_SMOOTH *  aTable.getValue(i, j, l, m) ;
	total += temp_mult[i][j] ;
	if (temp_mult[i][j] > word_best_score){
	    word_best_score = temp_mult[i][j] ;
	    best_i = i ;
	  }
      } // end of for (i) 
      viterbi_alignment[j] = best_i ;
      viterbi_score *= word_best_score ; /// total ;
      cross_entropy += log(total) ; 
      if (total == 0){
	  cerr << "WARNING: total is zero (TRAIN)\n";
	  viterbi_score = 0 ;
      }
      if (total > 0){
	for(i = 0; i <= l ; i++){
	  temp_mult[i][j] /= total ;
	  if (temp_mult[i][j] == 1) // smooth to prevent underflow
	    temp_mult[i][j] = 0.99 ;
	  else  if (temp_mult[i][j] == 0)
	    temp_mult[i][j] = PROB_SMOOTH ;
	 val = temp_mult[i][j] * PROB(count) ;
	  if ( val > PROB_SMOOTH) {
	    if( updateT )
	      {
		if (sPtrCache[i] != 0) 
		  (*(sPtrCache[i])).count += val ;
		else
		  tTable.incCount(es[i], fs[j], val);
	      }
	    aCountTable.getRef(i, j, l, m)+=val;
	    if (0 != i)
	      dCountTable.getRef(j, i, l, m)+=val;
	  }
	} // for (i = ..)
      } // for (if total ...)
    } // end of for (j  ...)
    if (dump_files)
      printAlignToFile(es, fs, Elist.getVocabList(), Flist.getVocabList(), of2, viterbi_alignment, sent.sentenceNo, viterbi_score);
    addAL(viterbi_alignment,sent.sentenceNo,l);
    if (!simple){
      max_fertility_here = min(WordIndex(m+1), MAX_FERTILITY);
      for (i = 1; i <= l ; i++) { 
	for ( k = 1; k < max_fertility_here; k++){
	  beta = 0 ;
	  alpha[k][i] = 0 ;
	  for (j = 1 ; j <= m ; j++){
	    temp =  temp_mult[i][j];	    	   
	    if (temp > 0.95) temp = 0.95; // smooth to prevent under/over flow
	    else if (temp < 0.05) temp = 0.05;
	    beta += pow(temp/(1.0-temp), (double) k);
	  }
	alpha[k][i] = beta * pow((double) -1, (double) (k+1)) / (double) k ;
	}
      }
      for (i = 1; i <= l ; i++){ 
	r = 1;
	for (j = 1 ; j <= m ; j++)
	  r *= (1 - temp_mult[i][j]); 
	for (k = 0  ; k <  max_fertility_here ; k++){
	  sum = get_sum_of_partitions(k, i, alpha);
	  temp = r * sum * count;
	  nCountTable.getRef(es[i], k)+=temp;	  
	} // end of for (k ..)
      } // end of for (i == ..)
    } // end of  if (!simple)
    perp.addFactor(cross_entropy, count, l, m,1);
    trainVPerp.addFactor(log(viterbi_score), count, l, m,1);
  } // end of while 
  sHandler1.rewind();
  cerr << "Normalizing t, a, d, n count tables now ... " ;
  if( dump_files && OutputInAachenFormat==1 )
    {
      tfile = Prefix + ".t2to3" ;
      tTable.printCountTable(tfile.c_str(),Elist.getVocabList(),Flist.getVocabList(),1);
    }
  if( updateT )
    tTable.normalizeTable(Elist, Flist);
  aCountTable.normalize(aTable);
  dCountTable.normalize(dTable);
  if (!simple)
    nCountTable.normalize(nTable,&Elist.getVocabList());
  else {
    for (i = 0 ; i< Elist.uniqTokens() ; i++){
      if (0 < MAX_FERTILITY){
	nTable.getRef(i,0)=PROB(0.2);
	if (1 < MAX_FERTILITY){
	  nTable.getRef(i,1)=PROB(0.65);
	  if (2 < MAX_FERTILITY){
	    nTable.getRef(i,2)=PROB(0.1);
	  if (3 < MAX_FERTILITY)
	    nTable.getRef(i,3)=PROB(0.04);
	  PROB val = 0.01/(MAX_FERTILITY-4);
	  for (k = 4 ; k < MAX_FERTILITY ; k++)
	    nTable.getRef(i, k)=val;
	  }
	}
      }
    }
  } // end of else (!simple) 
  p0 = 0.95;
  p1 = 0.05;
  if (dump_files){
    tfile = Prefix + ".t2to3" ;
    afile = Prefix + ".a2to3" ;
    nfile = Prefix + ".n2to3" ;
    dfile = Prefix + ".d2to3" ;
    p0file = Prefix + ".p0_2to3" ;
    
    if( OutputInAachenFormat==0 )
      tTable.printProbTable(tfile.c_str(),Elist.getVocabList(),Flist.getVocabList(),OutputInAachenFormat);
    aTable.printTable(afile.c_str());
    dTable.printTable(dfile.c_str());
    nCountTable.printNTable(Elist.uniqTokens(), nfile.c_str(), Elist.getVocabList(),OutputInAachenFormat);
    ofstream of(p0file.c_str());
    of << p0;
    of.close();
  }
  errorReportAL(cerr,"IBM-2");
  if(simple)
    {
      perp.record("T2To3");
      trainVPerp.record("T2To3");
    }
  else
    {
      perp.record("ST2To3");
      trainVPerp.record("ST2To3");
    }
}

void model3::transferSimple(/*model1& m1, model2& m2, */ sentenceHandler& sHandler1, 
			    bool dump_files, Perplexity& perp, Perplexity& trainVPerp,bool updateT)
{
  /* 
     This function performs simple Model 2 -> Model 3 transfer.
     It sets values for n and p without considering Model 2's ideas.
     It sets d values based on a.
  */
  time_t st, fn;
  // just inherit these from the previous models, to avoid data duplication
 
  st = time(NULL);
  cerr << "==========================================================\n";
  cerr << "\nTransfer started at: "<< ctime(&st) << '\n';  
  
  cerr << "Simple tranfer of Model2 --> Model3 (i.e. estimating initial parameters of Model3 from Model2 tables)\n";
  
  estimate_t_a_d(sHandler1, perp, trainVPerp, true, dump_files,updateT) ;
  fn = time(NULL) ;
  cerr << "\nTransfer: TRAIN CROSS-ENTROPY " << perp.cross_entropy()
       << " PERPLEXITY " << perp.perplexity() << '\n';
  cerr << "\nTransfer took: " << difftime(fn, st) << " seconds\n";
  cerr << "\nTransfer Finished at: "<< ctime(&fn) << '\n';  
  cerr << "==========================================================\n";
  
}


void model3::transfer(sentenceHandler& sHandler1,bool dump_files, Perplexity& perp, Perplexity& trainVPerp,bool updateT)
{
  if (Transfer == TRANSFER_SIMPLE)
    transferSimple(sHandler1,dump_files,perp, trainVPerp,updateT);
  {
    time_t st, fn ;
    
    st = time(NULL);
    cerr << "==========================================================\n";
    cerr << "\nTransfer started at: "<< ctime(&st) << '\n';  
    cerr << "Transfering Model2 --> Model3 (i.e. estimating initial parameters of Model3 from Model2 tables)\n";
    
    p1_count = p0_count = 0 ;
    
    estimate_t_a_d(sHandler1, perp, trainVPerp, false, dump_files,updateT);
    
    
    
    /* Below is a made-up stab at transferring t & a probs to p0/p1.
       (Method not documented in IBM paper).
       It seems to give p0 = .96, which may be right for Model 2, or may not.
       I'm commenting it out for now and hardwiring p0 = .90 as above. -Kevin
       
       // compute p0, p1 counts
       Vector<LogProb> nm(Elist.uniqTokens(),0.0);
       
       for(i=0; i < Elist.uniqTokens(); i++){
       for(k=1; k < MAX_FERTILITY; k++){
       nm[i] += nTable.getValue(i, k) * (LogProb) k;
       }
       }
       
       LogProb mprime;
       //  sentenceHandler sHandler1(efFilename.c_str());
       //  sentPair sent ;
       
       while(sHandler1.getNextSentence(sent)){
       Vector<WordIndex>& es = sent.eSent;
       Vector<WordIndex>& fs = sent.fSent;
       const float count  = sent.noOccurrences;
       
       l = es.size() - 1;
       m = fs.size() - 1;
       mprime = 0 ;
       for (i = 1; i <= l ; i++){
       mprime +=  nm[es[i]] ;
       }
       mprime = LogProb((int((double) mprime + 0.5)));  // round mprime to nearest integer 
       if ((mprime < m) && (2 * mprime >= m)) {
       //      cerr << "updating both p0_count and p1_count, mprime: " << mprime << 
       //	"m = " << m << "\n";
       p1_count +=  (m - (double) mprime)  * count ;
       p0_count +=  (2 * (double) mprime - m)  * count ;
       //  cerr << "p0_count = "<<p0_count << " , p1_count = " << p1_count << endl ;
       }
       else {
       //      p1_count += 0 ;
       //      cerr << "updating only p0_count, mprime: " << mprime << 
       //	"m = " << m << "\n";
       p0_count +=  double(m  * count) ;
       //  cerr << "p0_count = "<<p0_count << " , p1_count = " << p1_count << endl ;
       }
       }
       
       // normalize p1, p0 
       
       cerr << "p0_count = "<<p0_count << " , p1_count = " << p1_count << endl ;
       p1 = p1_count / (p1_count + p0_count ) ;
       p0 = 1 - p1;
       cerr << "p0 = "<<p0 << " , p1 = " << p1 << endl ;
       // Smooth p0 probability to avoid getting zero probability.
       if (0 == p0){
       p0 = (LogProb) SMOOTH_THRESHOLD ;
       p1 = p1 - (LogProb) SMOOTH_THRESHOLD ;
       }
       if (0 == p1){
       p1 = (LogProb) SMOOTH_THRESHOLD ;
       p0 = p0 - (LogProb) SMOOTH_THRESHOLD ;
       }
    */
    
    fn = time(NULL) ;
    cerr << "\nTransfer: TRAIN CROSS-ENTROPY " << perp.cross_entropy()
	 << " PERPLEXITY " << perp.perplexity() << '\n';
    //    cerr << "tTable contains " << tTable.getHash().bucket_count() 
    //	 << " buckets and  " << tTable.getHash().size() << " entries." ;
    cerr << "\nTransfer took: " << difftime(fn, st) << " seconds\n";
    cerr << "\nTransfer Finished at: "<< ctime(&fn) << endl;  
    cerr << "==========================================================\n";
    
  }

}
