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
#include <stdio.h>
#include "KategProblem.h"
#include "KategProblemTest.h"

#include "ProblemTest.h"

extern double SigmaVerfaelschung;

double h_table[MAX_H_TABLE],l_table[MAX_H_TABLE],hmy_table[MAX_H_TABLE],hmy_sigma; 

double LWRW_Faktor=0.5; 

static int intcompare(const void *p,const void *j)
{
  return *(int *)p - *(int *)j;
}

KategProblem::KategProblem(int aw,int mak,int _initialisierung,int _auswertung,
	   int _nachbarschaft,int mindestAnzahl) 
: Problem(mak,aw,_initialisierung,_auswertung,_nachbarschaft),
  sigmaVerfaelschung(SigmaVerfaelschung),katWasEmpty(0),nwg(mak+2),ngw(mak+2),_katOfWord(aw,-1),words(0),kats(0),
  wordFreq(aw,mindestAnzahl),katFreq(mak+2,(_auswertung==CRITERION_MY)?SigmaVerfaelschung:0.0),
  initLike(aw,-1)
  
{
  if( auswertung == CRITERION_MY )
    cout << "Sigma-Verfaelschung: " << sigmaVerfaelschung << endl;
  _maxComp=aw;
  _maxCompVal=mak;
  massert(katFreq.nKats>0);
  massert(mak<=aw);

  
  for(int i=1;i<MAX_H_TABLE;i++)
    {
      h_table[i]=i*log((double)(i));
      l_table[i]=log((double)(i));
      hmy_table[i]=i*log(verfaelsche(i,sigmaVerfaelschung));
    }
  hmy_sigma=sigmaVerfaelschung;
  l_table[0]=h_table[0]=0;

  if( katwahl()==K_BEST ) 
    _maxCompVal=1;         
                          
}

KategProblem::~KategProblem()

{
  delete words;
  delete kats;
}

void KategProblem::_initialize(int initTyp)
{
  _initialize(initTyp,-1);
}

void KategProblem::_initialize(int initTyp,int specialFixedWord)
  
{
  massert(wordFreq.filled);
  initialisierung = initTyp; 
 	int i;
  
  for(i=0;i<katFreq.nKats;i++)   
    for(int j=0;j<katFreq.nKats;j++)
      katFreq.setN(i,j,0);

  
  
  
  for(i=0;i<wordFreq.nWords;i++)
    {
      setKatOfWord(i,-1);
      if( strcmp(getString(i),"$")==0||strcmp(getString(i),"1$")==0||strcmp(getString(i),"2$")==0||strcmp(getString(i),"3$")==0||strcmp(getString(i),"4$")==0 )
	wordFreq.setDollar(i);
    }
  wordFreq.init(specialFixedWord); 
  
  
  
  
  _maxComp=wordFreq.nTranspWords;
  
  switch(initTyp)
    {
    case INIT_OTHER:
      
      if(verboseMode>2)cout << "KategProblem::_initialize(INIT_OTHER)\n";
      for(i=0;i<wordFreq.nWords;i++)
	fastPutWord(i,initLike[i]);
      break;
    case INIT_RAN:
      
      if(verboseMode>2)cout << "KategProblem::_initialize(INIT_RAN)\n";
      for(i=0;i<wordFreq.nWords;i++)
	{
	  if( wordFreq.minIndex[i]>0 && wordFreq.maxIndex[i]>0 )
	    fastPutWord(i,wordFreq.minIndex[i]+randomInt(wordFreq.maxIndex[i]-wordFreq.minIndex[i]+1));
	  else
	    fastPutWord(i,2+randomInt(katFreq.nKats-2));
	}
      
      
      break;
    case INIT_AIO:
      
      if(verboseMode>2)cout << "KategProblem::_initialize(INIT_AIO)\n";
      for(i=0;i<wordFreq.nWords;i++)
	fastPutWord(i,2);
      break;
    case INIT_FREQ:
      
      if(verboseMode>2)cout << "KategProblem::_initialize(INIT_FREQ)\n";
      for(i=0;i<wordFreq.nWords;i++)
	{
	  int to=i+2;
	  if( to>=katFreq.nKats )
	    to=katFreq.nKats-1;
	  fastPutWord((*(wordFreq.absteigend))[i],to);
	}
      curComp=katFreq.nKats-2; 
      break;
    case INIT_LWRW:
      
      {
	Array<int> markList(wordFreq.nWords,1);
	int to=2;
	int i=0;
	if(verboseMode>2)cout << "KategProblem::_initialize(INIT_LWRW)\n";
	for(to=2;to<katFreq.nKats*LWRW_Faktor;to++)
	  {
	    int w=(*(wordFreq.absteigend))[to-2];
	    fastPutWord(w,to);
	    markList[w]=0;
	  }
	while(to<katFreq.nKats-1 && i<wordFreq.nWords)
	  {
	    int toFilled=0;
	    int word=(*(wordFreq.absteigend))[i];
	    if(i%2)
	      {
		ManyFreq &after=wordFreq.after[word];
		for(int j=0;j<after.size();j++)
		  {
		    int w=after[j].w;
		    if( markList[w] )
		      fastPutWord(w,to),toFilled++;
		    markList[w]=0;
		  }
	      }
	    else 
	      {
		ManyFreq &before=wordFreq.before[word];
		for(int j=0;j<before.size();j++)
		  {
		    int w=before[j].w;
		    if( markList[w] )
		      fastPutWord(w,to),toFilled++;
		    markList[w]=0;
		  }
	      }
	    i++;
	    if( toFilled>0 )
	      to++;
	  }
	for(i=0;i<wordFreq.nWords;i++)
	  if(markList[i])
	    fastPutWord(i,katFreq.nKats-1);
      }
      break;
    default:
      cerr << "Wrong _initialize in KategProblem: " << initTyp << endl;
      exit(1);
    }

  
  
  for(int word=0;word<wordFreq.nWords;word++)
    {
      Array<OneFreq>& aft=wordFreq.after[word];
      
      int nAft=aft.size();
      
      for(i=0;i<nAft;i++)
	katFreq.addN(katOfWord(word),katOfWord(aft[i].w),aft[i].n);
    }

  if(verboseMode>2)
    {
      cout << "\nInitialization of KategProblem:";
      dumpOn(cout);
    }
}

double KategProblem::valueChange(ProblemChange&c)
  
{
  numberOfPartEvaluations++;
  KategProblemChange &k=*(KategProblemChange *)&c;
  fillNWG(k.word);        
                          
  return _valueChange(k); 
}


Problem *KategProblem::makeEqualProblem()
  
{
  KategProblem*p = new KategProblem(wordFreq.nWords,katFreq.nKats-2,initialisierung,
                    auswertung,nachbarschaft);
  KategProblemWBC &w=p->wordFreq;
  for(int x=0;x<wordFreq.nWords;x++)
    {
      w.setAfterWords(x,wordFreq.after[x].size());
      w.setBeforeWords(x,wordFreq.before[x].size());
    }
	int i;
  for(i=0;i<wordFreq.nWords;i++)
    {
      for(int j=0;j<wordFreq.after[i].size();j++)
	w.setFreq(i,wordFreq.after[i][j].w,wordFreq.after[i][j].n);
    }  
  w.testFull();
  w.mindestAnzahl = wordFreq.mindestAnzahl;
  if(words)
    p->words = new leda_array<string>(*words);
  for(i=0;i<wordFreq.nWords;i++)
    {
      p->setKatOfWord(i,katOfWord(i));
      p->initLike[i]=initLike[i];
    }
  p->setValuesFrom(this);
  return p;
}

double KategProblem::nicevalue(double val)
  
{
  double v;
  if( val!=1e100)
    v=val;
  else
    v=value();
  double h=wordFreq.get_h_of_words();
  double n=wordFreq.numberOfWords();
  double k=0;
  if(auswertung == CRITERION_MY)
    k=katFreq.myCriterionTerm();
  return exp((v+h-k)/n);
}

void KategProblem::makeKats()
  
{
  if(kats)delete kats;
  kats = new leda_array<intSet>(katFreq.nKats);
  for(int i=0;i<wordFreq.nWords;i++)
    (*kats)[katOfWord(i)].insert(i);
}

void KategProblem::dumpInfos(ostream &strm)
  
{
  strm << ";KategProblem:";
  strm << "cats: " << katFreq.nKats-2 << "   words: " << wordFreq.nWords 
    << endl;
}

void KategProblem::dumpOn(ostream &strm)
  
{
  writeClasses(_katOfWord,*this,strm);
  if(PrintBestTo2)
    {
      dumpInfos(*PrintBestTo2);
      makeKats();
      if( kats==0 )
	{
	  if( words==0 )
	    {
	      for(int i=0;i<wordFreq.nWords;i++)
		{
		  *PrintBestTo2 << i << ":" << katOfWord(i) << " ";
		}
	    }
	  else
	    {
	      for(int i=0;i<wordFreq.nWords;i++)
			*PrintBestTo2 << (*words)[i] << ":" << katOfWord(i) << " ";
	    }      
	}
      else
	{
	  int anzkat=0;
	  for(int i=0;i<katFreq.nKats;i++)
	    {
	      int printed=0;
	      *PrintBestTo2  << i << ":";
	      leda_set<int>&theSet = (*kats)[i];
	      if( words==0 )
		{
		  int nr=0;
		  forall_set(leda_set<int>,nr,theSet)
		    {
		      *PrintBestTo2 << nr << ", ";
		      printed=1;
		    }
		}
	      else
		{
		  int nr=0;
		  forall_set(leda_set<int>,nr,theSet)
		    {
		      *PrintBestTo2 << (*words)[nr]<< ","; 
		      printed=1;
		    }
		}
	      if(printed==1)anzkat++;
	      *PrintBestTo2 << endl;
	    }
	  *PrintBestTo2 << ";I have " << anzkat << " categories used.\n";
	}
      *PrintBestTo2 << endl;
      Problem::dumpOn(*PrintBestTo2);
    }
}






const char *KategProblem::getString(int i)
  
{
  if(words==0)
    return "<>";
  else
    return ((*words)[i]).c_str();
}

string KategProblem::getTheString(int i)
{
  return (*words)[i];
}

int KategProblem::maxNonBetterIterations()
  
{
  if(katwahl()==K_BEST)
    return wordFreq.nTranspWords;
  else
    return katFreq.nKats*wordFreq.nTranspWords;
}

int KategProblem::expectedNumberOfIterations()

{
  
  if(katwahl()==K_BEST)
    return 10*wordFreq.nTranspWords;
  else
    return 13*katFreq.nKats*wordFreq.nTranspWords;
}

void KategProblem::makeTitle(char x[512])
  
{
  const char *ww;
  const char *kw;
  const char *in;
  switch(wortwahl())
    {
    case W_RAN:
      ww="zufaellig";
      break;
    case W_DET_DECR:
      ww="absteigend";
      break;
    case W_DET_INCR:
      ww="aufsteigend";
      break;
    default:
      cerr << "Error: unknown word selection\n";
      exit(1);
    }
  switch(katwahl())
    {
    case K_DET:
      kw="rotierend";
      break;
    case K_RAN:
      kw="zufaellig";
      break;
    case K_BEST:
      kw="best     ";
      break;
    default:
      cout << "Error: unknown cagegory selection\n";
      exit(1);
    }
  switch(initialisierung)
    {
    case INIT_RAN:
      in="zufaellig ";
      break;
    case INIT_AIO:
      in="all-in-one";
      break;
    case INIT_LWRW:
      in="lwrw      ";
      break;
    case INIT_FREQ:
      in="freq      ";
      break;
    case INIT_OTHER:
      in="other     ";
      break;
    default:
      cout << "Error: unknown initialization\n";
      exit(1);
    }
  sprintf(x,"(c:%d,w:%d(%d),ww:%s,kw:%s,in:%s)",katFreq.nKats,wordFreq.nWords,
	  wordFreq.nTranspWords,ww,kw,in);
}

  
  
  
int KategProblem::_change(ProblemChange **p)
  
{
  *p=0;
  int word=curDimension();
  switch( wortwahl() )
    {
    case W_RAN: 
      word=(*(wordFreq.absteigend))[randomInt(wordFreq.nTranspWords)];
      break;
    case W_DET_DECR: 
      word=(*(wordFreq.absteigend))[word];
      break;
    case W_DET_INCR: 
      word=(*(wordFreq.absteigend))[wordFreq.nTranspWords-word-1];
      break;
    default:
      cerr << "Error: Unknown word selection\n";
      exit(1);
    }

  int kat=curDimensionVal()+2; 
  switch( katwahl() )
    {
    case K_RAN: 
      kat=randomInt(katFreq.nKats-2)+2;
      
    case K_DET: 
      
      
      if( kat==katOfWord(word)||(katWasEmpty&&katFreq.n1(kat)==0) )
	return 0;  
      else if( wordFreq.minIndex[word]>0 && wordFreq.maxIndex[word]>0 && (kat<wordFreq.minIndex[word]||kat>wordFreq.maxIndex[word]))
	{
	  
	  return 0;
	}
      else
	{
	  KategProblemChange *c = new KategProblemChange;
	  c->toKat=kat;
	  c->word=word;
	  c->fromKat=katOfWord(c->word);
	  massert( c->toKat < katFreq.nKats );
	  massert( c->fromKat < katFreq.nKats );
	  massert( c->word < wordFreq.nWords );
	  massert( c->toKat!=0   && c->toKat!=1 );
	  massert( c->fromKat!=0 && c->fromKat!=1 );
	  if(katFreq.n1(kat)==0) 
	    katWasEmpty=1;       
	  *p=c;
	  return 1;
	}
      break;
    case K_BEST: 
      {
	fillNWG(word);
	double smallest=1e100;
	KategProblemChange &smallestChange = *new KategProblemChange;
	short withEmpty=0;
	
	
	int startKat=2;
	int endKat=katFreq.nKats;
	if( wordFreq.minIndex[word]>0&&wordFreq.maxIndex[word]>0 )
	  {
	    startKat = max(2,wordFreq.minIndex[word]);
	    endKat = min(katFreq.nKats,wordFreq.maxIndex[word]+1);
	  }
	for(kat=startKat;kat<endKat;kat++)
	  {
	    if( kat!=katOfWord(word) && (withEmpty==0 || katFreq.n1(kat) 
					 || katFreq.n2(kat)) )
	      {
		KategProblemChange c;
		c.toKat=kat;
		c.word=word;
		c.fromKat=katOfWord(word);
		double n=_valueChange(c);
		if(n<smallest)
		  {
		    smallest=n;
		    smallestChange=c;
		  }
	      }
	    if( katFreq.n1(kat)==0 && katFreq.n2(kat)==0 )
	      withEmpty=1;
	  }
	massert(smallest!=1e100);
	*p= &smallestChange;
	return 1;
      }
      break;
    default:
      cerr << "Error: Unknown category selection\n";
      exit(1);
      return 0;
    }
}

void KategProblem::_doChange(ProblemChange &c)
  
{
  KategProblemChange &k=*(KategProblemChange *)&c;
  putWord(k.word,k.toKat);
  
}

void KategProblem::_undoChange(ProblemChange &c)
  
{
  KategProblemChange &k=*(KategProblemChange *)&c;
  putWord(k.word,k.fromKat);
  
}

void KategProblem::incrementDirection()
  
{
  Problem::incrementDirection();
  katWasEmpty=0; 
  massert( _maxComp==wordFreq.nTranspWords );
}

double KategProblem::_value()
  
{
  
  return katFreq.fullBewertung(auswertung);
}


double mkat_h_full(int n,double tf)
{
  
  
  if( tf>0 )
    return n*log(tf);
  else 
    return 0.0;
}

double mkat_h_part(int n,double cf)
{
  
  
  if( cf>0.0 )
    return n*log(cf);
  else
    return 0.0;
}

double KategProblem::kat_h_full(int n)
{
  return mkat_h_full(n,verfaelsche(n,sigmaVerfaelschung));
}
double KategProblem::kat_h_full(double n)
{
  abort();
  return mkat_h_full((int)n,verfaelsche(n,sigmaVerfaelschung));
}

double KategProblem::kat_h_part(int n)
{
  return mkat_h_part(n,verfaelsche(n,sigmaVerfaelschung));
}
double KategProblem::kat_h_part(double n)
{
  abort();
  return mkat_h_part((int)n,verfaelsche(n,sigmaVerfaelschung));
}

  
  
  
double KategProblem::nmo_my(int i,int j)
  
{
  FreqType n=nstrich(i,j),k=katFreq.n(i,j);
  return kat_h_full(n+k)-kat_h_full(k);
}
double KategProblem::nmo(int i,int j)
  
{
  FreqType n=nstrich(i,j),k=katFreq.n(i,j);
  return kat_h(n+k)-kat_h(k);
}
double KategProblem::nmo_lo(int i,int j,int &e0,int &e1)
  
{
  FreqType kij=katFreq.n(i,j);
  FreqType nij=nstrich(i,j)+kij;
  if( kij!=nij)
    {
      if( nij==0 )
	e0++;
      else if(nij==1)
	e1++;
      if( kij==0 )
	e0--;
      else if(kij==1)
	e1--;
    }
  return nij*kat_mlog(nij-1-rhoLo)-kij*kat_mlog(kij-1-rhoLo);
}


double KategProblem::_valueChange(KategProblemChange &k)
  
{
  double v=0;
  int i=0;
  
  ursprung=k.fromKat;
  ziel=k.toKat;

  if( auswertung==CRITERION_LO )
    {
      int e0a=katFreq.eta0,e1a=katFreq.eta1;
      v-=nmo_lo(ursprung,ursprung,e0a,e1a)+nmo_lo(ziel,ziel,e0a,e1a)
	+nmo_lo(ursprung,ziel,e0a,e1a)+nmo_lo(ziel,ursprung,e0a,e1a);
      i=0;
      while(i<nwg.anzNot0)
	{
	  int cl=nwg.not0[i];
	  if( cl!= ursprung && cl!=ziel )
	    v -= nmo_lo(ursprung,cl,e0a,e1a)+nmo_lo(ziel,cl,e0a,e1a);
	  i++;
	}
      i=0;
      while(i<ngw.anzNot0)
	{
	  int cl=ngw.not0[i];
	  if( cl!= ursprung && cl!=ziel )
	    v -= nmo_lo(cl,ursprung,e0a,e1a)+nmo_lo(cl,ziel,e0a,e1a);
	  i++;
	}
      
      v+=kat_hlo(katFreq.n1(ursprung)-wordFreq.n1(k.word))
	-kat_hlo(katFreq.n1(ursprung))
	+kat_hlo(katFreq.n2(ursprung)-wordFreq.n2(k.word))
	-kat_hlo(katFreq.n2(ursprung))
        +kat_hlo(katFreq.n1(ziel)+wordFreq.n1(k.word))
	-kat_hlo(katFreq.n1(ziel))
	+kat_hlo(katFreq.n2(ziel)+wordFreq.n2(k.word))
	-kat_hlo(katFreq.n2(ziel));

      int old0=katFreq.c1_0*katFreq.nKats+katFreq.c2_0*katFreq.nKats
	      -katFreq.c1_0*katFreq.c2_0;
      int nc1_0=katFreq.c1_0,nc2_0=katFreq.c2_0;
      if( wordFreq.n1(k.word)>0 && katFreq.n1(ursprung)==wordFreq.n1(k.word) ) 
	nc1_0++;
      if( wordFreq.n2(k.word)>0 && katFreq.n2(ursprung)==wordFreq.n2(k.word) ) 
	nc2_0++;
      if( wordFreq.n1(k.word)>0 && katFreq.n1(ziel)==0 ) nc1_0--;
      if( wordFreq.n2(k.word)>0 && katFreq.n2(ziel)==0 ) nc2_0--;
      int new0=nc1_0*katFreq.nKats+nc2_0*katFreq.nKats-nc1_0*nc2_0;
      v-=kat_etaFkt(e0a,e1a,new0,katFreq.nKats)
	-kat_etaFkt(katFreq.eta0,katFreq.eta1,old0,katFreq.nKats);
      vassert(NULLFLOAT(Problem::valueChange(k)-v));
    }
  else if(auswertung==CRITERION_ML)
    {
      v-=nmo(ursprung,ursprung)+nmo(ziel,ziel)
	+nmo(ursprung,ziel)+nmo(ziel,ursprung);
      i=0;
      while(i<nwg.anzNot0)
	{
	  int cl=nwg.not0[i];
	  if( cl!= ursprung && cl!=ziel )
	      v -= nmo(ursprung,cl)+nmo(ziel,cl);
	  i++;
	}
      i=0;
      while(i<ngw.anzNot0)
	{
	  int cl=ngw.not0[i];
	  if( cl!= ursprung && cl!=ziel )
	    v -= nmo(cl,ursprung)+nmo(cl,ziel);
	  i++;
	}
      v+=kat_h(katFreq.n1(ursprung)-wordFreq.n1(k.word))
	-kat_h(katFreq.n1(ursprung))
        +kat_h(katFreq.n2(ursprung)-wordFreq.n2(k.word))
	-kat_h(katFreq.n2(ursprung))
	+kat_h(katFreq.n1(ziel)+wordFreq.n1(k.word))
        -kat_h(katFreq.n1(ziel))
	+kat_h(katFreq.n2(ziel)+wordFreq.n2(k.word))
        -kat_h(katFreq.n2(ziel));
    }
  else if( auswertung==CRITERION_MY )
    {
      v-=nmo_my(ursprung,ursprung)+nmo_my(ziel,ziel)
	+nmo_my(ursprung,ziel)+nmo_my(ziel,ursprung);
      i=0;
      while(i<nwg.anzNot0)
	{
	  int cl=nwg.not0[i];
	  if( cl!= ursprung && cl!=ziel )
	      v -= nmo_my(ursprung,cl)+nmo_my(ziel,cl);
	  i++;
	}
      i=0;
      while(i<ngw.anzNot0)
	{
	  int cl=ngw.not0[i];
	  if( cl!= ursprung && cl!=ziel )
	    v -= nmo_my(cl,ursprung)+nmo_my(cl,ziel);
	  i++;
	}
      v+=kat_h_part(katFreq.n1(ursprung)-wordFreq.n1(k.word))
	-kat_h_part(katFreq.n1(ursprung))
        +kat_h_part(katFreq.n2(ursprung)-wordFreq.n2(k.word))
	-kat_h_part(katFreq.n2(ursprung))
	+kat_h_part(katFreq.n1(ziel)+wordFreq.n1(k.word))
        -kat_h_part(katFreq.n1(ziel))
	+kat_h_part(katFreq.n2(ziel)+wordFreq.n2(k.word))
        -kat_h_part(katFreq.n2(ziel));
      double bishZusatz = katFreq.myCriterionTerm();
      _doChange(k);
      double neuZusatz = katFreq.myCriterionTerm();
      _undoChange(k);
      if(verboseMode>2)
	cout << "ZUSATZ: " << bishZusatz << " " << neuZusatz << " " <<neuZusatz-bishZusatz<<"  " << v <<  endl;
      v+=neuZusatz-bishZusatz;
    }
  else
    {
      cerr << "Fatal error: Unknown criterion: '"<<auswertung<<"'\n";
    }
  vassert( NULLFLOAT(Problem::valueChange(k)-v) );
  return v;
}


void KategProblem::fillNWG(int w)
  
{
  if(nwgWord==w)
    return; 
  else
    {
      Array<OneFreq> &after=wordFreq.after[w];
      int size=after.size(),i;
      nww=0;
      nwg.init();
      for(i=0;i<size;i++)
	{
	  nwg.addFreq(katOfWord(after[i].w),after[i].n);
	  if(after[i].w==w)
	    nww=after[i].n;
	}

      Array<OneFreq> &before=wordFreq.before[w];
      size=before.size();
      ngw.init();
      for(i=0;i<size;i++)
	ngw.addFreq(katOfWord(before[i].w),before[i].n);
      nwgWord=w;
    }
}

void KategProblem::vnstrich(int i,int j)
  
{
  cout << ".) " << katFreq.n(i,j) << " ";
  if( i==ursprung )
    cout << "a) "<<-nwg.getFreq(j) << " ";
  if( i==ziel )
    cout << "b) " <<nwg.getFreq(j) << " ";
  
  if( j==ursprung )
    cout << "c) " <<-ngw.getFreq(i) << " ";
  if( j==ziel )
    cout << "d) " <<+ngw.getFreq(i) << " " ;
  
  if( i==ursprung && j==ursprung )
    cout << "e) " <<+nww << " ";
  if( i==ziel && j==ziel )
    cout << "f) " <<+nww << " " ;
  if( i==ursprung && j==ziel )
    cout << "g) " <<-nww << " ";
  if( i==ziel && j==ursprung )
    cout << "h) " <<-nww << " ";
}





void KategProblem::fastPutWord(int word,int toKat)
  
{
  massert(toKat>=0 && toKat<katFreq.nKats);
  
  
  
  if( wordFreq.fixedWord[word]>=0 )
    toKat=wordFreq.fixedWord[word]; 
  massert(katOfWord(word)==-1);
  setKatOfWord(word,toKat);
}

void KategProblem::fixInitLike()
{
  int fixed=0,fixed2=0;
  over_arr(initLike,i)
    if(initLike[i]>=0 )
      {
	fixed++;
	if( initLike[i]>=wordFreq.minIndex[i] || initLike[i]==1 )
	  wordFreq.fixedWord[i]=initLike[i];
	else
	  {
	    wordFreq.fixedWord[i]=wordFreq.minIndex[i]+initLike[i]-2;
	    fixed2++;
	  }
	initLike[i]=-1;
      }
  cout << "Fixed from file are: " << fixed << " " << fixed2 << " words.\n";
}

void KategProblem::putWord(int word,int toKat)
  
{
  massert(toKat!=0);massert(toKat!=1);
  massert(word<wordFreq.nWords);
  massert(toKat<katFreq.nKats);
  massert(wordFreq.fixedWord[word]<0);
  int k=katOfWord(word);
  massert(k!=0&&k!=1);
  Array<OneFreq>& aft=wordFreq.after[word];
  Array<OneFreq>& bef=wordFreq.before[word];
  int nAft=aft.size();
  int nBef=bef.size();
  int i;
  if(verboseMode>4)
    cout << "putWord(" << word << "," << toKat << ")" << k << " nAft" 
      << nAft << " nBef" << nBef << " k" << k << "\n";

  massert( k!=-1 );  
  massert( k!=toKat );

  for(i=0;i<nAft;i++)
    {
      katFreq.addN(k,katOfWord(aft[i].w),-aft[i].n);
      if(verboseMode>4)
	cout << k << " " << katOfWord(aft[i].w) << " " << -aft[i].n << endl;
    }
  for(i=0;i<nBef;i++)
    if( bef[i].w!=word ) 
      {
	katFreq.addN(katOfWord(bef[i].w),k,-bef[i].n);
	if(verboseMode>4)
	  cout << katOfWord(bef[i].w) << " " << k << " " << -bef[i].n << endl;
      }
	  
  setKatOfWord(word,toKat);

  for(i=0;i<nAft;i++)
    katFreq.addN(toKat,katOfWord(aft[i].w),aft[i].n);
  for(i=0;i<nBef;i++)
    if( bef[i].w!=word ) 
      katFreq.addN(katOfWord(bef[i].w),toKat,bef[i].n);

}



  
  
  




static KategProblemChange theOneKategProblemChange; 
static int anzKategProblemChange=0;

void *KategProblemChange::operator new(size_t size)
{ 
  anzKategProblemChange++;
  massert(anzKategProblemChange>0);
  massert(anzKategProblemChange<2);
  if( anzKategProblemChange==1 )
    return &theOneKategProblemChange;
  else
    {
      if( verboseMode>1 )
	cout << "generate instance of KategProblemChange: " << size 
	  << " " << anzKategProblemChange<<  endl;
      return malloc(size); 
    }
}
void KategProblemChange::operator delete(void *ptr,size_t 
)
{ massert(size==sizeof(KategProblemChange));
  anzKategProblemChange--;
  if( ptr!= &theOneKategProblemChange)
    free(ptr);
}



  
  
  






NWG::NWG(int n) : freq(n,0),timeOfFreq(n,0),not0(n),word(-1)
{
  massert(n>0);
  curTime=1;
  init();
}

void NWG::init()
{
  curTime++;
  anzNot0=0;
}

void NWG::sort()
{
  qsort(not0.getPointerToData(),anzNot0,sizeof(int),intcompare);
  massert(anzNot0<=not0.size());
}


int KategProblem::maxDimension()
{
  return _maxComp;
}

int KategProblem::maxDimensionVal()
{
  return _maxCompVal;
}
	
