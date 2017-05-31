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







#ifndef KATEGPROBLEMKBC_H
#define KATEGPROBLEMKBC_H

typedef Array<FreqType> FreqArray;
typedef Array<double> FreqArrayReal;


double verfaelsche(int a,double b);
double verfaelsche(double a,double b);

class KategProblemKBC


{
 friend class KategProblem;

 private:
  Array<FreqArray> _n; 
  Array<FreqType> _n1;      
                       
  Array<FreqType> _n2;      
                       
			
  double sigmaVerfaelschung;
  short withVerfaelschung;

  Array<FreqArrayReal> _nverf;
  Array<double> _n1verf;
  Array<double> _n2verf;
  FreqType _nWords;

 protected:
  int eta0;            
  int eta1;            
  int c1_0;            
  int c2_0;            
  double _bigramVerfSum;
  double _unigramVerfSum1;
  double _unigramVerfSum2;
  double verfInit0;

 public:
  int nKats;           

  KategProblemKBC(int nKats,double sv);
  

  double fullBewertung(int auswertung);
  

  FreqType n(int w1,int w2) { return _n[w1][w2]; };
  

  FreqType n1(int w) { return _n1[w];};
  

  FreqType n2(int w) { return _n2[w];};
  
  
  double bigramVerfSum();
  double unigramVerfSum1();
  double unigramVerfSum2();

  double nverf(int w1,int w2) { return _nverf[w1][w2]; }
  
  double n1verf(int w) { return _n1verf[w]; };

  double n2verf(int w) { return _n2verf[w]; };

  inline void addN(int w1,int w2, FreqType n);
  

  void setN(int w1,int w2, FreqType n);  
  
  
  double myCriterionTerm();

};

inline void KategProblemKBC::addN(int w1,int w2, FreqType n)    
{
  if(n!=0)
    {
      FreqType &s= _n[w1][w2];
      if(s==0)
	eta0--;
      else if(s==1)
	eta1--;
      if(_n1[w1]==0)
	c1_0--;
      if(_n2[w2]==0)
	c2_0--;
      
      if(withVerfaelschung)
	{
	  double verfOld=verfaelsche(s,sigmaVerfaelschung);
	  double verfNew=verfaelsche(s+n,sigmaVerfaelschung);
	  double verfOld1=verfaelsche(_n1[w1],sigmaVerfaelschung);
	  assert(verfOld1==_n1verf[w1]);
	  double verfNew1=verfaelsche(_n1[w1]+n,sigmaVerfaelschung);
	  double verfOld2=verfaelsche(_n2[w2],sigmaVerfaelschung);
	  assert(verfOld2==_n2verf[w2]);
	  double verfNew2=verfaelsche(_n2[w2]+n,sigmaVerfaelschung);
	  _n1verf[w1]=verfNew1;
	  _unigramVerfSum1+=verfNew1-verfOld1;
	  _n2verf[w2]=verfNew2;
	  _unigramVerfSum2+=verfNew2-verfOld2;
	  _nverf[w1][w2]=verfNew;
	  _bigramVerfSum+=verfNew-verfOld;
	  _nWords+=n;
	}
      s+=n;_n1[w1]+=n;_n2[w2]+=n; 

      assert(_n[w1][w2]>=0);
      assert(_n1[w1]>=0);
      assert(_n2[w2]>=0);
      
      if(s==0)
	eta0++;
      else if(s==1) 
	eta1++;
      if(_n1[w1]==0)
	c1_0++;
      if(_n2[w2]==0)
	c2_0++;
    }
};
#endif
