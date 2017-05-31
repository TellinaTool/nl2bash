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
/* --------------------------------------------------------------------------*
 *                                                                           *
 * Module : TTables                                                          *
 *                                                                           *
 * Prototypes File: TTables.h                                               *
 *                                                                           *
 * Objective: Defines clases and methods for handling I/O for Probability &  *
 *            Count tables and also alignment tables                         *
 *****************************************************************************/

#ifndef _ttables_h
#define _ttables_h 1


#include "defs.h"
#include "vocab.h"  

#include <cassert>
 
#include <iostream>
#include <algorithm>
#include <functional>
#include <map>
#include <set>
#include "Vector.h"
#include <utility>

#include <fstream>

#include "Globals.h"


/* The tables defined in the following classes are defined as hash tables. For
   example. the t-table is a hash function of a word pair; an alignment is 
   a hash function of a vector of integer numbers (sentence positions) and so
   on   */


/*----------- Defnition of Hash Function for class tmodel ------- -----------*/

typedef pair<WordIndex, WordIndex> wordPairIds;


class hashpair : public unary_function< pair<WordIndex, WordIndex>, size_t >
{
public:
  size_t operator() (const pair<WordIndex, WordIndex>& key) const
    {
      return (size_t) MAX_W*key.first + key.second; /* hash function and it 
						       is guarnteed to have 
						       unique id for each 
						       unique pair */
    }
};



/* ------------------ Class Prototype Definitions ---------------------------*
  Class Name: tmodel
  Objective: This defines the underlying data structur for t Tables and t 
  Count Tables. They are defined as a hash table. Each entry in the hash table
  is the probability (P(fj/ei) ) or count collected for ( C(fj/ei)). The 
  probability and the count are represented as log integer probability as 
  defined by the class LogProb .  

  This class is used to represents t Tables (probabiliity) and n (fertility 
  Tables and also their corresponding count tables .
 
 *---------------------------------------------------------------------------*/

//typedef float COUNT ;
//typedef LogProb PROB ;
template <class COUNT, class PROB>
class LpPair {
 public:
  COUNT count ;
  PROB  prob ;
 public: // constructor 
  LpPair():count(0), prob(0){} ;
  LpPair(COUNT c, PROB p):count(c), prob(p){};
} ;

#ifdef BINARY_SEARCH_FOR_TTABLE


template<class T>
T*mbinary_search(T*x,T*y,unsigned int val)
{
  if( y-x==0 )
    return 0;
  if( x->first==val)
    return x;
  if( y-x<2 )
    return 0;
  T*mid=x+(y-x)/2;
  if( val < mid->first )
    return mbinary_search(x,mid,val);
  else
    return mbinary_search(mid,y,val);
  
}

template<class T>
const T*mbinary_search(const T*x,const T*y,unsigned int val)
{
  if( y-x==0 )
    return 0;
  if( x->first==val)
    return x;
  if( y-x<2 )
    return 0;
  const T*mid=x+(y-x)/2;
  if( val < mid->first )
    return mbinary_search(x,mid,val);
  else
    return mbinary_search(mid,y,val);
  
}

template <class COUNT, class PROB>
class tmodel{
  typedef LpPair<COUNT, PROB> CPPair;
 public:
  int noEnglishWords;  // total number of unique source words
  int noFrenchWords;   // total number of unique target words
  //vector<pair<unsigned int,CPPair> > fs;
  //vector<unsigned int> es;
  vector< vector<pair<unsigned int,CPPair> >* > lexmat;

  void erase(WordIndex e, WordIndex f)
    {
      CPPair *p=find(e,f);
      if(p)
	*p=CPPair(0,0);
    };
  CPPair*find(int e,int f)
    {
      //pair<unsigned int,CPPair> *be=&(fs[0])+es[e];
      //pair<unsigned int,CPPair> *en=&(fs[0])+es[e+1];
      pair<unsigned int,CPPair> *be=&(*lexmat[e])[0];
      pair<unsigned int,CPPair> *en=&(*lexmat[e])[0]+(*lexmat[e]).size();
      pair<unsigned int,CPPair> *x= mbinary_search(be,en,f);
      if( x==0 )
	{
	  //cerr << "A:DID NOT FIND ENTRY: " << e << " " << f << '\n';
	  //abort();
	  return 0;
	}
      return &(x->second);
    }
  const CPPair*find(int e,int f)const
    {
      const pair<unsigned int,CPPair> *be=&(*lexmat[e])[0];
      const pair<unsigned int,CPPair> *en=&(*lexmat[e])[0]+(*lexmat[e]).size();
      //const pair<unsigned int,CPPair> *be=&(fs[0])+es[e];
      //const pair<unsigned int,CPPair> *en=&(fs[0])+es[e+1];
      const pair<unsigned int,CPPair> *x= mbinary_search(be,en,f);
      if( x==0 )
	{
	  //cerr << "B:DID NOT FIND ENTRY: " << e << " " << f << '\n';
	  //abort();
	  return 0;
	}

      return &(x->second);
    }
public:
  void insert(WordIndex e, WordIndex f, COUNT cval=0.0, PROB pval = 0.0){
    *find(e,f)=CPPair(cval,pval);
  }
  CPPair*getPtr(int e,int f){return find(e,f);}
  tmodel(const string&fn)
    {
      int count=0,count2=0;
      ifstream infile2(fn.c_str());
      int e,f,olde=-1,oldf=-1;
      pair<unsigned int,CPPair> cp;
      vector< pair<unsigned int,CPPair> > cps;
      while(infile2>>e>>f)
	{
	  cp.first=f;
	  assert(e>=olde);
	  assert(e>olde ||f>oldf);
	  if( e!=olde&&olde>=0 )
	    {
	      int oldsize=lexmat.size();
	      lexmat.resize(olde+1);
	      for(unsigned int i=oldsize;i<lexmat.size();++i)
		lexmat[i]=0;
	      lexmat[olde]=new vector< pair<unsigned int,CPPair> > (cps);
	      cps.clear();
	      if( !((*lexmat[olde]).size()==(*lexmat[olde]).capacity()) )
		cerr << "eRROR: waste of memory: " << (*lexmat[olde]).size() << " " << (*lexmat[olde]).capacity() << endl;
	      count2+=lexmat[olde]->capacity();
	    }
	  cps.push_back(cp);
	  olde=e;
	  oldf=f;
	  count++;
	}
      lexmat.resize(olde+1);
      lexmat[olde]=new vector< pair<unsigned int,CPPair> > (cps);
      count2+=lexmat[olde]->capacity();      
      cout << "There are " << count << " " << count2 << " entries in table" << '\n';
    }


  /*  tmodel(const string&fn)
    {
      size_t count=0;
      {
	ifstream infile1(fn.c_str());
	if( !infile1 )
	  {
	    cerr << "ERROR: can't read coocurrence file " << fn << '\n';
	    abort();
	  }
	int e,f;
	while(infile1>>e>>f)
	  count++;
      }
      cout << "There are " << count << " entries in table" << '\n';
      ifstream infile2(fn.c_str());
      fs.resize(count);
      int e,f,olde=-1,oldf=-1;
      pair<unsigned int,CPPair> cp;
      count=0;
      while(infile2>>e>>f)
	{
	  assert(e>=olde);
	  assert(e>olde ||f>oldf);
	  if( e!=olde )
	    {
	      es.resize(e+1);
	      for(unsigned int i=olde+1;int(i)<=e;++i)
		es[i]=count;
	    }
	  cp.first=f;
	  assert(count<fs.size());
	  fs[count]=cp;
	  //fs.push_back(cp);
	  olde=e;
	  oldf=f;
	  count++;
	}
      assert(count==fs.size());
      es.push_back(fs.size());
      cout << fs.size() << " " << count << " coocurrences read" << '\n';
      }*/
  void incCount(WordIndex e, WordIndex f, COUNT inc) 
    {
      if( inc )
	{
	  CPPair *p=find(e,f);
	  if( p )
	    p->count += inc ;
	}
    }

  PROB getProb(WordIndex e, WordIndex f) const
    {
      const CPPair *p=find(e,f);
      if( p )
	return max(p->prob, PROB_SMOOTH);
      else
	return PROB_SMOOTH;
    }

  COUNT getCount(WordIndex e, WordIndex f) const
    {
      const CPPair *p=find(e,f);
      if( p )
	return p->count;
      else
	return 0.0;
    }

  void printProbTable(const char* filename, const Vector<WordEntry>&, const Vector<WordEntry>&,bool actual) const;
  void printCountTable(const char* filename, const Vector<WordEntry>&, const Vector<WordEntry>&,bool actual) const;
  void printProbTableInverse(const char *filename, 
			     const Vector<WordEntry>& evlist, 
			     const Vector<WordEntry>& fvlist, 
			     const double eTotal, 
			     const double fTotal, 
			     const bool actual = false ) const;
  void normalizeTable(const vcbList&engl, const vcbList&french, int iter=2);
  void readProbTable(const char *filename); 
};


#else


template <class COUNT, class PROB>
class tmodel{
  typedef LpPair<COUNT, PROB> CPPair;
 public:
  int noEnglishWords;  // total number of unique source words
  int noFrenchWords;   // total number of unique target words
  hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> > ef;
  void erase(WordIndex e, WordIndex f)
  // In: a source and a target token ids.
  // removes the entry with that pair from table
    {
      ef.erase(wordPairIds(e, f));
    };

public:
  Vector<PROB> total2;
  Vector<int> nFrench;
  Vector<int> nEng;

 
  // methods;

  // insert: add entry P(fj/ei) to the hash function, Default value is 0.0 
  void insert(WordIndex e, WordIndex f, COUNT cval=0.0, PROB pval = 0.0){
    ef[wordPairIds(e, f)].count = cval ;
    ef[wordPairIds(e, f)].prob = pval ;
  }

  // returns a reference to the word pair, if does not exists, it creates it.
  CPPair&getRe(WordIndex e, WordIndex f)
    {return ef[wordPairIds(e, f)];}

  // returns a pointer to an existing word pair. if pair does not exists, 
  // the method returns the zero pointer (NULL)

  CPPair*getPtr(WordIndex e, WordIndex f) 
    {      
      // look up this pair and return its position
      typename hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::iterator i = ef.find(wordPairIds(e, f)); 
      if(i != ef.end())  // if it exists, return a pointer to it.
	return(&((*i).second));
      else return(0) ; // else return NULL pointer
    }

  void incCount(WordIndex e, WordIndex f, COUNT inc) 
    // increments the count of the given word pair. if the pair does not exist, 
    // it creates it with the given value.
    {
      if( inc )
	ef[wordPairIds(e, f)].count += inc ;
    }

  PROB getProb(WordIndex e, WordIndex f) const
    // read probability value for P(fj/ei) from the hash table 
    // if pair does not exist, return floor value PROB_SMOOTH
    {
      typename hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::const_iterator i= ef.find(wordPairIds(e, f));
      if(i == ef.end())  
	return PROB_SMOOTH; 
      else
	return max(((*i).second).prob, PROB_SMOOTH);
    }

  COUNT getCount(WordIndex e, WordIndex f) const
    /* read count value for entry pair (fj/ei) from the hash table */
    {
      typename hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::const_iterator i= ef.find(wordPairIds(e, f));
      if(i == ef.end())
	return 0; 
      else
	return ((*i).second).count;
    }

  inline const hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >& getHash(void) const {return ef;};
  /* get a refernece to the hash table */
  //inline void resize(WordIndex n) {ef.resize(n);};
  // to resize he hash table 

  void printProbTable(const char* filename, const Vector<WordEntry>&, const Vector<WordEntry>&,bool actual) const;
  void printCountTable(const char* filename, const Vector<WordEntry>&, const Vector<WordEntry>&,bool actual) const;
  // print the t table to the given file but this time print actual source and
  //     target words instead of thier token ids 
  
  void printProbTableInverse(const char *filename, 
			     const Vector<WordEntry>& evlist, 
			     const Vector<WordEntry>& fvlist, 
			     const double eTotal, 
			     const double fTotal, 
			     const bool actual = false ) const;
  // dump  inverse of t table (i.e P(ei/fj)) to the given file name, 
  //  if the given flag is true then actual words are printed not token ids 
  
  void normalizeTable(const vcbList&engl, const vcbList&french, int iter=2);
  // to norlmalize the table i.e. make sure P(fj/ei) for all j is equal to 1 

  void readProbTable(const char *filename); 
  //  void readAsFertilityTable(const char *filename);
};
/*--------------- End of Class Definition for tmodel -----------------------*/ 

#endif

#endif
