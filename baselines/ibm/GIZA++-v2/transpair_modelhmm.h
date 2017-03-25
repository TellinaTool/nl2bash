/*

Copyright (C) 2000,2001  Franz Josef Och (RWTH Aachen - Lehrstuhl fuer Informatik VI)

This file is part of GIZA++ ( extension of GIZA ).

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
#ifndef transpair_modelhmm_h_fjo_defined
#define transpair_modelhmm_h_fjo_defined
#include "Array2.h"
#include "defs.h"
#include "Vector.h"
#include "NTables.h"
#include "ATables.h"
#include "TTables.h"
#include "alignment.h"
#include <cmath>
#include "transpair_model2.h"
#include "ForwardBackward.h"
#include "hmm.h"

class transpair_modelhmm : public transpair_model2
{
 public:
 typedef transpair_modelhmm simpler_transpair_model;           
  HMMNetwork*net;
  transpair_modelhmm(const Vector<WordIndex>&es, const Vector<WordIndex>&fs, const tmodel<COUNT, PROB>&tTable, 
		   const amodel<PROB>&aTable,const amodel<PROB>&,const nmodel<PROB>&, 
		   double, double,const hmm*h)
    : transpair_model2(es,fs,tTable,aTable),net(h->makeHMMNetwork(es,fs,0))
    {}
   ~transpair_modelhmm() { delete net; }
  int modelnr()const{return 6;}
  LogProb scoreOfMove(const alignment&a, WordIndex _new_i, WordIndex j,double=-1.0)const
    {
      int new_i=_new_i;
      LogProb change=1.0;
      int old_i=a(j);
      if (old_i == new_i)
	change=1.0;
      else
	{
	  int theJ=j-1;
	  old_i--;
	  new_i--;
	  int jj=j-1;
	  while(jj>0&&a(jj)==0)
	    jj--;
	  int theIPrev= (jj>0)?(a(jj)-1):0;
	  if( j>1&&a(j-1)==0 )
	    theIPrev+=l;
	  if( old_i==-1 ){old_i = theIPrev;if(old_i<int(l))old_i+=l;}
	  if( new_i==-1 ){new_i = theIPrev;if(new_i<int(l))new_i+=l;}
	  int theIPrevOld=theIPrev,theIPrevNew=theIPrev;
	  if( theJ==0 )
	    {
	      change*=net->getAlphainit(new_i)/net->getAlphainit(old_i);
	    }
	  do
	    {
	      if( new_i!=old_i )
		{
		  change*=net->nodeProb(new_i,theJ)/net->nodeProb(old_i,theJ);
		}
	      if( theJ>0)
		change*=net->outProb(theJ,theIPrevNew,new_i)/net->outProb(theJ,theIPrevOld,old_i);
	      theIPrevOld=old_i;
	      theIPrevNew=new_i;
	      theJ++;
	      if( theJ<int(m) && a(theJ+1)==0 )
		{
		  if( new_i<int(l)) new_i+=l;
		  if( old_i<int(l)) old_i+=l;
		}
	    } while( theJ<int(m) && a(theJ+1)==0 );
	  if(theJ==int(m))
	    {
	      change*=net->getBetainit(new_i)/net->getBetainit(old_i);
	    }
	  else
	    {
	      new_i=a(theJ+1)-1;
	      if( new_i==-1)
		new_i=theIPrevNew;
	      change*=net->outProb(theJ,theIPrevNew,new_i)/net->outProb(theJ,theIPrevOld,new_i);
	    }
	}
      return change;
    }
  LogProb scoreOfAlignmentForChange(const alignment&)const
    {return -1.0; }  
  LogProb scoreOfSwap(const alignment&a, WordIndex j1, WordIndex j2,double=-1.0)const 
    {
      return _scoreOfSwap(a,j1,j2);
    }
  LogProb _scoreOfMove(const alignment&a, WordIndex new_i, WordIndex j,double=-1.0)const
    {
      alignment b(a);
      b.set(j, new_i);
      LogProb a_prob=prob_of_target_and_alignment_given_source(a);
      LogProb b_prob=prob_of_target_and_alignment_given_source(b);
      if( a_prob )
	return b_prob/a_prob;
      else if( b_prob )
	return 1e20;
      else
	return 1.0;
    }
  LogProb _scoreOfSwap(const alignment&a, WordIndex j1, WordIndex j2,double=-1.0)const
    {
      WordIndex aj1=a(j1),aj2=a(j2);
      if( aj1==aj2 )
	return 1.0;
      LogProb a_prob=prob_of_target_and_alignment_given_source(a);

      /*alignment b(a);
      b.set(j1, a(j2));
      b.set(j2, a(j1));
      LogProb b_prob=prob_of_target_and_alignment_given_source(b);*/

      const_cast<alignment&>(a).set(j1,aj2);
      const_cast<alignment&>(a).set(j2,aj1);
      LogProb b_prob=prob_of_target_and_alignment_given_source(a);
      const_cast<alignment&>(a).set(j1,aj1);
      const_cast<alignment&>(a).set(j2,aj2);

      if( a_prob )
	return b_prob/a_prob;
      else if( b_prob )
	return 1e20;
      else
	return 1.0;
    }
  inline friend ostream&operator<<(ostream&out, const transpair_modelhmm&)
    {
      return out << "NO-OUTPUT for transpair_modelhmm\n";
    }
  LogProb prob_of_target_and_alignment_given_source(const alignment&al,bool verbose=0)const
    {
      double prob=1.0;
      int theIPrev=0;
      for(unsigned int j=1;j<=m;j++)
	{
	  int theJ=j-1;
	  int theI=al(j)-1;
	  if( theI==-1 )
	    theI=(theIPrev%l)+l;
	  prob*=net->nodeProb(theI,theJ);
	  if( verbose )
	    cout << "NP " << net->nodeProb(theI,theJ) << ' ';
	  if( j==1 )
	    {
	      prob*=net->getAlphainit(theI);
	      if( verbose )
		cout << "AP0 " << net->getAlphainit(theI) << ' ';
	    }
	  else
	    {
	      prob*=net->outProb(theJ,theIPrev,theI);
	      if( verbose )
		cout << "AP1 " << net->outProb(theJ,theIPrev,theI) << ' ';
	    }
	  theIPrev=theI;
	  if( j==m )
	    {
	      prob*=net->getBetainit(theI);
	      if( verbose )
		cout << "AP2 " << net->getBetainit(theI) << ' ';
	    }
	  if( verbose )
	    cout << "j:"<<theJ<<" i:"<<theI << ";  ";
	}
      if( verbose )
	cout << '\n';
      return prob*net->finalMultiply;
    }
  void computeScores(const alignment&al,vector<double>&d)const
    {
      double prob1=1.0,prob2=1.0;
      int theIPrev=0;
      for(unsigned int j=1;j<=m;j++)
	{
	  int theJ=j-1;
	  int theI=al(j)-1;
	  if( theI==-1 )
	    theI=(theIPrev%l)+l;
	  prob1*=net->nodeProb(theI,theJ);
	  if( j==1 )
	    {
	      prob2*=net->getAlphainit(theI);
	    }
	  else
	    {
	      prob2*=net->outProb(theJ,theIPrev,theI);
	    }
	  theIPrev=theI;
	  if( j==m )
	    {
	      prob2*=net->getBetainit(theI);
	    }
	}
      d.push_back(prob1);
      d.push_back(prob2);
    }

  bool isSubOptimal()const{return 0;}
};
#endif
