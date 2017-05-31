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






#ifndef KATEG_OPT_H
#define KATEG_OPT_H
#include <string>

#include <stdlib.h>
#include "Problem.h"

extern double rhoLo; 

typedef int Kategory;        
typedef int Word;



#ifdef FREQTYPE_DOUBLE
typedef double FreqType;
#else
typedef int FreqType;
#endif


#include "KategProblemWBC.h" 


#include "KategProblemKBC.h" 


enum { 
  INIT_RAN=1,
  INIT_AIO=2,
  INIT_LWRW=3,
  INIT_FREQ=4,
  INIT_OTHER=5
     };


enum { 
  W_RAN=(8|16),
  W_DET_DECR=(16),
  W_DET_INCR =(32)
};
#define CHOOSE_WORD (8|16|32)


enum {
  K_DET=(64),
  K_RAN=(128),
  K_BEST=(64|128)
};
#define CHOOSE_KAT (64|128)


enum {
  CRITERION_ML=0,
  CRITERION_LO=1,
  CRITERION_MY=2
};



class NWG
{
 private:
  Array<FreqType> freq;       

  Array<int> timeOfFreq; 
                         
                         
			 

  int curTime;           
 public:
  NWG(int n);            
  void init();           

  int anzNot0;           
                         

  Array<int> not0;       
                         
  int word;          

  inline void addFreq(int C,FreqType n); 

  void sort();           
                         
  FreqType getFreq(int i)     
    {
      if( timeOfFreq[i]==curTime )
	return freq[i];
      else
	return 0;
    };
};

inline void NWG::addFreq(int g,FreqType n)
{
  if(timeOfFreq[g]==curTime)
    freq[g]+=n;
  else
    {
      timeOfFreq[g]=curTime;
      freq[g]=n;
      not0[anzNot0++]=g;
    }
}



struct KategProblemChange : public ProblemChange
{
  void *operator new(size_t size);
  void operator delete(void *ptr,size_t size);

  int word;     
  int toKat;    
  int fromKat;  
};

class KategProblem : public Problem
{
 private:
  double kat_h_full(int n);
  double kat_h_full(double n);
  double kat_h_part(int n);
  double kat_h_part(double n);
  double sigmaVerfaelschung;
  short katWasEmpty;
                    
		    

  int nwgWord;
              
  NWG nwg; 
  NWG ngw; 
  FreqType nww; 

  int ursprung,ziel;    
 
  Array<int> _katOfWord; 

  int _maxComp,_maxCompVal;

   double nmo_my(int i,int j);                            
   double nmo(int i,int j);                            
      

  double nmo_lo(int i,int j,int &e0,int &e1); 
  

   void putWord(int word,int to);
  

   void fastPutWord(int word,int to);
  

   void setKatOfWord(int w,int k)
{
  if( !(wordFreq.fixedWord[w]==k||wordFreq.fixedWord[w]==-1||k==-1) )
    {
      cout << "mkcls::setKatOfWord::ERROR: " << w << " " << k << " " << wordFreq.fixedWord[w] << " " << (*words)[w] << endl;
    }
  _katOfWord[w]=k;
  nwgWord=-1;
};
  

   void fillNWG(int w);
  

   inline FreqType nstrich(int i,int j);
  

   void vnstrich(int i,int j);
  


 protected:
   virtual int _change(ProblemChange **p);
  

   virtual void _doChange(ProblemChange &c);
  

   virtual void _undoChange(ProblemChange &c);
  

   virtual double _value();
  

   double _valueChange(KategProblemChange &k);
  

   virtual void incrementDirection();
  

   virtual int maxDimensionVal(void) ;
  

   virtual int maxDimension(void) ;
  
  
public:
  leda_array<string> *words;
typedef leda_set<int> intSet;

leda_array<intSet> *kats;
	
  KategProblemWBC wordFreq;   
  KategProblemKBC katFreq;    

  Array<int> initLike; 
  
   KategProblem(int aw,int mak,int _initialisierung,int _auswertung,
                           int _nachbarschaft,int minw=0);
  

  virtual ~KategProblem();
  

   virtual void _initialize(int initTyp);
   virtual void _initialize(int initTyp,int specialFixedWord);
  

   virtual double valueChange(ProblemChange&c);
  

   virtual Problem *makeEqualProblem();
  

   virtual double nicevalue(double value=1e100);
  

   void makeKats();
  

   virtual void dumpOn(ostream &strm);
  

   virtual void dumpInfos(ostream &strm);
  

  
  
  
   inline void katwahl(int k);
  

   inline void wortwahl(int w);
  

  
  
  
   inline int katOfWord(int w);
  

   inline short wortwahl();
  

   inline short katwahl() ;
  

   virtual int maxNonBetterIterations();
  

   virtual int expectedNumberOfIterations();
  

   const char *getString(int i);
   string getTheString(int i);
  

 void makeTitle(char x[512]);


 void fixInitLike();

};

inline int KategProblem::katOfWord(int w){return _katOfWord[w];};
inline short KategProblem::wortwahl(){return nachbarschaft&CHOOSE_WORD;};
inline short KategProblem::katwahl() {return nachbarschaft&CHOOSE_KAT;};

inline void KategProblem::katwahl(int k) 
    { 
      nachbarschaft = (nachbarschaft&(~CHOOSE_KAT)) | k; 
      if(k==K_BEST)
	_maxCompVal=1;
      else
	_maxCompVal=katFreq.nKats-2;
    };

inline void KategProblem::wortwahl(int w) 
    { 
      nachbarschaft = (nachbarschaft&(~CHOOSE_WORD)) | w;
    };



inline FreqType KategProblem::nstrich(int i,int j)
{
  FreqType n=0;

  if( i==ursprung )
    n-=nwg.getFreq(j); 
  if( i==ziel )
    n+=nwg.getFreq(j);

  if( j==ursprung )
    n-=ngw.getFreq(i);
  if( j==ziel )
    n+=ngw.getFreq(i);

  if( i==ursprung && j==ursprung )
    n+=nww;
  if( i==ziel && j==ziel )
    n+=nww;

  if( i==ursprung && j==ziel )
    n-=nww;
  if( i==ziel && j==ursprung )
    n-=nww;
  
  return n;
}





#define MAX_H_TABLE 4000 
extern double h_table[],l_table[],hmy_table[],hmy_sigma;

 
inline double kat_mlog(double x)
{
  if(x<=1e-9)
    return 0;
  else
    return log(x);
}

 
inline double kat_mlog(int s)
{
  if(s<=0)
    return 0;
  else if( s<MAX_H_TABLE )
    {
      massert( s==0 || l_table[s]==log(s) );
      return l_table[s];
    }
  else 
    return log((double)(s));
}


 
inline double kat_hlo(int n)
{
  return n*kat_mlog(n-1);
}
 
inline double kat_hlo(double n)
{
  return n*kat_mlog(n-1);
}

 
inline double kat_h(int n)
{
  massert(n>=-1);
  if(n<=0)
    return 0;
  else
    if(n<MAX_H_TABLE)
      {
	massert(n==0||fabs(h_table[n]-n*log((double)n))<1e-8);
	return h_table[n];
      }
    else
      return n*log((double)(n));
}
inline double kat_h(double n)
{
  if(n<=1e-9)
    return 0;
  else
    return n*log(n);
}

 
inline double kat_etaFkt(int _e0,int e1,int immer0,int cats)
{
  int e0    = _e0 - immer0;
  int ePlus = cats*cats - _e0;
  if(cats*cats-e0>1)
    return e1*log( (ePlus-1.0)/(e0+1.0)*rhoLo );
  else
    return 0;
}

double mkat_h_full(int n,double tf);
double mkat_h_part(int n,double cf);

int Hash(const string& s);


#endif

