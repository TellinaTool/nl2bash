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







#ifndef KATEGPROBLEMWBC_H
#define KATEGPROBLEMWBC_H

struct OneFreq
{
  int w; 
  FreqType n; 
};

typedef Array<OneFreq> ManyFreq;

class KategProblemWBC

{

  friend class KategProblem;

 private:
  Array<FreqType> _n1; 
                  
  Array<FreqType> _n2; 
                  

  double h_of_words;
                  
                  
  short with_h_of_words; 

  Array<int> afterFilled; 
  Array<int> beforeFilled;

  Array<int> &getSortedList(int steigend); 
  

 protected:
  KategProblemWBC(int n,int minw);
  

  ~KategProblemWBC();
  

  short filled;           
                               
  Array<int> fixedWord; 
  Array<int> *absteigend; 

  void init(int specialFixedWord=-1);
  

 public:
  int nWords;             
  int nTranspWords;       
  short mindestAnzahl;    
  Array<ManyFreq> after;  
  Array<ManyFreq> before; 
  Array<int> minIndex; 
  Array<int> maxIndex; 
  

  
  void setAfterWords(int w,int anzahl);
  

  void setBeforeWords(int w,int anzahl);
  

  void setFreq(int w1,int w2, FreqType anzahl);
  

  void addFreq(int w1,int w2,FreqType anzahl);
  

  void setDollar(int n);
  

  int fixed(int w)
    {
      return fixedWord[w];
    }

  FreqType n1(int w) { return _n1[w];};
  

  FreqType n2(int w) { return _n2[w];};
  

  FreqType numberOfWords();
  

  short testFull(int doIt=0);
  

  double get_h_of_words();
  

  void set_h_of_words(double s);
  

  void initializeIndex(const leda_array<string>&words,char firstChar,int min,int max,bool noHapas);
};

#endif
