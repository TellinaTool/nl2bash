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
#ifndef _ntables_h
#define _ntables_h 1
#include "Array2.h"
#include "Vector.h"
#include <cassert>
#include "defs.h"
#include "vocab.h"
#include "myassert.h"
#include "Globals.h"

extern double NTablesFactorGraphemes,NTablesFactorGeneral;

template <class VALTYPE>
class nmodel
{
 private:
  Array2<VALTYPE, Vector<VALTYPE> > ntab;
 public:
  nmodel(int maxw, int maxn)
    : ntab(maxw, maxn, 0.0)
    {}
  VALTYPE getValue(int w, unsigned int n)const
    {
      massert(w!=0);
      if(n>=ntab.getLen2())
	return 0.0;
      else
	return max(ntab(w, n), VALTYPE(PROB_SMOOTH));
    }
  VALTYPE&getRef(int w, int n)
    {
      //massert(w!=0);
      return ntab(w, n);
    }
  template<class COUNT>
  void normalize(nmodel<COUNT>&write,const Vector<WordEntry>* _evlist)const
{
  int h1=ntab.getLen1(), h2=ntab.getLen2();
  int nParams=0;
  if( _evlist&&(NTablesFactorGraphemes||NTablesFactorGeneral) )
    {
      size_t maxlen=0;
      const Vector<WordEntry>&evlist=*_evlist;
      for(unsigned int i=1;i<evlist.size();i++)
	maxlen=max(maxlen,evlist[i].word.length());
      Array2<COUNT,Vector<COUNT> > counts(maxlen+1,MAX_FERTILITY+1,0.0);
      Vector<COUNT> nprob_general(MAX_FERTILITY+1,0.0);
      for(unsigned int i=1;i<min((unsigned int)h1,(unsigned int)evlist.size());i++)
	{
	  int l=evlist[i].word.length();
	  for(int k=0;k<h2;k++)
	    {
	      counts(l,k)+=getValue(i,k);
	      nprob_general[k]+=getValue(i,k);
	    }
	}
      COUNT sum2=0; 
      for(unsigned int i=1;i<maxlen+1;i++)
	{
	  COUNT sum=0.0;
	  for(int k=0;k<h2;k++)
	    sum+=counts(i,k);
	  sum2+=sum;
	  if( sum )
	    {
	      double average=0.0;
	      //cerr << "l: " << i << " " << sum << " ";
	      for(int k=0;k<h2;k++)
		{
		  counts(i,k)/=sum;
		  //cerr << counts(i,k) << ' ';
		  average+=k*counts(i,k);
		}
	      //cerr << "avg: " << average << endl;
	      //cerr << '\n';
	    }
	}
      for(unsigned int k=0;k<nprob_general.size();k++)
	nprob_general[k]/=sum2;
      
      for(int i=1;i<h1;i++)
	{
	  int l=-1;
	  if((unsigned int)i<evlist.size())
	    l=evlist[i].word.length();
	  COUNT sum=0.0;
	  for(int k=0;k<h2;k++)
	    sum+=getValue(i, k)+((l==-1)?0.0:(counts(l,k)*NTablesFactorGraphemes)) + NTablesFactorGeneral*nprob_general[k];
	  assert(sum);
	  for(int k=0;k<h2;k++)
	    {
	      write.getRef(i, k)=(getValue(i, k)+((l==-1)?0.0:(counts(l,k)*NTablesFactorGraphemes)))/sum + NTablesFactorGeneral*nprob_general[k];
	      nParams++;
	    }
	}
    }
  else
    for(int i=1;i<h1;i++)
      {
	COUNT sum=0.0;
	for(int k=0;k<h2;k++)
	  sum+=getValue(i, k);
	assert(sum);
	for(int k=0;k<h2;k++)
	  {
	    write.getRef(i, k)=getValue(i, k)/sum;
	    nParams++;
	  }
      }
  cerr << "NTable contains " << nParams << " parameter.\n";
}

  void clear()
    {
      int h1=ntab.getLen1(), h2=ntab.getLen2();
      for(int i=0;i<h1;i++)for(int k=0;k<h2;k++)
	ntab(i, k)=0;
    }
  void printNTable(int noEW, const char* filename, const Vector<WordEntry>& evlist, bool) const;
  void readNTable(const char *filename);
  
};

#endif
