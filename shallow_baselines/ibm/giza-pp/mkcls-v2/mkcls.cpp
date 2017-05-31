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




#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <ctype.h>
#include "general.h"

#include "KategProblem.h"
#include "KategProblemTest.h"

#include "ProblemTest.h"
#include "TAOptimization.h"
#include "GDAOptimization.h"
#include "RRTOptimization.h"
#include "SAOptimization.h"
#include "HCOptimization.h"


double SigmaVerfaelschung=5.0;
int OneWithHapas=1;
char *hapaxInitName=0;




 
static int nLaeufe=1,nLaeufeReduce=3; 

  
static int optimizeParameterAnzahl=10;

 
static int IterOptVerf=TA_OPT;

 
static int MaxIterOptSteps= -1;

 
static int MaxSecs=0;




 
static int InitValue=INIT_RAN;

 
static int Criterion=CRITERION_ML;

 
static int Wwahl=W_DET_DECR;

 
static int Kwahl=K_BEST;

 
static int NumberCategories=100;

 
static int MinWordFrequency=0;

 
static int IterOptSet=0;

 
static KategProblem *p = 0;

 
char korpusName[1024]="train";
int korpusIsText=1;


char *FileForOther=0;

void printUsage(int r)
{
  cout << 
    "mkcls - a program for making word classes: Usage: \n"
    " mkcls [-nnum] [-ptrain] [-Vfile] opt\n"
    
    
    
    
    
    
    "-V output classes (Default: no file)\n"
    
    
    "-n number of optimization runs (Default: 1); larger number => better results\n"
    
    "-p filename of training corpus (Default: 'train')\n"
    
    
    
    
    
    
    
    
    "Example:\n"
    " mkcls -c80 -n10 -pin -Vout opt\n"
    " (generates 80 classes for the corpus 'in' and writes the classes in 'out')\n"
    "Literature: \n"
    " Franz Josef Och: »Maximum-Likelihood-Schätzung von Wortkategorien mit Verfahren\n"
    " der kombinatorischen Optimierung« Studienarbeit, Universität Erlangen-Nürnberg,\n"
    " Germany,1995. \n";
  exit(r);
}







void makeIterOpt()
{
  double maxTime=clockSec()+MaxSecs;
  if(MaxSecs==0)maxTime=0;
  double mean;
  StatVar end,laufzeit,init;
  solveProblem(1+(PrintBestTo!=0),*p,nLaeufe,MaxIterOptSteps,IterOptVerf,
	       mean,end,laufzeit,init,maxTime);
  if( verboseMode>1 )
    p->dumpOn(cout);
}



void makeIzrOpt()
{
  double maxTime=clockSec()+MaxSecs;
  if(MaxSecs==0)maxTime=0;
  izrOptimization(*p,nLaeufeReduce,nLaeufeReduce,0,maxTime,IterOptVerf);
}



int makeMetaOpt(int argc,char **argv)
{
  int ret=0;

  if(argc==4 || argc==3)
    {
      int typ=0;
      if( argc==4 )
	{
	  sscanf(argv[3],"%d",&typ);
	  assert(typ>0 && typ<=11 );
	}
      if( isdigit(argv[2][0]) )
	{
	  int a;
	  sscanf(argv[2],"%d",&a);
	  switch(a)
	    {
	    case 1: 
	      SAOptimization::optimizeValue(*p,nLaeufe,
					    optimizeParameterAnzahl,1);
	      break;
	    case 2: 
	      SAOptimization::optimizeValue(*p,nLaeufe,
					    optimizeParameterAnzahl,2);
	      break;
	    case 3: 
	      SAOptimization::optimizeValue(*p,nLaeufe,
					    optimizeParameterAnzahl,10);
	      break;
	    case 4: 
	      TAOptimization::optimizeValue(*p,nLaeufe,
					    optimizeParameterAnzahl,1);
	      break;
	    case 5: 
	      TAOptimization::optimizeValue(*p,nLaeufe,
					    optimizeParameterAnzahl,10);
	      break;
	    case 6: 
	      RRTOptimization::optimizeValue(*p,nLaeufe,
					     optimizeParameterAnzahl,1);
	      break;
	    case 7: 
	      RRTOptimization::optimizeValue(*p,nLaeufe,
					     optimizeParameterAnzahl,10);
	      break;
	    case 8: 
	      GDAOptimization::optimizeValue(*p,nLaeufe,
					     optimizeParameterAnzahl,1);
	      break;
	    default:
	      cerr << "Error: Wrong number of parameter (" << argv[2] 
		<< ").\n";
	      printUsage(1);
	    }
	}
      else
	{
	  if(strcasecmp(argv[2],"gda")==0)
	    {
	      GDAOptimization::optimizeValue(*p,nLaeufe,
					     optimizeParameterAnzahl,typ);
	    }
	  else if(strcasecmp(argv[2],"ta")==0)
	    {
	      TAOptimization::optimizeValue(*p,nLaeufe,
					    optimizeParameterAnzahl,typ);
	    }
	  else if(strcasecmp(argv[2],"rrt")==0)
	    {
	      RRTOptimization::optimizeValue(*p,nLaeufe,
					     optimizeParameterAnzahl,typ);
	    }
	  else if(strcasecmp(argv[2],"sa")==0)
	    {
	      SAOptimization::optimizeValue(*p,nLaeufe,
					    optimizeParameterAnzahl,typ);
	    }
	  
	  
	  
	  
	  else
	    {
	      cerr << "Error: unknown algorithm" << argv[2] << endl; 
	      printUsage(1);
	    }
	}
    }
  else
    {
      cerr << "Error: wrong number of arguments: " << argc << endl;
      printUsage(1);
    }
  return ret;
}










void setVerfahren(char *p)
{
  if(strcasecmp(p,"rrt")==0 )
    IterOptVerf=RRT_OPT;
  else if(strcasecmp(p,"ta")==0)
    IterOptVerf=TA_OPT;
  else if(strcasecmp(p,"gda")==0)
    IterOptVerf=GDA_OPT;
  else if(strcasecmp(p,"sa")==0)
    IterOptVerf=SA_OPT;
  else if(strcasecmp(p,"hc")==0)
    IterOptVerf=HC_OPT;
  else
    {
      cerr << "Error: Unknown iterativ-optimizing algorithm '" << p << "'.\n";
      printUsage(1);
    }
}



void setInitValue(char *iv,char *fileForOther)
{
  if(strcasecmp(iv,"ran")==0 )
    InitValue=INIT_RAN;
  else if(strcasecmp(iv,"aio")==0)
    InitValue=INIT_AIO;
  else if(strcasecmp(iv,"gda")==0)
    InitValue=INIT_LWRW;
  else if(strcasecmp(iv,"freq")==0)
    InitValue=INIT_FREQ;
  else if(strcasecmp(iv,"other")==0)
    {
      InitValue=INIT_OTHER;
      FileForOther=strdup(fileForOther);
    }
  else
    {
      cerr << "Error: Unknown initialization '" << p << "'.\n";;
      printUsage(1);
    }
}


void setWwahl(const char *ww)
{
  if(strcasecmp(ww,"ran")==0 )
    Wwahl=W_RAN;
  else if(strcasecmp(ww,"det")==0)
    Wwahl=W_DET_DECR;
  else if(strcasecmp(ww,"incr")==0)
    Wwahl=W_DET_INCR;
  else
    {
      cerr << "Error: Unknown word-selection '" << ww << "'.\n";;
      printUsage(1);
    }
}


void setKwahl(const char *kw)
{
  if( strcasecmp(kw,"det")==0 )
    Kwahl=K_DET;
  else if(strcasecmp(kw,"ran")==0 )
    Kwahl=K_RAN;
  else if(strcasecmp(kw,"best")==0)
    Kwahl=K_BEST;
  else
    {
      cerr << "Error: Unknown category-selection '" << kw << "'.\n";
      printUsage(1);
    }
}


void setParameter(const char *nr1,const char *nr2)
{
  int n1;
  float n2;
  sscanf(nr1,"%d",&n1);
  sscanf(nr2,"%f",&n2);
  IterOptSet=1;
  switch(n1)
    {
    case 1:
      SAOptimization::defaultAnfAnnRate=n2;
      if(verboseMode)cout << "Parameter gamma_0 (SA) set to " 
	<< SAOptimization::defaultAnfAnnRate << endl;
      iassert(0<=SAOptimization::defaultAnfAnnRate&& 
	      SAOptimization::defaultAnfAnnRate<=1);
      break;
    case 2:
      SAOptimization::defaultEndAnnRate=n2;
      if(verboseMode)cout << "Parameter gamma_e (SA) set to " 
	<< SAOptimization::defaultEndAnnRate << endl;
      iassert(0<=SAOptimization::defaultEndAnnRate
	      &&SAOptimization::defaultEndAnnRate<=1);
      break;
    case 3:
      SAOptimization::defaultMultiple=n2;
      if(verboseMode)cout << "Parameter nu_e (SA) set to " 
	<< SAOptimization::defaultMultiple << endl;
      iassert( SAOptimization::defaultMultiple>0 );
      break;
    case 4:
      TAOptimization::defaultAnnRate=n2;
      if(verboseMode)cout << "Parameter gamma_{TA} set to " 
	<< TAOptimization::defaultAnnRate << endl;
      iassert(0<=TAOptimization::defaultAnnRate 
	      &&TAOptimization::defaultAnnRate<=1);
      break;
    case 5:
      TAOptimization::defaultMultiple=n2;
      if(verboseMode)cout << "Parameter nu_{TA} set to " 
	<< TAOptimization::defaultMultiple << endl;
      iassert( TAOptimization::defaultMultiple>0 );
      break;
    case 6:
      RRTOptimization::defaultAnnRate=n2;
      if(verboseMode)cout << "Parameter gamma_{RRT} set to " 
	<< RRTOptimization::defaultAnnRate << endl;
      iassert(0<=RRTOptimization::defaultAnnRate 
	      && RRTOptimization::defaultAnnRate<=1);
      break;
    case 7:
      RRTOptimization::defaultMultiple=n2;
      if(verboseMode)cout << "Parameter nu_{RRT} set to " 
	<< RRTOptimization::defaultMultiple << endl;
      iassert( RRTOptimization::defaultMultiple>0 );
      break;
    case 8:
      GDAOptimization::defaultAlpha=n2;
      if(verboseMode)cout << "Parameter alpha set to " 
	<< GDAOptimization::defaultAlpha << endl;
      iassert(0<=GDAOptimization::defaultAlpha 
	      && GDAOptimization::defaultAlpha<1 );
      break;
    default:
      cerr << "Error: Wrong parameter number " << nr1 << " " << n1 << endl;
      printUsage(1);
    }
}



void setKorpusName(const char *s)
{
  strcpy(korpusName,s);
}

void setHapaxInitName(const char *s)
{
  hapaxInitName=strdup(s);
}

void setKorpus()
{
  if( korpusIsText )
    {
      if( (p=fromKModel(korpusName,NumberCategories,InitValue,Criterion,Wwahl|Kwahl,
			MinWordFrequency))==0)
	{
	  cerr << "Error: Could not read the file '" << korpusName << "'.\n";
	  printUsage(1);
	}
    }
  else
    {
      if( (p=fromNgrFile(korpusName,NumberCategories,InitValue,Criterion,Wwahl|Kwahl,
			 MinWordFrequency))==0)
	{
	  cerr << "Error: Could not read the file '" << korpusName << "'.\n";
	  printUsage(1);
	}
      p->wordFreq.initializeIndex(*(p->words),'1',2,1+NumberCategories/2,!OneWithHapas);
      p->wordFreq.initializeIndex(*(p->words),'2',2+NumberCategories/2,1+NumberCategories,OneWithHapas);
    }
  if( IterOptSet==0 ) 				
    KategProblemSetParameters(*p); 	
}






int main(int argc,char **argv)
{
  double startTime=clockSec();
  zufallSeed();
  while( argc>1 && argv[1][0]=='-' )
    {
      
      switch(argv[1][1])
	{
	case 'v': 
	  sscanf(argv[1]+2,"%d",&verboseMode);
	  iassert(verboseMode>=0);
	  break;
	case 'O':
	  sscanf(argv[1]+2,"%d",&OneWithHapas);
	  cout << "OneWithHapas: " << OneWithHapas << endl;
	  break;
	case 'n': 
	  sscanf(argv[1]+2,"%d",&nLaeufe);
	  nLaeufeReduce=nLaeufe;
	  iassert( nLaeufe>=1 );
	  break;
	case 'l': 
	  Criterion=1;
	  if( argv[1][2] )
	    {
	      sscanf(argv[1]+2,"%lf",&rhoLo);
	      if( verboseMode )
		cout << "Parameter rho (for LO) set to" << rhoLo << ".\n";
	      iassert(0<=rhoLo && rhoLo<=1);
	    }
	  if( verboseMode )
	    cout << "Criterion LO used.\n";
	  break;
	case 'y':
	  Criterion=2;
	  if( argv[1][2] )
	    {
	      sscanf(argv[1]+2,"%lf",&SigmaVerfaelschung);
	      if( verboseMode )
		cout << "Parameter rho (for LO) set to" << SigmaVerfaelschung << ".\n";
	      iassert(0<SigmaVerfaelschung);
	    }
	  if( verboseMode )
	    cout << "My special criterion used.\n";
	  break;
	case 'p': 
	  setKorpusName(argv[1]+2);
	  assert(argv[2]&&argv[2][0]!='-' || argv[2][0]!='i');
	  break;
	case 'P':
	  setKorpusName(argv[1]+2);
	  korpusIsText=0;
	  assert(argv[2]&&argv[2][0]!='-' || argv[2][0]!='i');
	  break;		
	case 'i': 
	  setInitValue(argv[1]+2,argv[2]);
	  if( InitValue==INIT_OTHER )
	    argv++,argc--;
	  break;
	case 'h':
	  setHapaxInitName(argv[1]+2);
	  break;
	case 'k': 
	  setKwahl(argv[1]+2);
	  break;
	case 'w': 
	  setWwahl(argv[1]+2);
	  break;
	case 'c': 
	  sscanf(argv[1]+2,"%d",&NumberCategories);
	  iassert(NumberCategories>=2);
	  break;
	case 'm': 
	  sscanf(argv[1]+2,"%d",&MinWordFrequency);
	  break;
	case 'e': 
	  setParameter(argv[1]+2,argv[2]);
	  argv++,argc--;
	  break;
	case 'a': 
	  setVerfahren(argv[1]+2);
	  break;
	case 'r': 
	  {
	    int s;
	    sscanf(argv[1]+2,"%d",&s);
	    zufallSeed(s);
	  }
	  break;
	case 'V': 
	  if(argv[1][2])
	    {
	      char str[1024];
	      strcpy(str,argv[1]+2);
	      PrintBestTo=new ofstream(str);
	      strcat(str,".cats");
	      PrintBestTo2=new ofstream(str);
	    }
	  else
	    cout << "AUSGABE auf cout\n";
	  break;
	case 'M': 
	  sscanf(argv[1]+2,"%d",&MaxIterOptSteps);
	  break;
	case 's': 
	  sscanf(argv[1]+2,"%d",&MaxSecs);
	  break;
	case 'N': 
	  sscanf(argv[1]+2,"%d",&optimizeParameterAnzahl); 
	  break;
	case 'o': 
	  GraphOutput = new ofstream(argv[1]+2);
	  if( GraphOutput==0 )
	    cerr << "Warning: Open failed for file '" << argv[1]+2 << "'.\n";
	  break;
    	default:
	  cerr << "Fehlerhafte Option: " << argv[1] << endl;
	  printUsage(1);
	}
      argv++;
      argc--;
    }

  
  setKorpus();
  if( FileForOther )
    {
      fromCatFile(p,FileForOther);
      p->initialisierung=InitValue;
      p->_initialize(InitValue);
    }
  
  if( hapaxInitName )
    {
      fromCatFile(p,hapaxInitName,0);
      p->fixInitLike();
    }

  double start2Time=clockSec(); 

  if(argc>=2 && strcasecmp(argv[1],"opt")==0 )
    makeIterOpt();
  else if(argc>=2 && strcasecmp(argv[1],"meta-opt")==0)
    makeMetaOpt(argc,argv);
  else if(argc>=2 && strcasecmp(argv[1],"izr-opt")==0)
    makeIzrOpt();
  
  
  else
    {
      makeIterOpt();
    }

  if( verboseMode )
    {
      cout << "    full-time: " << clockSec()-startTime << endl;
      cout << "optimize-time: " << clockSec()-start2Time << endl;
    }
  return 0;
}

