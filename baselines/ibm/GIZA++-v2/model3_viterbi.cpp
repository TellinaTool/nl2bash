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


LogProb model3::prob_of_target_and_alignment_given_source(Vector<WordIndex>& A, 
							Vector<WordIndex>& Fert, 
							tmodel<COUNT, PROB>& tTable, 
							Vector<WordIndex>& fs, 
							Vector<WordIndex>& es)
{
  LogProb total = 1.0 ;
  LogProb temp = 0.0 ;
  const LogProb zero = 0.0 ;
  WordIndex l = es.size()-1, m = fs.size()-1;
  WordIndex i, j ;

  total *= pow(double(1-p1), m-2.0 * Fert[0]) * pow(double(p1), double(Fert[0]));
  if (total == 0)
    return(zero);
  for (i = 1 ; i <= Fert[0] ; i++){  // loop caculates m-fert[0] choose fert[0]
    total *= double(m - Fert[0] - i + 1) / i ;
    if (total == 0)
      return(zero);
  }
  for (i = 1 ; i <= l ; i++){ // this loop calculates fertilities term
    total *= double(nTable.getValue(es[i], Fert[i])) * (LogProb) factorial(Fert[i]);
    if (total == 0)
      return(zero);
  }
  for (j = 1 ; j <= m ; j++){
    //    temp = tTable.getValue(es[A[j]], fs[j]) ;
    temp = double(tTable.getProb(es[A[j]], fs[j])) ;
    total *= temp ;
    if (0 != A[j])
      total *= double(dTable.getValue(j, A[j], l, m));
    if (total == 0)
      return(zero);
  }
  return(total);
}

LogProb model3::prob_of_target_given_source(tmodel<COUNT, PROB>& tTable, 
					  Vector<WordIndex>& fs, 
					  Vector<WordIndex>& es)
{
  
  WordIndex x, y ;
  LogProb total = 0 ;
  //  WordIndex l = es.size(), m = fs.size();
  WordIndex l = es.size()-1, m = fs.size()-1;
  Vector<WordIndex> A(fs.size(),/*-1*/0);
  Vector<WordIndex> Fert(es.size(),0);
  WordIndex i,j ;

  for ( x = 0 ; x < pow(l+1.0, double(m)) ; x++){ // For all possible alignmets A
    y = x ;
    //    for (j = 1 ; j < m ; j++){
    for (j = 1 ; j <= m ; j++){
      A[j] = y % (l+1) ;
      y /= (l+1) ;
    }
    //    for(i = 0 ; i < l ; i++)
    for(i = 0 ; i <= l ; i++)
      Fert[i] = 0 ;
    //    for (j = 1 ; j < m ; j++)
    for (j = 1 ; j <= m ; j++)
      Fert[A[j]]++;
    //    if (2 * Fert[0] < m){ 
    if (2 * Fert[0] <= m){ /* consider alignments that has Fert[0] less than
			      half the length of french sentence  */
      total += prob_of_target_and_alignment_given_source(A, Fert, tTable, fs, es);
    }
  }
  return(total);
}


LogProb model3::scoreOfMove(Vector<WordIndex>& es, 
			  Vector<WordIndex>& fs, 
			  Vector<WordIndex>& A, 
			  Vector<WordIndex>& Fert, 
			  tmodel<COUNT, PROB>& tTable, 
			  WordIndex j, 
			  WordIndex i)
     // returns the scaling factor of the original score if A[j] is linked to
     // i, no change is really made to A
     // but the score is calculated if the move is to be taken (i.e. 
     // no side effects on Alignment A nor its Fertility Fert
     // If the value of the scaling factor is:
     //    1: then the score of the new alignment if the move is taken will
     //       not change.
     //    0.5: the new score is half the score of the original alignment.
     //    2.0: the new score will be twice as much.
     //
{
  //  LogProb score;
  LogProb change ;
  WordIndex m, l ;
  
  m = fs.size() - 1;
  l = es.size() - 1;
  
  
  if (A[j] == i)
    //    return(original_score);
    return(1) ;
  else if (A[j] == 0){ // a move from position zero to something else
    change = double(p0*p0)/p1 *
      (double((Fert[0]*(m-Fert[0]+1))) / ((m-2*Fert[0]+1)*(m-2*Fert[0]+2))) *
      (Fert[i]+1) *
      double(nTable.getValue(es[i], Fert[i]+1)) / 
      double(nTable.getValue(es[i], Fert[i])) *
      double(tTable.getProb(es[i], fs[j])) /
      double(tTable.getProb(es[A[j]], fs[j])) *
      double(dTable.getValue(j, i, l, m));
  }
  else if (i == 0){ // a move to position zero
    change= 
      ((double(p1) / (p0*p0)) *
       (double((m-2*Fert[0])*(m-2*Fert[0]-1))/((Fert[0]+1)*(m-Fert[0]))) *
       (double(1)/Fert[A[j]]) *
       double(nTable.getValue(es[A[j]], Fert[A[j]]-1)) /
       double(nTable.getValue(es[A[j]], Fert[A[j]]))*
       double(tTable.getProb(es[i], fs[j])) /
       double(tTable.getProb(es[A[j]], fs[j])) *
       1.0 / double(dTable.getValue(j, A[j], l, m)));
  }
  else{ // a move that does not involve position zero
    change = 
      ((double(Fert[i]+1)/Fert[A[j]]) *
       double(nTable.getValue(es[A[j]], Fert[A[j]]-1)) / 
       double(nTable.getValue(es[A[j]], Fert[A[j]])) *
       double(nTable.getValue(es[i], Fert[i]+1)) /
       double(nTable.getValue(es[i], Fert[i])) *
       double(tTable.getProb(es[i], fs[j]))/
       double(tTable.getProb(es[A[j]], fs[j])) *
       double(dTable.getValue(j, i, l, m))/
       double(dTable.getValue(j, A[j], l, m)));
  }
  return(change);  
}


LogProb model3::scoreOfSwap(Vector<WordIndex>& es, 
			  Vector<WordIndex>& fs, 
			  Vector<WordIndex>& A, 
			  tmodel<COUNT, PROB>& tTable, 
			  int j1, 
			  int j2)
  // returns the scaling factor of the original score if the swap to 
  // take place, 
  // No side effects here (none of the parameters passed is changed!
  // (i.e. the alignment A is not really changed)
  // If the value of the scaling factor is:
  //    1: then the score of the new alignment if the move is taken will
  //       not change.
  //    0.5: the new score is half the score of the original alignment.
  //    2.0: the new score will be twice as much.
  //
{
  LogProb score ;
  WordIndex i1, i2, m, l ;

  m = fs.size() - 1 ;
  l = es.size() - 1 ;
  if (j1 == j2 || A[j1] == A[j2]) // if swapping same position return ratio 1
    return(1);  
  else {
    i1 = A[j1] ;
    i2 = A[j2] ;
    score = 
      double(tTable.getProb(es[i2], fs[j1]))/double(tTable.getProb(es[i1], fs[j1])) * 
      double(tTable.getProb(es[i1], fs[j2]))/double(tTable.getProb(es[i2], fs[j2]));
    if (i1 != 0){
      score *= double(dTable.getValue(j2, i1, l, m))/double(dTable.getValue(j1, i1, l, m));
    }
    if (i2 != 0){
      score *= double(dTable.getValue(j1, i2, l, m))/double(dTable.getValue(j2, i2, l, m));
    }
    return(score);
  }
}



void model3::hillClimb(Vector<WordIndex>& es, 
		       Vector<WordIndex>& fs, 
		       Vector<WordIndex>& A, 
		       Vector<WordIndex>& Fert, 
		       LogProb& best_score, 
		       tmodel<COUNT, PROB>& tTable, 
		       int = -1, 
		       int j_peg = -1)
  // Hill climbing given alignment A  .
  // Alignment A will be updated and also best_score
  // if no pegging is needed i_peg == -1, and j_peg == -1
{
  WordIndex i, j, l, m, j1, old_i;
  LogProb change ;
  bool local_minima;
  int level = 0 ;
  LogProb best_change_so_far, best_change ;
  Vector<WordIndex> A_so_far; 
  Vector<WordIndex> Fert_so_far;
  
  l = es.size() - 1;
  m = fs.size() - 1;
  if (Log)
    logmsg << "\nStarting hill climbing with original score: " << best_score <<"\n";
  best_change = 1 ; // overall scaling factor (i.e. from the begining of climb
  do {
    best_change_so_far = 1 ; // best scaling factor of this level of hill climb
    local_minima = true ;
    for (j = 1 ; j <= m ; j++){ 
      if (int(j) != j_peg){ // make sure not to change the pegged link
	for (j1 = j + 1 ; j1 <= m; j1++){ 
	  // for all possible swaps
	  // make sure you are not swapping at same position
	  if ((A[j] != A[j1]) && (int(j1) != j_peg)){
	    //	    change = scoreOfSwap(es, fs, A, best_score, tTable, j, j1);
	    change = scoreOfSwap(es, fs, A, tTable, j, j1);
	    if (change > best_change_so_far){ // if better alignment found, keep it
	      local_minima = false ;
	      best_change_so_far = change ;
	      A_so_far = A ;
	      Fert_so_far = Fert ;
	      old_i = A_so_far[j] ;
	      A_so_far[j] = A_so_far[j1] ;
	      A_so_far[j1] = old_i ;
	    } // end of if (change > best_change_so_far) 
	  } // end of if (A[j] != A[j1]  ..)
	} // of for (j1 = j+1  ....)
	//      for (i = 0 ; i < l ; i++){ // all possible moves
	for (i = 0 ; i <= l ; i++){ // all possible moves
	  if (i != A[j]){ // make sure not to move to same position
	    if (i != 0 || (m >= 2 * (Fert[0]+1))){ // if moving to NULL word 
	      // (pos 0), make sure not to violate the fertility restriction
	      // i.e. NULL can not take more than half the target words 
	      //	      change = scoreOfMove(es, fs, A, Fert, best_score, tTable, j, i);
	      change = scoreOfMove(es, fs, A, Fert, tTable, j, i);
	      if (change > best_change_so_far){ // if better alignment found, keep it
		best_change_so_far = change ;
		local_minima = false ;
		A_so_far = A ;
		Fert_so_far = Fert ;
		old_i = A_so_far[j] ;
		A_so_far[j] = i ;
		Fert_so_far[old_i]-- ;
		Fert_so_far[i]++ ;
	      } // end of if (change > best_change_so_far)
	    } // end of if ((i!=0) ...
	  } // end of if (i != A[j] )
	} // end of for (i = 0 ;  ....)
      } // end of if(j != j_peg)      
    } // end of for (j = 1 ; ...)
    level++;
    if (!local_minima){
      if (best_change_so_far > 1){ // if current chage is improving 
	A = A_so_far ;
	Fert = Fert_so_far ;
	best_change *= best_change_so_far ;
      }
      else{
	local_minima = true ;
      }
    } // end of if(!local_minima)
    if (Log)
    logmsg << "." ;
    if (level> 15)
      cerr << "." ;
  } while (local_minima == false);
  if (Log)
    logmsg << "\n" << "Hill Climb Level: " << level << " score: scaling old: " <<(best_score*best_change) ;
  if (level > 15)
    cerr << "\nHill Climb Level: " << level << " score: scaling old: " <<(best_score*best_change) ;
  best_score = prob_of_target_and_alignment_given_source(A, Fert, tTable, fs, es);
  if (Log) 
    logmsg << " using new calc: " << best_score << '\n';
  if (level>15) 
    cerr << " using new calc: " << best_score << '\n';
}


void model3::findBestAlignment(Vector<WordIndex>& es, 
			       Vector<WordIndex>& fs, 
			       Vector<WordIndex>& A, 
			       Vector<WordIndex>& Fert, 
			       LogProb& best_score, 
			       /*tmodel<COUNT, PROB>& tTable, 
				 amodel<PROB>& aTable, */
			       int i_peg = -1 , 
			       int j_peg = -1 )
     // This finds the best Model2 alignment (i.e. no fertilities stuff) in A
     // for the given sentence pair. Its score is returned in A. Its fertility
     // info in Fert. 
     // if j_peg == -1 && i_peg == -1 then No pegging is performed.
{
  WordIndex i, j, l, m, best_i=0;
  LogProb temp, score, ss;
  
  l = es.size() - 1;
  m = fs.size() - 1;
  for (i=0 ; i <= l ; i++)
    Fert[i] = 0 ;
  ss = 1 ;
  if ((j_peg != -1) && (i_peg != -1)){ //  if you're doing pegging
    A[j_peg]  = i_peg ;
    Fert[i_peg] = 1 ;
    ss *= double(tTable.getProb(es[i_peg], fs[j_peg])) * 
      double(aTable.getValue(i_peg, j_peg, l, m));
  }
  for (j = 1 ; j <= m ; j++){
    if (int(j) != j_peg){
      score = 0 ;
      for (i = 0 ; i <= l ; i++){
	// first make sure that connecting target word at pos j to source word 
	// at  pos i will not lead to a violation on Fertility restrictions 
	// (e.g. maximum fertility for a word, max fertility for NULL word, etc)
	if ((Fert[i]+1 < MAX_FERTILITY) && ((i == 0 &&  (m >= 2*(Fert[0]+1)))
					    || (i != 0))){
	  temp = double(tTable.getProb(es[i], fs[j])) * 
	    double(aTable.getValue(i, j, l, m));
	  if (temp > score ){
	    best_i = i ;
	    score = temp ;
	  } // end of if (temp > score)
	} // end of if (((i == 0 ...)
      } // end of for (i= 0 ...)
      if (score == 0){
	cerr << "WARNING: In searching for model2 best alignment\n " ;
	cerr << "Nothing was set for target token " << fs[j] << 
	  "at position j: " << j << "\n";
	for (i = 0 ; i <= l ; i++){
	  cerr << "i: " << i << "ttable("<<es[i]<<", "<<fs[j]<<") = " <<
	    tTable.getProb(es[i], fs[j]) << " atable(" << i<<", "<<j<<", "<<
	    l<<", "<<m<<") = "<< aTable.getValue(i, j, l, m) << " product " <<
	    double(tTable.getProb(es[i], fs[j])) * 
	    double(aTable.getValue(i, j, l, m)) << '\n';
	  if ((Fert[i]+1 < MAX_FERTILITY) && ((i == 0 &&  (m >= 2*(Fert[0]+1)))
					      || (i != 0)))
	    cerr <<"Passed fertility condition \n";
	  else 
	    cerr <<"Failed fertility condition \n";
	}	    

      } // end of if (score == 0)
      else {
	Fert[best_i]++ ;
	A[j] = best_i ;
      }
      ss *= score ;
    } // end of if (j != j_peg)
  } // end of for (j == 1 ;  ...)
  if (ss <= 0){
    cerr << "WARNING: Model2 viterbi alignment has zero score for sentence pair:\n" ;
    printSentencePair(es, fs, cerr);
  } 
  best_score = prob_of_target_and_alignment_given_source(A, Fert, tTable, fs, es);
  if (Log)
    logmsg << "finding best alignment : score : " << ss <<"p(f, a/e) = "<< best_score<<"\n"; 
}
  
void model3::collectCountsOverAlignement(const Vector<WordIndex>& es, 
					 const Vector<WordIndex>& fs, 
					 const Vector<WordIndex>& A, 
					 LogProb score, 
					 float count)
{
  WordIndex j,i,l,m ;
  Vector<WordIndex> Fert(es.size(),0);
  l = es.size() - 1 ;
  m = fs.size() - 1 ;
  score *= LogProb(count);
  COUNT temp = COUNT(score) ;
  for (i=0 ; i <= l ; i++)
    Fert[i] = 0 ;
  for (j = 1 ; j <= m ; j++){
    Fert[A[j]]++;
    tTable.incCount(es[A[j]], fs[j], temp);
    //    tCountTable.getRef(es[A[j]], fs[j])+=score;
    if (A[j])
      dCountTable.getRef(j, A[j], l, m)+= temp ;
    aCountTable.getRef(A[j], j, l, m)+= temp ;
  }
  for(i = 0 ; i <= l ; i++)
    nCountTable.getRef(es[i], Fert[i])+= temp ;
  //  p1_count += score * (LogProb) (Fert[0]) ;
  //  p0_count += score * (LogProb) ((m - 2 * Fert[0])) ;
  p1_count += temp * (Fert[0]) ;
  p0_count += temp *  ((m - 2 * Fert[0])) ;
}



void model3::findAlignmentsNeighborhood(Vector<WordIndex>& es, 
					Vector<WordIndex>& fs, 
					LogProb&align_total_count, 
					alignmodel&neighborhood, 
					int i_peg = -1, 
					int j_peg = -1
					)
  // Finding the Neigborhood of a best viterbi alignment after hill climbing
     // if (i_peg == -1 and j_peg == -1, then  No Pegging is done.
{
    LogProb best_score,score;
    WordIndex i,j,l,m,old_i,j1;
    Vector<WordIndex> A(fs.size(),0);
    Vector<WordIndex> Fert(es.size(),0);
    time_t it_st;
    
    best_score = 0 ;
    l = es.size() - 1;
    m = fs.size() - 1;
    findBestAlignment(es, fs, A, Fert, best_score, /*tTable, aTable,*/ i_peg, j_peg);
    if (best_score == 0){
      cerr << "WARNING: viterbi alignment score is zero for the following pair\n";
      printSentencePair(es, fs, cerr);
    }
    hillClimb(es, fs, A, Fert, best_score, tTable, i_peg, j_peg);
    if (best_score <= 0){
      cerr << "WARNING: Hill Climbing yielded a zero score viterbi alignment for the following pair:\n";
      printSentencePair(es, fs, cerr);      
      if(Log){
	logmsg << "WARNING: Hill Climbing yielded a zero score viterbi alignment for the following pair:\n";
	printSentencePair(es, fs, logmsg);
      }
    }
    else { // best_score > 0
      //      if (2 * Fert[0] < m ){ 
      if (2*Fert[0] <= m ){ 
	/* consider alignments that has Fert[0] less than
	   half the number of words in French sentence */
	if (neighborhood.insert(A, best_score)){
	  align_total_count += best_score ;
	}
      }
      else { // else part is added for debugging / Yaser
	cerr << "WARNING:Best Alignment found violates Fertility requiremnets !!\n" ;
	for (i = 0 ; i <= l ; i++)
	  cerr << "Fert["<<i<<"] = "<< Fert[i] << "\n";
	for (j = 1 ; j <= m ; j++){
	  cerr << "A["<<j<<"] = "<< A[j] <<"\n";
	}
	cerr << "Condition violated : 2 * Fert[0] <= m " << 2*Fert[0] <<"?"<<
	  m << "\n";
      } // end of added code for debugging // Yaser
      it_st = time(NULL) ;
      
      // Now find add all neighbors of the best alignmet to the  collection
      for (j = 1 ; j <= m ; j++){
	for (j1 = j + 1 ; j1 <= m; j1++){ // all possible swaps
	  if (A[j] != A[j1]){// make sure you are not swapping at same position
	    //	    score = best_score * scoreOfSwap(es, fs, A, best_score, tTable, j, j1);
	    score = best_score * scoreOfSwap(es, fs, A, tTable, j, j1);
	    // ADD  A and its score to list of alig. to collect counts over
	    if (2 * Fert[0] <= m && score > 0){ 
	      /* consider alignments that has Fert[0] less than
		 half the number of words in French sentence */
	      old_i = A[j] ;
	      A[j] = A[j1] ;
	      A[j1] = old_i ;
	      if (neighborhood.insert(A, score)){
		align_total_count += score ;      
	      }	    
	      // restore original alignment 
	      old_i = A[j] ;
	      A[j] = A[j1] ;
	      A[j1] = old_i ;
	    }
	  }
	}
	for (i = 0 ; i <= l ; i++){ // all possible moves
	  if (i != A[j]){ // make sure not to move to same position
	    if ((Fert[i]+1 < MAX_FERTILITY) && 
		((i == 0 &&  (m >= 2*(Fert[0]+1))) || (i != 0))){ 
	      // consider legal alignments only
	      score = best_score * scoreOfMove(es, fs, A, Fert, tTable, j, i);
	      // ADD  A and its score to list of alig. to collect counts over
	      if (score > 0){
		old_i = A[j] ;
		A[j] = i ;
		Fert[old_i]-- ;
		Fert[i]++ ;
		// add to list of alignemts here  ******************
		if (neighborhood.insert(A, score)){
		  align_total_count += score ;	      
		}
		// now resotre alignment and fertilities to previoud values
		A[j] = old_i ;
		Fert[old_i]++ ;
		Fert[i]-- ;
	      } // end of if (score > 0)
	    } // end of if (i == 0 ...) 
	  } // end of if (i != A[j])
	}// end of for(i = 0 ; ...)
      }// end of for (j = 1 ; ...)
    } // of else best_score <= 0  
}

void model3::viterbi_loop(Perplexity& perp, Perplexity& viterbiPerp, sentenceHandler& sHandler1, 
			   bool dump_files, const char* alignfile, 
			   bool collect_counts, string model )
{
  WordIndex i, j, l, m ;
  ofstream of2 ;
  int pair_no;
  LogProb temp;

  if (dump_files)
    of2.open(alignfile);
  pair_no = 0 ; // sentence pair number 
  // for each sentence pair in the corpus
  perp.clear() ; // clears cross_entrop & perplexity 
  viterbiPerp.clear();
  sentPair sent ;
  while(sHandler1.getNextSentence(sent)){
    Vector<WordIndex>& es = sent.eSent;
    Vector<WordIndex>& fs = sent.fSent;
    const float count  = sent.getCount();
    if ((sent.sentenceNo % 1000) == 0)
      cerr <<sent.sentenceNo << '\n'; 
    time_t sent_s = time(NULL) ;
    pair_no++ ;
    l = es.size() - 1 ;
    m = fs.size() - 1 ;
    if (Log){
      logmsg << "Processing sentence pair:\n\t";
      printSentencePair(es, fs, logmsg);
      for (i = 0 ; i <= l ; i++)
	  logmsg << Elist.getVocabList()[es[i]].word << " ";
	logmsg << "\n\t";
	for (j = 1 ; j <= m ; j++)
	  logmsg << Flist.getVocabList()[fs[j]].word << " ";
	logmsg << "\n";
      } 

      LogProb align_total_count=0;
      //      LogProb best_score;

      Vector<WordIndex> viterbi_alignment;
      LogProb  viterbi_score ;
      alignmodel neighborhood;
      neighborhood.clear();
      align_total_count = 0;
      findAlignmentsNeighborhood(/*tTable, aTable,*/ /*p1_count, p0_count,*/ es, fs, align_total_count, neighborhood) ;
      if (Peg){
	for (i = 0 ; i <= l ; i++)
	  for (j = 1 ; j <= m ; j++){
	    if ( (tTable.getProb(es[i], fs[j]) > PROB_SMOOTH) &&
		 (aTable.getValue(i, j, l, m) > PROB_SMOOTH) &&
		 (dTable.getValue(j, i, l, m) > PROB_SMOOTH))
	      findAlignmentsNeighborhood(/*tTable, aTable,*/ /*p1_count, 
							   p0_count, */ es, fs, align_total_count, neighborhood, i, j);  
	  }
      }
      //  Now Collect counts over saved neighborhoods
      viterbi_score = 0 ;
      if (Verbose)
	cerr << "\nCollecting counts over found alignments, total prob: " 
	     << align_total_count <<  "\n";
      if (Log)
	logmsg << "\nCollecting counts over found alignments, total prob: " 
	       << align_total_count <<  "\n";
      hash_map<Vector<WordIndex>, LogProb, hashmyalignment, equal_to_myalignment >::iterator align ;
      int acount = 0 ;
      if (align_total_count == 0 ){
	cerr << " WARNINIG: For the following sentence pair : \n";
	printSentencePair(es, fs, cerr);
	cerr << "The collection of alignments found have 0 probability!!\n";
	cerr << "No counts will be collected of it \n";
	if (Log){
	  logmsg << "The collection of alignments found have 0 probability!!\n";
	  logmsg << "No counts will be collected of it \n";
	}
      }
      else {
	if (collect_counts) {
	  for(align = neighborhood.begin(); align != neighborhood.end(); align++){
	    temp = (*align).second/align_total_count ;	  
	    collectCountsOverAlignement(/*tTable, aCountTable, */es, fs, /*p1_count, 
					  p0_count ,*/ ((*align).first), temp , count);
	    acount++;
	    if (viterbi_score < temp){
	      viterbi_alignment = ((*align).first);
	      viterbi_score = temp;
	    }
	  }
	} // end of if (collect_counts)
	perp.addFactor(log(double(align_total_count)), count, l, m,0);
	viterbiPerp.addFactor(log(double(viterbi_score)), count, l, m,0);
	
      if (Verbose){
	cerr << "Collected counts over "<<acount <<" (of "
	     << pow(double(m), double(l+1)) <<") differnet alignments\n";
	cerr << "Bucket count of alignments hash: "<<
	  neighborhood.getHash().bucket_count()<< ", size " <<
	  neighborhood.getHash().size() << "\n";
	}
	if (Log){
	  logmsg << "Collected counts over "<<acount <<" (of "
		 << pow(double(m), double(l+1)) <<") differnet alignments\n";
	  logmsg << "Bucket count of alignments hash: "<<
	    neighborhood.getHash().bucket_count()<< "\n";
	}
      } // end of else 
      // write best alignment (viterbi) for this sentence pair to alignment file 
      if (collect_counts){
	if (viterbi_score <= 0){
	  cerr << "Viterbi Alignment for this pair have score zero!!\n";
	  of2 << "\n\n";
	}
	else {
	  if (dump_files)
	    printAlignToFile(es, fs, Elist.getVocabList(), Flist.getVocabList(), of2, viterbi_alignment, pair_no, viterbi_score);
	  addAL(viterbi_alignment,sent.sentenceNo,l);
	}
      } // end of if (collect_counts) 
      double period = difftime(time(NULL), sent_s);
      if (Log)
      	logmsg << "processing this sentence pair ("<<l+1<<"x"<<m<<") : "<<
      	  (l+1)*m << " took : " << period << " seconds\n";
      if (Verbose)
	cerr << "processing this sentence pair took : " << period
	     << " seconds\n";
      
    } /* of sentence pair E, F */
    sHandler1.rewind();
    errorReportAL(cerr,model);
    perp.record(model);
    viterbiPerp.record(model);
    if (dump_files)
      of2.close();

}
