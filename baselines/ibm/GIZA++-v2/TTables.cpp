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
#include "TTables.h"
#include "Parameter.h"

GLOBAL_PARAMETER(float,PROB_CUTOFF,"PROB CUTOFF","Probability cutoff threshold for lexicon probabilities",PARLEV_OPTHEUR,1e-7);
GLOBAL_PARAMETER2(float, COUNTINCREASE_CUTOFF,"COUNTINCREASE CUTOFF","countCutoff","Counts increment cutoff threshold",PARLEV_OPTHEUR,1e-6);

#ifdef BINARY_SEARCH_FOR_TTABLE
template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::printCountTable(const char *, 
					 const Vector<WordEntry>&, 
					 const Vector<WordEntry>&,
					 const bool) const
{
}

template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::printProbTable(const char *filename, 
					 const Vector<WordEntry>& evlist, 
					 const Vector<WordEntry>& fvlist,
					 const bool actual) const
{
  ofstream of(filename);
  /*  for(unsigned int i=0;i<es.size()-1;++i)
    for(unsigned int j=es[i];j<es[i+1];++j)
      {
	const CPPair&x=fs[j].second;
	WordIndex e=i,f=fs[j].first;
	if( actual )
	  of << evlist[e].word << ' ' << fvlist[f].word << ' ' << x.prob << '\n';
	else
	  of << e << ' ' << f << ' ' << x.prob << '\n';
	  }*/
  for(unsigned int i=0;i<lexmat.size();++i)
    {
      if( lexmat[i] )
	for(unsigned int j=0;j<lexmat[i]->size();++j)
	  {
	    const CPPair&x=(*lexmat[i])[j].second;
	    WordIndex e=i,f=(*lexmat[i])[j].first;
	    if( x.prob>PROB_SMOOTH )
	      if( actual )
		of << evlist[e].word << ' ' << fvlist[f].word << ' ' << x.prob << '\n';
	      else
		of << e << ' ' << f << ' ' << x.prob << '\n';
	  }
    }
}

template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::printProbTableInverse(const char *, 
				   const Vector<WordEntry>&, 
				   const Vector<WordEntry>&, 
				   const double, 
				   const double, 
				   const bool ) const
{
}
template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::normalizeTable(const vcbList&, const vcbList&, int)
{
  for(unsigned int i=0;i<lexmat.size();++i)
    {
      double c=0.0;
      if( lexmat[i] )
	{
	  unsigned int lSize=lexmat[i]->size();
	  for(unsigned int j=0;j<lSize;++j)
	    c+=(*lexmat[i])[j].second.count;
	  for(unsigned int j=0;j<lSize;++j)
	    {
	      if( c==0 )
		(*lexmat[i])[j].second.prob=1.0/(lSize);
	      else
		(*lexmat[i])[j].second.prob=(*lexmat[i])[j].second.count/c;
	      (*lexmat[i])[j].second.count=0;
	    }
	}
    }
}

template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::readProbTable(const char *){
}

template class tmodel<COUNT,PROB> ; 
#else
/* ------------------ Method Definiotns for Class tmodel --------------------*/

#
template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::printCountTable(const char *filename, 
					 const Vector<WordEntry>& evlist, 
					 const Vector<WordEntry>& fvlist,
					 const bool actual) const
     // this function dumps the t table. Each line is of the following format:
     //
     // c(target_word/source_word) source_word target_word
{
  ofstream of(filename);
  typename hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::const_iterator i;
  for(i = ef.begin(); i != ef.end();++i){
    if ( ((*i).second).count >  COUNTINCREASE_CUTOFF)
      if (actual)
	of <<  ((*i).second).count << ' ' << evlist[ ((*i).first).first ].word << ' ' << fvlist[((*i).first).second].word << ' ' << (*i).second.prob << '\n';
      else 
	of << ((*i).second).count << ' ' <<  ((*i).first).first  << ' ' << ((*i).first).second << ' ' << (*i).second.prob << '\n';
  }
}

template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::printProbTable(const char *filename, 
					 const Vector<WordEntry>& evlist, 
					 const Vector<WordEntry>& fvlist,
					 const bool actual) const
     // this function dumps the t table. Each line is of the following format:
     //
     // source_word target_word p(target_word/source_word)
{
  ofstream of(filename);
  typename hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::const_iterator i;
  for(i = ef.begin(); i != ef.end();++i)
    if( actual )
      of << evlist[((*i).first).first].word << ' ' << 
	fvlist[((*i).first).second].word << ' ' << (*i).second.prob << '\n';
    else
      of << ((*i).first).first << ' ' << ((*i).first).second << ' ' << 
	(*i).second.prob << '\n';
}

template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::printProbTableInverse(const char *filename, 
				   const Vector<WordEntry>& evlist, 
				   const Vector<WordEntry>& fvlist, 
				   const double, 
				   const double, 
				   const bool actual) const
  // this function dumps the inverse t table. Each line is of the format:
  //
  // target_word_id source_word_id p(source_word/target_word)
  //
  // if flag "actual " is true then print actual word entries instead of 
  // token ids
{
  cerr << "Dumping the t table inverse to file: " << filename << '\n';
  ofstream of(filename);
  typename hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::const_iterator i;
  PROB p_inv = 0 ;
  //  static const PROB ratio(double(fTotal)/eTotal);
  WordIndex e, f ;
  int no_errors(0);
  vector<PROB> total(fvlist.size(),PROB(0)) ; // Sum over all e of P(f/e) * p(e) - needed for normalization
 
  for(i = ef.begin(); i != ef.end(); i++){
    e = ((*i).first).first ;
    f = ((*i).first).second ;
    total[f] += (PROB) evlist[e].freq * ((*i).second.prob); //add P(f/ei) * F(ei) 
  }
  
  for(i = ef.begin(); i != ef.end(); i++){
    e = ((*i).first).first ;
    f = ((*i).first).second ;
    p_inv = ((*i).second.prob) * (PROB) evlist[e].freq / total[f] ;
    if (p_inv > 1.0001 || p_inv < 0){
      no_errors++;
      if (no_errors <= 10){
	cerr << "printProbTableInverse(): Error - P("<<evlist[e].word<<"("<<
	  e<<") / "<<fvlist[f].word << "("<<f<<")) = " << p_inv <<'\n';
	cerr << "f(e) = "<<evlist[e].freq << " Sum(p(f/e).f(e)) = " << total[f] <<
	  " P(f/e) = " <<((*i).second.prob)  <<'\n';
	if (no_errors == 10)
	  cerr<<"printProbTableInverse(): Too many P inverse errors ..\n";
      }
    }
    if (actual)
      of << fvlist[f].word << ' ' << evlist[e].word << ' ' << p_inv << '\n';
    else 
      of << f << ' ' << e << ' ' << p_inv <<  '\n';
  }
}
/*



{
  cerr << "Dumping the t table inverse to file: " << filename << '\n';
  ofstream of(filename);
  hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::const_iterator i;
  PROB p_inv = 0 ;
  static const PROB ratio(double(fTotal)/eTotal);
  WordIndex e, f ;
  for(i = ef.begin(); i != ef.end(); i++){
    e = ((*i).first).first ;
    f = ((*i).first).second ;
    p_inv = ((*i).second.prob) * ratio * (PROB) evlist[e].freq / 
      (PROB) fvlist[f].freq ;
    if (actual)
      of << fvlist[f].word << ' ' << evlist[e].word << ' ' << p_inv << '\n';
    else 
      of << f << ' ' << e << ' ' << p_inv <<  '\n';
  }
}
*/
template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::normalizeTable(const vcbList&engl, const vcbList&french, int iter)
  // normalize conditional probability P(fj/ei):
  // i.e. make sure that Sum over all j of P(fj/e) = 1  
  // this method reads the counts portion of the table and normalize into
  // the probability portion. Then the counts are cleared (i.e. zeroed)
  // if the resulting probability of an entry is below a threshold, then 
  // remove it .
{
  if( iter==2 )
    {
      total2.resize(engl.uniqTokens());for(unsigned int i=0;i<total2.size();i++)total2[i]=0.0;
    }
  nFrench.resize(engl.uniqTokens());for(unsigned int i=0;i<nFrench.size();i++)nFrench[i]=0;
  nEng.resize(french.uniqTokens());for(unsigned int i=0;i<nEng.size();i++)nEng[i]=0;
  Vector<double> total(engl.uniqTokens(),0.0);
  //Vector<int> nFrench(engl.uniqTokens(), 0);
  //Vector<int> nEng(french.uniqTokens(), 0);

  typename hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::const_iterator i;
  for(i = ef.begin(); i != ef.end(); i++){ // for all possible source words e
    if( iter==2 )
      total2[((*i).first).first] += (*i).second.count;
    total[((*i).first).first] += (*i).second.count;
    nFrench[((*i).first).first]++;
    nEng[((*i).first).second]++;
  }
  for(unsigned int k=0;k<engl.uniqTokens();++k)
    if( nFrench[k] )
      {
	double probMass=(french.uniqTokensInCorpus()-nFrench[k])*PROB_SMOOTH;
	if( probMass<0.0 )
	  cout << k << " french.uniqTokensInCorpus(): " << french.uniqTokensInCorpus() << "  nFrench[k]:"<< nFrench[k] << '\n';
	total[k]+= total[k]*probMass/(1-probMass);
      }
  typename hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::iterator j, k;
  PROB p ;
  int nParams=0;
  for(j = ef.begin(); j != ef.end(); ){
    k = j;
    k++ ;
    if( (total[((*j).first).first])>0.0 )
      p = ((((*j).second).count) /(total[((*j).first).first])) ;
    else
      p= 0.0;
    if (p > PROB_CUTOFF)
      {
	if( iter>0 )
	  {
	    ((*j).second).prob = 0 ;
	    ((*j).second).count = p ;
	  }
	else
	  {
	    ((*j).second).prob = p ;
	    ((*j).second).count = 0 ;
	  }
	nParams++;
      }
    else {
      erase(((*j).first).first, ((*j).first).second);
    }
    j = k ;
  }
  if( iter>0 )
    return normalizeTable(engl, french, iter-1);
  else
    {
    }
}

template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::readProbTable(const char *filename){
  /* This function reads the t table from a file.
     Each line is of the format:  source_word_id target_word_id p(target_word|source_word)
     This is the inverse operation of the printTable function.
     NAS, 7/11/99
  */
  ifstream inf(filename);
  cerr << "Reading t prob. table from " << filename << "\n";
  if(!inf){
    cerr << "\nERROR: Cannot open " << filename << "\n";
    return;
  }
  WordIndex src_id, trg_id;
  PROB prob;
  int nEntry=0;
  while(    inf >> src_id  >> trg_id  >> prob){
    insert(src_id, trg_id, 0.0, prob);
    nEntry++;
  }
  cerr << "Read " << nEntry << " entries in prob. table.\n";
}

template class tmodel<COUNT,PROB> ; 

/* ---------------- End of Method Definitions of class tmodel ---------------*/


#endif
