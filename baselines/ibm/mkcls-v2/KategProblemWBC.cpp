/*

Copyright (C) 1997,1998,1999,2000,2001  Franz Josef Och

mkcls - a program for making word classes .

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




#include <stdlib.h>
#include "KategProblem.h"

static int oneFreqCompareSteigend(const void *p,const void *j)
{
#ifdef FREQTYPE_DOUBLE
  if( (((OneFreq *)p)->n < ((OneFreq *)j)->n) )
    return -1;
  if( (((OneFreq *)p)->n > ((OneFreq *)j)->n) )
    return +1;
  else
    return 0;
#else
  return ((OneFreq *)p)->n - ((OneFreq *)j)->n;
#endif
}
static int oneFreqCompareFallend(const void *p,const void *j)
{
#ifdef FREQTYPE_DOUBLE
  if( (((OneFreq *)p)->n > ((OneFreq *)j)->n) )
    return -1;
  if( (((OneFreq *)p)->n < ((OneFreq *)j)->n) )
    return +1;
  else
    return 0;
#else
  return -((OneFreq *)p)->n + ((OneFreq *)j)->n;
#endif
}


KategProblemWBC::KategProblemWBC(int n,int minw) 
: _n1(n,0),_n2(n,0),with_h_of_words(0),afterFilled(n,0),beforeFilled(n,0),filled(0),fixedWord(n,-1),absteigend(0),nWords(n),nTranspWords(0),
  mindestAnzahl(minw),after(n),before(n),minIndex(n,-1),maxIndex(n,-1)
  
{
}

KategProblemWBC::~KategProblemWBC()
  
{
  massert( after.size()==nWords);
  if( absteigend )
    delete absteigend;
}

void KategProblemWBC::init(int specialFixedWord)
{
  
  nTranspWords=0;
  int i;
  for(i=0;i<_n1.size();i++)
    {
      if( (_n1[i]<mindestAnzahl && _n2[i]<mindestAnzahl && minIndex[i]<=1) ||i==specialFixedWord )
	{
	  
	  if(!( fixedWord[i]==1 || fixedWord[i]== -1))
	    cerr << "mkcls:KategProblemWBC::init::ERROR: " << i << " " << fixedWord[i] << endl;
	  fixedWord[i]=1;
	}
      else if(fixedWord[i]<0)
	nTranspWords++;
    }
  if( absteigend==0 )
    absteigend= &(getSortedList(0));
  
  
  
  
  
  if(verboseMode && nTranspWords!=_n1.size()-1 )
    cout << "Es sind: " <<nTranspWords<<" transportierbar.\n";
}

void KategProblemWBC::set_h_of_words(double s)
  
{
  with_h_of_words=1;
  h_of_words = -s;
}

double KategProblemWBC::get_h_of_words()
  
{
  if( with_h_of_words )
    return -h_of_words;
  else
    {
      h_of_words=0;
      for(int i=0;i<nWords;i++)
	h_of_words+=0.5*(kat_h(_n2[i])+kat_h(_n1[i]));
      with_h_of_words=1;
      return -h_of_words;
    }
}


void KategProblemWBC::setAfterWords(int w,int anzahl) 
  
{ 
  OneFreq o;
  o.w=-1;
  o.n=0;
  afterFilled[w]=0; 
  after[w].init(anzahl,o,1);
}
void KategProblemWBC::setBeforeWords(int w,int anzahl) 
  
{ 
  OneFreq o;
  o.w=-1;
  o.n=0;
  beforeFilled[w]=0;
  before[w].init(anzahl,o,1); 
}


void KategProblemWBC::setFreq(int w1,int w2,FreqType anzahl) 
  
{
  OneFreq o;
  o.n=anzahl;

  o.w=w2;
  after[w1][afterFilled[w1]++]=o;
  _n1[w1]+=anzahl;
  o.w=w1;
  before[w2][beforeFilled[w2]++]=o;
  _n2[w2]+=anzahl;
}

void KategProblemWBC::addFreq(int w1,int w2,FreqType anzahl) 
  
{
  OneFreq o;
  o.n=anzahl;
  int pos=-1,i;
  for(i=0;i<afterFilled[w1];i++)
    if(after[w1][i].w==w2)
      pos=i;

  if(pos==-1)
    {
      o.w=w2;
      after[w1][afterFilled[w1]++]=o;
    }
  else
      after[w1][pos].n+=anzahl;
  _n1[w1]+=anzahl;

  pos=-1;
  for(i=0;i<beforeFilled[w2];i++)
    if(before[w2][i].w==w1)
      pos=i;
  if(pos==-1)
    {
      o.w=w1;
      before[w2][beforeFilled[w2]++]=o;
    }
  else
    before[w2][pos].n+=anzahl;
  _n2[w2]+=anzahl;
}


short KategProblemWBC::testFull(int doIt)
  
{
  int enaNom=0;
  int afterFilledSum=0,beforeFilledSum=0;
  int ret=1,i;
  for(i=0;i<nWords;i++)
    {
      if( n1(i)==1 && n2(i)==1 )
	enaNom++;
      afterFilledSum+=afterFilled[i];
      beforeFilledSum+=beforeFilled[i];
      if(afterFilled[i]!=after[i].size())
	{
	  ret=0;
	  if( doIt )
	    after[i].resize(afterFilled[i]);
	}
      if(beforeFilled[i]!=before[i].size())
	{
	  ret=0;
	  if( doIt )
	    before[i].resize(beforeFilled[i]);
	}
      
    }
  if( ret==0 && !doIt )
    {
      cerr << "Error: Unfilled word bigram statistics.\n";
      exit(1);
    }
  else
    filled=1;
  if( verboseMode>1 )
    {
      cout << "MEAN(|L(w)|+|R(w)|)=" << (beforeFilledSum/(float)nWords)
	+(afterFilledSum/(float)nWords) << endl;
      cout << "Hapaslegomena: " << enaNom << endl;
    }
  int symmetrisch=1;
  for(i=0;i<nWords;i++)
    {
		int j;
      massert(before[i].size()==beforeFilled[i]);
      massert( after[i].size()== afterFilled[i]);
      FreqType sum=0;
      for(j=0;j<after[i].size();j++)
	sum+=after[i][j].n;
      massert( sum==_n1[i] );
      sum=0;
      for(j=0;j<before[i].size();j++)
	sum+=before[i][j].n;
      massert(sum==_n2[i]);
      if(_n1[i]!=_n2[i])
	{
	  symmetrisch=0;
	  if( verboseMode>1 )
	    cout << "Asymmetrie: " << i << " " << _n1[i] << " " << _n2[i] << endl;
	}
      
    }
  if(verboseMode && symmetrisch==0)
    cout << "Warning: word bigram statistic is not symmetric " 
            "(this is possibly an error)\n";
  return ret;
}

Array<Word> &KategProblemWBC::getSortedList(int steigend)
  
{
  int siz=_n2.size(),i;
  massert(filled);
  Array<Word> &sortedList =*new Array<Word>(siz);
  Array<OneFreq> list(siz);
  int pos=0;
  for(i=0;i<siz;i++)
    {
      if( fixedWord[i]<0 )
	{
	  list[pos].w=i;
	  list[pos].n=_n1[i];
	  pos++;
	}
    }
  int anzFree=pos;
  for(i=0;i<siz;i++)
    {
      if( fixedWord[i]>=0 )
	{
	  list[pos].w=i;
	  list[pos].n=_n1[i];
	  pos++;
	}
    }
  massert(pos==siz);
  if(steigend )
    qsort(list.getPointerToData(),anzFree,sizeof(OneFreq),oneFreqCompareSteigend);
  else
    qsort(list.getPointerToData(),anzFree,sizeof(OneFreq),oneFreqCompareFallend);
  massert( anzFree<=list.size() );

  for(i=0;i<siz;i++)
    {
      sortedList[i]=list[i].w;
      massert(steigend || i==0 || i>=anzFree || list[i-1].n>=list[i].n );
      massert((!steigend) || i==0 || i>=anzFree || list[i-1].n<=list[i].n );
    }
  return sortedList;
}

FreqType KategProblemWBC::numberOfWords()
  
{
  FreqType n1=0,n2=0;
  for(int i=0;i<_n1.size();i++)
    {
      n1+=_n1[i];
      n2+=_n2[i];
    }
  #ifndef FREQTYPE_DOUBLE
  massert(n1==n2);
  #endif
  return n1;
}

void KategProblemWBC::setDollar(int n)
  
{
  if( fixedWord[n]<0 )
    nTranspWords--;
  fixedWord[n]=0;
}

void KategProblemWBC::initializeIndex(const leda_array<string>&words,char firstChar,int unten,int oben,bool noHapas)
{
  int n=0;
  int i;
  massert(-1<unten);massert(unten<oben);
  if( verboseMode )
    cout << "InitializeIndex: " << firstChar << " u:" << unten << " o:" << oben << " " << noHapas << endl;
  over_array(words,i)
    {
      if( words[i][0]==firstChar && (noHapas || ((short)(n1(i)+0.0001))>=mindestAnzahl || ((short)(n2(i)+0.0001))>=mindestAnzahl) )
	{
	  minIndex[i]=unten;
	  maxIndex[i]=oben;
	  n++;  
	}
    }
  if( verboseMode )
    cout << "InitializeIndex gefunden fuer " << n << " Woerter.\n";
}

