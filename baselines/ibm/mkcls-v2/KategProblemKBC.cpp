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

double rhoLo=0.75; 
#define MAX_VERFAELSCHUNG 5000
double verfTab[MAX_VERFAELSCHUNG],verfTabSigma=-1.0;
double verfaelsche(int a,double b)
{
  
  if( a>=0&&verfTabSigma==b&&a<MAX_VERFAELSCHUNG )
    {
      massert(verfTab[a]== b*(erf(10000.0) - erf(a/b))/2+a);
      return verfTab[a];
    }
  else
    {
      double x = b*(erf(10000.0) - erf(a/b))/2+a;
      return x;
    }
}
double verfaelsche(double,double b)
{
  abort();
  return b;
}

KategProblemKBC::KategProblemKBC(int s,double sv) : 
  _n(s),_n1(s,0),_n2(s,0),sigmaVerfaelschung(sv),withVerfaelschung(sv!=0.0),
  _nverf(s),_n1verf(s,0.0),_n2verf(s,0.0),_nWords(0),
  eta0(s*s),eta1(0),c1_0(s),c2_0(s),
  _bigramVerfSum(0.0),_unigramVerfSum1(0.0),_unigramVerfSum2(0.0),nKats(s)
  
{ 
  verfInit0=0.0;
  int i;
  if( withVerfaelschung )
    {
      verfInit0=verfaelsche(0,sv);
      cout << "VERFAELSCHUNG wird mitgefuehrt => LANGSAMER!!!\n";
    }
  for(i=0;i<s;i++)
    {
      _n[i].init(s,0);
      _nverf[i].init(s,verfInit0);
      _n1verf[i]=_n2verf[i]=verfInit0;
      _bigramVerfSum+=verfInit0*s;
      _unigramVerfSum1+=verfInit0;
      _unigramVerfSum2+=verfInit0;
    }
  if( withVerfaelschung )
    {
      cout << "VERFAELSCHUNG " << _bigramVerfSum << " " << _unigramVerfSum1 << " " << _unigramVerfSum2 << endl;
    }
  verfTabSigma=sigmaVerfaelschung;
  
  
  
}

void KategProblemKBC::setN(int w1,int w2, FreqType n)
  
{
  addN(w1,w2,-_n[w1][w2]);
  addN(w1,w2,n);
}
  

double KategProblemKBC::fullBewertung(int auswertung)
{
  
  double bewertung=0;
  int c1,c2;
  

  switch( auswertung )
    {
    case CRITERION_ML:
      for(c1=0;c1<nKats;c1++)
	{
	  for(c2=0;c2<nKats;c2++)
	    bewertung-=kat_h(_n[c1][c2]);
	  bewertung+=kat_h(_n1[c1])+kat_h(_n2[c1]);
	}
      break;
    case CRITERION_MY:
      {
      for(c1=0;c1<nKats;c1++)
	{
	  for(c2=0;c2<nKats;c2++)
	    bewertung-=mkat_h_full((int)n(c1,c2),nverf(c1,c2));
	  bewertung+=mkat_h_part((int)(n1(c1)),n1verf(c1))+mkat_h_part((int)(n2(c1)),n2verf(c1));
	}
      double u1=_unigramVerfSum1-verfInit0*c1_0;
      double u2=_unigramVerfSum2-verfInit0*c2_0;
      double b=_bigramVerfSum-verfInit0*(c1_0*nKats+c2_0*nKats-c1_0*c2_0);
      if( verboseMode>1 )
	{
	  cout << "CRITERION_MY: " << bewertung << endl;
	  cout << "U1:"<<_unigramVerfSum1 << " n:"<<u1<< " " 
	       << "U2:"<<_unigramVerfSum2 << " n:"<<u2<< " " 
	       << "U3:"<<_bigramVerfSum   << " n:"<<b<< endl;
	}
      if(b>0.000001)
	{
	  
	  
	  if(verboseMode>1 )
	    cout <<  "  NEU: " <<_nWords*log( u1 * u2 / b ) << endl;
	  bewertung -= _nWords*log( u1 * u2 / b );
	  if(verboseMode>1)
	    cout << "SCHLUSSBEWERTUNG: " << bewertung << endl;
	}
      else
	cout << "B zu klein " << b << endl;
      }
      break;
    case CRITERION_LO:
      for(c1=0;c1<nKats;c1++)
	{
	  for(c2=0;c2<nKats;c2++)
	    bewertung-=_n[c1][c2]*kat_mlog(_n[c1][c2]-1-rhoLo);
	  bewertung+=_n1[c1]*kat_mlog(_n1[c1]-1)+_n2[c1]*kat_mlog(_n2[c1]-1);
	}
      bewertung-=kat_etaFkt(eta0,eta1,(c1_0*nKats+c2_0*nKats-c1_0*c2_0),nKats);
      break;
    default:
      cerr << "Error: wrong criterion " << auswertung << endl;
      exit(1);
    }
  return bewertung;
}

double KategProblemKBC::myCriterionTerm()
{
  iassert( withVerfaelschung );
  double r;
      double u1=_unigramVerfSum1-verfInit0*c1_0;
      double u2=_unigramVerfSum2-verfInit0*c2_0;
      double b=_bigramVerfSum-verfInit0*(c1_0*nKats+c2_0*nKats-c1_0*c2_0);
  
  
  if( verboseMode>1 )
    {
      cout << "nwords divisor:"<<_nWords << " " << u1 * u2 / b << endl;
      cout << "ergebnis:      "<<_nWords*log( u1 * u2 / b ) << endl;
      cout << "0:             "<<c1_0 << endl;
    }
  r       = _nWords*log( u1 * u2 / b );
  
  return -r;
}




double KategProblemKBC::bigramVerfSum()
{
  double sum=0;
  for(int c1=0;c1<nKats;c1++)
    for(int c2=0;c2<nKats;c2++)
      sum+=nverf(c1,c2);
  cout << "BIGRAMVERFSUM: " << sum << endl;
  return sum;
}

double KategProblemKBC::unigramVerfSum1()
{
  double sum=0;
  for(int c1=0;c1<nKats;c1++)
    sum+=n1verf(c1);
  cout << "UNIGRAMVERFSUM1: " << sum << endl;
  return sum;
}

double KategProblemKBC::unigramVerfSum2()
{
  double sum=0;
  for(int c1=0;c1<nKats;c1++)
    sum+=n2verf(c1);
  cout << "UNIGRAMVERFSUM2: " << sum << endl;
 return sum;
}



































