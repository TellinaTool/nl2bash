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
#include "transpair_model4.h"
#include "Parameter.h"

GLOBAL_PARAMETER(float,d4modelsmooth_factor,"model4SmoothFactor","smooting parameter for alignment probabilities in Model 4",PARLEV_SMOOTH,0.2);

LogProb transpair_model4::_scoreOfMove(const alignment&a, WordIndex new_i, WordIndex j,double)const
{
  LogProb a_prob=prob_of_target_and_alignment_given_source(a);
  alignment b(a);
  b.set(j, new_i);
  LogProb b_prob=prob_of_target_and_alignment_given_source(b);
  if( a_prob )
    return b_prob/a_prob;
  else if( b_prob )
    return 1e20;
  else
    return 1.0;
}
LogProb transpair_model4::_scoreOfSwap(const alignment&a, WordIndex j1, WordIndex j2,double)const 
{
  LogProb a_prob=prob_of_target_and_alignment_given_source(a);
  alignment b(a);
  b.set(j1, a(j2));
  b.set(j2, a(j1));
  LogProb b_prob=prob_of_target_and_alignment_given_source(b);
  if( a_prob )
    return b_prob/a_prob;
  else if( b_prob )
    return 1e20;
  else
    return 1.0;
}
//increasing efficiency: no copy of alignment (calc. everything incrementally)
LogProb transpair_model4::scoreOfMove(const alignment&a, WordIndex new_i, WordIndex j,double thisValue)const
{
  if( a(j)==new_i )
    return 1.0;
  LogProb change=transpair_model3::scoreOfMove(a,new_i,j,-1.0,0);
  LogProb a_prob=thisValue;
  if(a_prob<0.0 )
    a_prob=prob_of_target_and_alignment_given_source(a,2);
  massert(a_prob==prob_of_target_and_alignment_given_source(a,2));
  WordIndex old_i=a(j);
  //alignment b(a);
  const_cast<alignment&>(a).set(j,new_i);
  LogProb b_prob=prob_of_target_and_alignment_given_source(a,2);
  const_cast<alignment&>(a).set(j,old_i);
  change*=b_prob/a_prob;
  return change;
}
//increasing efficiency: no copy of alignment (calc. everything incrementally)
LogProb transpair_model4::scoreOfSwap(const alignment&a, WordIndex j1, WordIndex j2,double thisValue)const 
{
  WordIndex aj1=a(j1),aj2=a(j2);
  if( aj1==aj2 )
    return 1.0;
  LogProb change=transpair_model3::scoreOfSwap(a,j1,j2,-1.0,0);
  LogProb a_prob=thisValue;
  if( a_prob<0.0 )
    a_prob=prob_of_target_and_alignment_given_source(a,2);
  massert(a_prob==prob_of_target_and_alignment_given_source(a,2));

  //alignment b(a);
  const_cast<alignment&>(a).set(j1,aj2);
  const_cast<alignment&>(a).set(j2,aj1);
  LogProb b_prob=prob_of_target_and_alignment_given_source(a,2);
  const_cast<alignment&>(a).set(j1,aj1);
  const_cast<alignment&>(a).set(j2,aj2);

  if( verboseTP )
    cerr << "scoreOfSwap: " << change << ' ' << a_prob << ' ' << b_prob << ' ' << endl;
  change*=b_prob/a_prob;
  if( verboseTP )
    cerr << "resulting: " << change << " should be " << _scoreOfSwap(a,j1,j2) << endl;
  return change;
}

LogProb transpair_model4::prob_of_target_and_alignment_given_source_1(const alignment&al,bool verb)const
{
  LogProb total = 1.0 ;
  total *= pow(double(1-p1), m-2.0 * al.fert(0)) * pow(double(p1), double(al.fert(0)));
  if( verb) cerr << "IBM-4: (1-p1)^(m-2 f0)*p1^f0: " << total << endl;
  for (WordIndex i = 1 ; i <= al.fert(0) ; i++)
    total *= double(m - al.fert(0) - i + 1) / (double(DeficientDistortionForEmptyWord?(max(2,int(m))/DeficientDistortionForEmptyWord):i)) ;
  if( verb) cerr << "IBM-4: +NULL:binomial+distortion " << total << endl;
  for (WordIndex i = 1 ; i <= l ; i++)
    {
      total *= get_fertility(i, al.fert(i));// * (LogProb) factorial(al.fert(i));
      if( verb) cerr << "IBM-4: fertility of " << i << " " << get_fertility(i, al.fert(i)) << " -> " << total << endl;
    }
  for (WordIndex j = 1 ; j <= m ; j++)
    {
      total*= get_t(al(j), j) ;
      if( verb) cerr << "IBM-4: t of j:" << j << " i:" << al(j) << ": " << get_t(al(j), j)  << " -> " << total << endl;
    }
  return total;
}

LogProb transpair_model4::prob_of_target_and_alignment_given_source(const alignment&al, short distortionType,bool verb)const
{
  LogProb total = 1.0 ;
  static const LogProb almostZero = 1E-299 ; 
  if( distortionType&1 )
    {
      total *= prob_of_target_and_alignment_given_source_1(al,verb);
    }
  if( distortionType&2 )
    {
      for(WordIndex j=1;j<=m;j++)
	if( al(j) )
	  if( al.get_head(al(j))==j)
	    {
	      int ep=al.prev_cept(al(j));
	      float x2=probFirst[ep](j,al.get_center(ep));
	      massert(x2<=1.0);
	      total*=x2;
	      if( verb) cerr << "IBM-4: d=1 of " << j << ": " << x2  << " -> " << total << endl;
	    }
	  else
	    {
	      float x2=probSecond(j,al.prev_in_cept(j));
	      massert(x2<=1.0);
	      total*=x2;
	      if( verb) cerr << "IBM-4: d>1 of " << j << ": " << x2  << " -> " << total << endl;
	    }
    }
  return total?total:almostZero;
}

void transpair_model4::computeScores(const alignment&al,vector<double>&d)const
{
  LogProb total1 = 1.0,total2=1.0,total3=1.0,total4=1.0 ;
  total1 *= pow(double(1-p1), m-2.0 * al.fert(0)) * pow(double(p1), double(al.fert(0)));
  for (WordIndex i = 1 ; i <= al.fert(0) ; i++)
    total1 *= double(m - al.fert(0) - i + 1) / (double(DeficientDistortionForEmptyWord?(max(2,int(m))/DeficientDistortionForEmptyWord):i)) ;
  for (WordIndex i = 1 ; i <= l ; i++)
    total2 *= get_fertility(i, al.fert(i));// * (LogProb) factorial(al.fert(i));
  for (WordIndex j = 1 ; j <= m ; j++)
    total3*= get_t(al(j), j) ;
  for(WordIndex j=1;j<=m;j++)
    if( al(j) )
      if( al.get_head(al(j))==j)
	{
	  int ep=al.prev_cept(al(j));
	  float x2=probFirst[ep](j,al.get_center(ep));
	  total4*=x2;
	}
      else
	{
	  float x2=probSecond(j,al.prev_in_cept(j));
	  total4*=x2;
	}
  d.push_back(total1);//9
  d.push_back(total2);//10
  d.push_back(total3);//11
  d.push_back(total4);//12
}
