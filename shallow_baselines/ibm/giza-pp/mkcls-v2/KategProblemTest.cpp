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




#include "KategProblemTest.h"

#include "ProblemTest.h"
#include "HCOptimization.h"
#include "TAOptimization.h"
#include "RRTOptimization.h"
#include "GDAOptimization.h"

#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <sstream>

typedef pair<string,string> PSS;

#define NEW_SENTENCE_END "mkcls-mapped-dollar-symbol-$"

#ifdef NeXT
char *strdup(char *a)
{
  char *p = (char *)malloc(strlen(a)+1);
  strcpy(p,a);
  return p;
}

#endif


void writeClasses(Array<Kategory> &katOfWord,KategProblem &problem,ostream &to)
{	    
  for(int i=0;i<katOfWord.size();i++)
    {
      if( strcmp(problem.getString(i),"$") ) {
	if( strcmp(problem.getString(i),"mkcls-mapped-dollar-symbol-$")==0 )
	  to << "$" << "\t" << katOfWord[i] << endl;
	else
	  to << problem.getString(i) << "\t" << katOfWord[i] << endl;
      }
    }
}


void mysplit(const string &s,string &s1,string &s2)
{
  unsigned int i=0;
  for(;i<s.length();i++)if( s[i]==' ' || s[i]=='\t' || s[i]==' ')break;
  s1=s.substr(0,i);
  for(;i<s.length();i++)if( !(s[i]==' ' || s[i]=='\t' || s[i]==' ') )break;  
  s2=s.substr(i,s.length()-i);
  
  iassert(s1.size());
  iassert(s2.size());
}



int fromCatFile(KategProblem *p,const char *fname,bool verb)
{
  leda_h_array<string,int> translation(-1);
  int maxCat=2;
  ifstream in(fname);
  if(!in)
    {
      cerr << "Error: File '" << fname << "' cannot be opened.\n";
      exit(1);
    }
  for(int i=0;i<p->wordFreq.nWords;i++)
    (p->initLike)[i]= -1;
  
  
  translation["1"]=1;
  translation["0"]=0;

  
  string s;
  while( getline(in,s) ) 
    {
      string str,categ;
      mysplit(s,str,categ);
      int i=p->words->binary_locate(str);
      if(i>=0 && (*(p->words))[i]==str )
	{
	  
	  if( translation[categ]==-1 )
	    translation[categ]=maxCat++;
	  int cat=translation[categ];
	  if( (p->initLike)[i]!= -1 )
	    cerr << "Warning: Word '" << ((*(p->words))[i])<< "' is already in a category.\n";
	  (p->initLike)[i]=cat;
	}
      else
	cerr << "Warning: Word '" << str << "' " << i << " is not in training corpus.\n";
    }
  
  if( verboseMode )
    cout << "We have " << maxCat << " read non-empty categories" 
      " (with words from the corpus).\n";
  
  if(maxCat>p->katFreq.nKats)
    {
      cerr << "Error: Not enough categories reserved (only " 
	   << p->katFreq.nKats << ", but i need " << maxCat << ").\n";
      exit(1);
    }
  
  
  int i=p->words->binary_locate("$");
  if( i>=0 &&  (*(p->words))[i]=="$" )
    (p->initLike)[i]=0;
  else
    if( verboseMode )
      cerr << "Warning: No '$' in vocabulary!\n";
  
  
  int errors=0;
  for(i=0;i<p->wordFreq.nWords;i++)
    if((p->initLike)[i]== -1 )
      {
	if( verb ) cerr << "Error: I don't know the category of word " << i 
	     << " (" << (*(p->words))[i] << ") " << ".\n";
	errors=1;
      }
  return errors;
}



KategProblem *makeKategProblem(const leda_h_array<PSS,FreqType>&cTbl,const leda_set<string>&setVokabular, int maxClass,int initialisierung,
			 int auswertung,int nachbarschaft,int minWordFrequency)
{
  
  int nwrd=0;
  leda_array<string>&sVok = *new leda_array<string>(setVokabular.size());
  string s;
  unsigned int ctr=0;
  forall_set(leda_set<string>,s,setVokabular)
    {
      if( verboseMode>2 )
	cout << "mkcls:Wort " << ctr << " " << s << endl;
      sVok[ctr++]=s;
    }
  for(unsigned int z=0;z<ctr-1;z++)
    iassert( sVok[z]<sVok[z+1] );
  sVok.sort();

  if( verboseMode>2 )
    cout << "*****Vocabulary: " << sVok;
  
  unsigned int vokSize=sVok.size();
  massert(vokSize==ctr); massert(vokSize==setVokabular.size());
  if(verboseMode)
    {cout << "Size of vocabulary: " << vokSize << "\n";cout.flush();}
  
  KategProblem *k = new KategProblem(vokSize,maxClass,initialisierung,
				     auswertung,nachbarschaft,minWordFrequency);
  KategProblemWBC &w=k->wordFreq;
  k->words=&sVok;
  
  Array<int> after(vokSize,0);
  Array<int> before(vokSize,0);
  
  
  nwrd=0;
  {
    PSS s;
    forall_defined_h2(PSS,FreqType,s,cTbl)
      {
	const string&ss1=s.first;
	const string&ss2=s.second;
	if( ss2.length()&&(ss1!="$" || ss2!="$") )
	  {
	    int i1=sVok.binary_search(ss1);
	    int i2=sVok.binary_search(ss2);
	    iassert( sVok[i1] == ss1 );iassert( sVok[i2] == ss2 );
	    after[i1]++;
	    before[i2]++;
	  }
	if( verboseMode&&((nwrd++)%10000==0) ) 
	  {cout<<"Statistiken-1 " << nwrd<< ".      \r";cout.flush();}
      }
  }
  
  for(unsigned int i=0;i<vokSize;i++)
    {
      w.setAfterWords(i,after[i]);
      w.setBeforeWords(i,before[i]);
    }
  
  
  {
    nwrd=0;
    PSS s;
    forall_defined_h2(PSS,FreqType,s,cTbl)
      {
	const string&ss1=s.first;
	const string&ss2=s.second;
	FreqType p=cTbl[s];
	if( ss2.length()&&(ss1!="$" || ss2!="$") )
	  {
	    int i1=sVok.binary_search(ss1);
	    int i2=sVok.binary_search(ss2);
	    iassert( sVok[i1] == ss1 );iassert( sVok[i2] == ss2 );
	    w.setFreq(i1,i2,p);
	    if( verboseMode>2 )
	      cout << "BIGRAMM-HAEUF: " << ss1 << ":" << i1 << "   " 
		   << ss2 << ":" << i2 << "   " << p << endl;
	  }
 	if( verboseMode&&((nwrd++)%10000==0) ) 
	  {cout<<"Statistiken-2 " <<nwrd<< ".    \r";cout.flush();}
     }
  }
  
  w.testFull();
  if(verboseMode){cout << "Datenintegritaet getestet.\n";cout.flush();}
  return k;
}

KategProblem *fromNgrFile(const char *str,int maxClass,int initialisierung,
			 int auswertung,int nachbarschaft,int minWordFrequency)
{
  ifstream file(str);
  if(!file)return 0;
  leda_set<string> setVokabular;
  leda_h_array<PSS,FreqType> cTbl;
  double c=0;
  if( verboseMode )cout << "NGRFILE: " << str << endl;
  string s1,s2;
  while(file >> c >> s1 >> s2)
    {
      if( s1.length()==0||s2.length()==0 )
	{
	  cerr << "ERROR: strings are zero: " << s1.length() <<" " << s1 <<" " << s2.length()<<" " << s2 << endl;
	  return 0;
	}
      if( c==0 )
	{
	  cerr << "Count ist 0 " << s1 << " " << s2 << endl;
	  return 0;
	}
      cTbl[pair<string,string>(s1,s2)]=(FreqType)c;
      setVokabular.insert(s1);
      setVokabular.insert(s2);
      if( verboseMode>1 )
	cout << "R: " << s1 << " " << s2 << " " << c << endl;
      c=0;
    }
  
  return makeKategProblem(cTbl,setVokabular,maxClass,initialisierung,auswertung,nachbarschaft,minWordFrequency);
}



	

	


KategProblem *fromKModel(const char *str,int maxClass,int initialisierung,
			 int auswertung,int nachbarschaft,int minWordFrequency)
{
  string oldText,text,line;
  ifstream f(str);
  if( !f )
    {
      cerr << "ERROR: can not open file " << str << ".\n";
      return 0;
    }
  
  leda_set<string> setVokabular;
  leda_h_array<PSS,FreqType> cTbl(0);
  oldText="$";
  while(1)
    {
      getline(f,line);
      if(f.fail() && !f.bad() && !f.eof())
	{
	  cerr << "WARNING: strange characters in stream (getline) " << endl;f.clear();
	}
      if(!f)break;
      
      istringstream f2(line);
      while( 1 )
	{
	  f2 >> text;
	  if(f2.fail() && !f2.bad() && !f2.eof())
	    {
	      cerr << "WARNING: strange characters in stream (>>) !\n";
	      f2.clear(ios::failbit);
	    }
	  if(!f2){break;}
	  if( text == "$" )
	    text = "mkcls-mapped-dollar-symbol-$";
	  if( !setVokabular.member(text) )setVokabular.insert(text);
	  cTbl[pair<string,string>(oldText,text)]++;
	  oldText=text;
	}
      text="$";
      if( !setVokabular.member(text) )setVokabular.insert(text);
      cTbl[pair<string,string>(oldText,text)]++;
      oldText=text;
    }
  return makeKategProblem(cTbl,setVokabular,maxClass,initialisierung,auswertung,nachbarschaft,minWordFrequency);
}
 




void KategProblemSetParameters(KategProblem &p)
{
  if( p.katwahl()==K_BEST )
    {
      TAOptimization::defaultAnnRate=0.7;
      RRTOptimization::defaultAnnRate=0.95;
      GDAOptimization::defaultAlpha=0.05;
      if( verboseMode )
	cout << "Parameter-setting like W-DET-BEST\n";
    }
  else
    {
      TAOptimization::defaultAnnRate=0.4;
      RRTOptimization::defaultAnnRate=0.6;
      GDAOptimization::defaultAlpha=0.0125;
      if( verboseMode )
	cout << "Parameter-setting like W-DET-DET\n";
    }
}




KategProblem &makRandom(int ANZ_WORD,int ANZ_CLS,int initValue,
			int auswertung,int nachbarschaft,float relInit)
{
  KategProblem &k=
    *new KategProblem(ANZ_WORD,ANZ_CLS,initValue,auswertung,nachbarschaft);
  KategProblemWBC &w=k.wordFreq;
  Array<int> after(ANZ_WORD,0);
  Array<int> before(ANZ_WORD,0);
  Array<FreqArray> twoD(ANZ_WORD);
	int i;
  for(i=0;i<ANZ_WORD;i++) twoD[i].init(ANZ_WORD,0); 
  
  for(i=0;i<ANZ_WORD;i++)
    {
      massert(after[i]==0);
      massert(before[i]==0);
      for(int j=0;j<ANZ_WORD;j++)
	{
	  massert(twoD[i][j]==0);
	}
    }
  for(i=0;i<ANZ_WORD*ANZ_WORD*relInit;i++)
    {
      int x=randomInt(ANZ_WORD);
      int y=randomInt(ANZ_WORD);
      if(twoD[x][y]==0)
	{
	  after[x]++;
	  before[y]++;
	}
      twoD[x][y]+=randomInt(10)+1;
    }
  for(i=0;i<ANZ_WORD;i++)
    {
      w.setAfterWords(i,after[i]);
      w.setBeforeWords(i,before[i]);
    }
  
  for(i=0;i<ANZ_WORD;i++)
    {
      for(int j=0;j<ANZ_WORD;j++)
	if( twoD[i][j] )
	    w.setFreq(i,j,twoD[i][j]);
    }
  w.testFull();
  return k;
}




char *makeTitle(KategProblem &problem,int verfahren)
{
  char x[1024];
  switch(verfahren)
    {
    case HC_OPT:
      strcpy(x,"HC   ");
      break;
    case SA_OPT:
      strcpy(x,"SA     ");
      break;
    case TA_OPT:
      strcpy(x,"TA     ");
      break;
    case GDA_OPT:
      strcpy(x,"GDA    ");
      break;
    case RRT_OPT:
      strcpy(x,"RRT    ");
      break;
    }
  problem.makeTitle(x+strlen(x));
  return strdup(x);
}




#define MAX_MULTIPLE 10  

Array<KategProblem *> &_izrOptimization(Array<KategProblem *> &probs,
int anzprob,double timeForOneRed,double maxClock,Array<Kategory> &katOfWord,
int anzIter,int verfahren)
{
  massert(anzprob>1);
  massert(probs[0]->wordFreq.mindestAnzahl<=1);
  KategProblem *p0=probs[0];

  int nWords=p0->wordFreq.nWords;
  int nKats=p0->katFreq.nKats;
  int minimumNumberOfWords = max(1,int(nWords*0.95));

  int indexOfDurchschnitt;
  Array<int> newWords(nWords);
  int useAnzprob=anzprob;
  do
    {
      int w,k;
      indexOfDurchschnitt=0;
      for(w=0;w<nWords;w++)
	newWords[w]=-1;
      for(k=0;k<useAnzprob;k++)
	{
	  massert(probs[k]->wordFreq.nWords==nWords);
	  probs[k]->makeKats();
	}
      
      for(w=0;w<nWords;w++)
	{
	  if( newWords[w]==-1 )
	    {
	      
	      
	      
	      leda_set<int> durchschnitt=(*p0->kats)[p0->katOfWord(w)];
	      for(k=1;k<useAnzprob;k++)
	      durchschnitt = durchschnitt & (*probs[k]->kats)[probs[k]->katOfWord(w)];
	      
	      
	      int _anzInDurchschnitt=0;
	      int nr=0;
	      forall_set(leda_set<int>,nr,durchschnitt)
		{
		  _anzInDurchschnitt++;
		  newWords[nr]=indexOfDurchschnitt;
		}
	      if( verboseMode && _anzInDurchschnitt>1 && anzIter==0 )
		{
		  cout << "- (";
		    forall_set(leda_set<int>,nr,durchschnitt)
		    {
		      cout << p0->getString(nr);
		      if( p0->wordFreq.n1(nr)==1 )
			cout << "* ";
		      else
			cout << " ";
		    }
		  cout << ")\n";
		}
	      
	      
	      
	      
	      for(k=0;k<useAnzprob;k++)
		{
		  durchschnitt = durchschnitt - (*probs[k]->kats)[probs[k]->katOfWord(w)];
		}
	      indexOfDurchschnitt++;
	    }
	}
      
    if(indexOfDurchschnitt>=minimumNumberOfWords)
	{
	  if(useAnzprob==1)
	    {
	      cout << "useAnzProb==1 => mysterious.\n";
	      break;	
	    }
	  useAnzprob--;
	}
    }
  while(indexOfDurchschnitt>=minimumNumberOfWords);
  
  
  Array<KategProblem *> &neu=*new Array<KategProblem *>(MAX_MULTIPLE*anzprob,(KategProblem *)0);
  qsort(probs.getPointerToData(),useAnzprob,sizeof(KategProblem *),compareProblem);
  massert(useAnzprob<=probs.size());
  double startTime=clockSec();
  int i, numberOfNew;
  for(numberOfNew=0; (clockSec()-startTime<timeForOneRed) 
                         || (numberOfNew < anzprob) ; numberOfNew++)
    {
      int w;
      if( numberOfNew==anzprob*MAX_MULTIPLE-1 )
	break;
      KategProblem *p 
	= neu[numberOfNew] 
	  = new KategProblem(indexOfDurchschnitt,nKats-2,
		          p0->initialisierung,p0->auswertung,p0->nachbarschaft);

      for(w=0;w<indexOfDurchschnitt;w++)
	{
	  p->wordFreq.setAfterWords(w,5);
	  p->wordFreq.setBeforeWords(w,5);
	}
      for(w=0;w<nWords;w++)
	{
	  Array<OneFreq> &after=p0->wordFreq.after[w];
	  int size=after.size();
	  for(i=0;i<size;i++)
	    p->wordFreq.addFreq(newWords[w],newWords[after[i].w],after[i].n);
	}
      p->wordFreq.testFull(1);
      
      
      
      
      
      
      p->wordFreq.set_h_of_words(p0->wordFreq.get_h_of_words());
      double w1=0.0,w2=0.0;
      if(numberOfNew<useAnzprob)
	{
	  
	  for(i=0;i<nWords;i++)
	    (p->initLike)[newWords[i]]=probs[numberOfNew]->katOfWord(i);
	  p->_initialize(5);
	  HCOptimization hc(*p,-1);
	  if(verboseMode)
	    {
	      w1=p->nicevalue();
	      cout << "from old category system:" << w1 << endl;
	    }
	  hc.minimize(-1);
	  if(verboseMode)
	    {
	      w2=p->nicevalue();
	      if(w2<w1)
		cout << "improvement: " << w1-w2 << endl;
	    }
	}
      else
	{
	  p->_initialize(1);
	  double mean;
	  StatVar end,laufzeit,start;
	  solveProblem(0,*p,1,-1,verfahren,mean,end,laufzeit,start);
	  w2=p->value();
	  if(verboseMode)
	      cout << "new category system: " << w2 << " (" << p->nicevalue() 
		<< ") Zeit: " << clockSec() << "\n";
	}
    }
	int p;
  for(p=0;p<probs.size();p++)
    {
      if( probs[p] )
	delete probs[p];
    }
  qsort(neu.getPointerToData(),numberOfNew,sizeof(Problem *),compareProblem);
  massert(numberOfNew<=neu.size());
  if( verboseMode )
    cout << "Iterierte Zustandsraum-Reduktion: " << indexOfDurchschnitt 
      << " words. costs: " << neu[0]->value() << " " 
      << neu[0]->nicevalue() << " (" << numberOfNew-anzprob << ")" << "time: " 
      << clockSec() << endl;
  if( indexOfDurchschnitt<=nKats 
      || (clockSec()>maxClock&&maxClock) )
    {
      if( clockSec()>maxClock&&maxClock )
	cout << "STOP (time limit: " << (clockSec()-maxClock) << " s)\n";
      for(i=0;i<nWords;i++)
	katOfWord[i]=neu[0]->katOfWord(newWords[i]);
      return neu;
    }
  else
    {
      Array<Kategory> &newKatOfWord=
       *(new Array<Kategory>(neu[0]->wordFreq.nWords,-1));
      Array<KategProblem *> &erg=_izrOptimization(neu,anzprob,timeForOneRed,
						  maxClock,newKatOfWord,
						  anzIter+1,verfahren);
      for(i=0;i<nWords;i++)
	katOfWord[i]=newKatOfWord[newWords[i]];
      return erg;
    }
}




KategProblem *izrOptimization(KategProblem &p,int minN,int firstN,
			      double clockForOneRed,double maxClock,int verfahren)
{
  Array<Kategory> katOfWord(p.wordFreq.nWords,-1);
  int startN;
  if( clockForOneRed<=0 )
    startN=firstN;
  else
    startN=1000;
  Array<KategProblem *> probs(startN);
  double val1=0.0,val2=0.0;
  double endTime=-1;

  double startTime=clockSec();
  int i;
  for(i=0;i<startN;i++)
    {
      StatVar end,laufzeit,start;
      double mean;
      probs[i] = (KategProblem *)((KategProblem *)p.makeEqualProblem());
      solveProblem(0,*(probs[i]),1,-1,verfahren,mean,end,laufzeit,start);
      if( i==minN-1 )
	endTime = clockSec();
      if( i>=firstN-1 && (startTime+clockForOneRed>clockSec() || i==999) )
	break;
    }
  if( endTime<0 )
    endTime=clockSec();
  massert(i>=firstN);

  qsort(probs.getPointerToData(),i,sizeof(KategProblem *),compareProblem);
  massert(i<=probs.size());
  if( clockForOneRed<=0 )
    {
      clockForOneRed=endTime-startTime;
      if( verboseMode )
	cout << "time for one reduction: " << clockForOneRed << endl;
    }
  _izrOptimization(probs,minN,clockForOneRed,maxClock,katOfWord,0,verfahren);
  
  KategProblem *n=(KategProblem *)(p.makeEqualProblem());
  n->initLike= katOfWord;
  n->_initialize(5);
  if( verboseMode )
    val1=n->value();
  HCOptimization hc(*n,-1);
  hc.minimize(-1);
  val2=n->value();
  if( verboseMode )
    cout << "last improvement: " << val2-val1 << "\n";
  cout << "final costs: " << val2 << " " << n->nicevalue() << endl;
  if(PrintBestTo)
    n->dumpOn(*PrintBestTo);
  return n;
}











