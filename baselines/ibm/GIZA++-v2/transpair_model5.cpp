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
#include "transpair_model5.h"
#include "Parameter.h"

int m5scorefound=0,m5scorenotfound=0;

GLOBAL_PARAMETER(float,d5modelsmooth_factor,"model5SmoothFactor","smooting parameter for distortion probabilities in Model 5 (linear interpolation with constant)",PARLEV_SMOOTH,0.1);
float d5modelsmooth_countoffset=0.0;

LogProb transpair_model5::_scoreOfMove(const alignment&a, WordIndex new_i, WordIndex j,double)const
{
  if( doModel4Scoring )
    return transpair_model4::_scoreOfMove(a,new_i,j);
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
LogProb transpair_model5::_scoreOfSwap(const alignment&a, WordIndex j1, WordIndex j2,double thisValue)const 
{
  if( doModel4Scoring )
    return transpair_model4::_scoreOfSwap(a,j1,j2,thisValue);
  alignment b(a);
  b.set(j1, a(j2));
  b.set(j2, a(j1));
  LogProb a_prob=prob_of_target_and_alignment_given_source(a);
  LogProb b_prob=prob_of_target_and_alignment_given_source(b);
  assert(a_prob);
  assert(b_prob);
  if( a_prob )
    return b_prob/a_prob;
  else if( b_prob )
    return 1e20;
  else
    return 1.0;
}

//increasing efficiency: no copy of alignment (calc. everything incrementally)
LogProb transpair_model5::scoreOfMove(const alignment&a, WordIndex new_i, WordIndex j,double thisValue)const
{
  if( doModel4Scoring )
    return transpair_model4::scoreOfMove(a,new_i,j,thisValue);
  alignment b(a);
  b.set(j,new_i);
  
  LogProb change;
  const WordIndex old_i=a(j);
  WordIndex f0=a.fert(0);
  if (old_i == new_i)
    change=1.0;
  else if (old_i == 0)
    change=((double)p0*p0/p1) *
      ((f0*(m-f0+1.0)) / ((m-2*f0+1)*(m-2*f0+2.0))) *
      ((PROB)(1.0)) *
      (get_fertility(new_i, a.fert(new_i)+1) / get_fertility(new_i, a.fert(new_i)))*
      (t(new_i, j)/t(old_i, j))*
      1.0;
  else if (new_i == 0)
    change=(double(p1) / (p0*p0)) *
      (double((m-2*f0)*(m-2*f0-1))/((1+f0)*(m-f0))) *
      (1.0) *
      (get_fertility(old_i, a.fert(old_i)-1) /get_fertility(old_i, a.fert(old_i)))*
      (t(new_i, j) /t(old_i, j)) *
      (1.0);
  else
    change=(1.0) *
      (get_fertility(old_i,a.fert(old_i)-1) / get_fertility(old_i,a.fert(old_i))) *
      (get_fertility(new_i,a.fert(new_i)+1) /get_fertility(new_i,a.fert(new_i))) *
      (t(new_i,j)/t(old_i,j)) *
      (1.0);
  LogProb a_prob=thisValue;
  if( a_prob<0.0 )
    a_prob=prob_of_target_and_alignment_given_source(a,2);
  massert(a_prob==prob_of_target_and_alignment_given_source(a,2));
  
  LogProb b_prob=prob_of_target_and_alignment_given_source(b,2);
  change*=b_prob/a_prob;
  return change;
}
LogProb transpair_model5::scoreOfSwap(const alignment&a, WordIndex j1, WordIndex j2,double thisValue)const 
{
  if( doModel4Scoring )
    return transpair_model4::scoreOfSwap(a,j1,j2,thisValue);
  alignment b(a);
  b.set(j1,a(j2));
  b.set(j2,a(j1));
  LogProb change=transpair_model3::scoreOfSwap(a,j1,j2,-1.0,0);
  LogProb a_prob=thisValue;
  if( a_prob<0.0 )
    a_prob=prob_of_target_and_alignment_given_source(a,2);
  massert(a_prob==prob_of_target_and_alignment_given_source(a,2));
  LogProb b_prob=prob_of_target_and_alignment_given_source(b,2);
  change*=b_prob/a_prob;
  return change;
}

LogProb transpair_model5::prob_of_target_and_alignment_given_source(const alignment&al, short distortionType,bool verb)const
{
  if( doModel4Scoring )
    return transpair_model4::prob_of_target_and_alignment_given_source(al,distortionType);
  LogProb total = 1.0 ;
  static const LogProb almostZero = 1E-299 ; 
  double x2;
  if( distortionType&1 )
    {
      total *= pow(double(1-p1), m-2.0 * al.fert(0)) * pow(double(p1), double(al.fert(0)));
      if( verb) cerr << "IBM-5: (1-p1)^(m-2 f0)*p1^f0: " << total << endl;
      for (WordIndex i = 1 ; i <= al.fert(0) ; i++)
	total *= double(m - al.fert(0) - i + 1) / i ; // IBM-5 is not deficient!
      if( verb) cerr << "IBM-5: +NULL:binomial+distortion " << total << endl;
      for (WordIndex i = 1 ; i <= l ; i++)
	{
	  total *= get_fertility(i, al.fert(i));
	  if( verb) cerr << "IBM-5: fertility of " << i << " " << get_fertility(i, al.fert(i)) << " -> " << total << endl;
	}
      for (WordIndex j = 1 ; j <= m ; j++)
	{
	  total*= get_t(al(j), j) ;
	  if( verb) cerr << "IBM-5: t of j:" << j << " i:" << al(j) << ": " << get_t(al(j), j)  << " -> " << total << endl;
	}
    }
  if( distortionType&2 )
    {
      PositionIndex prev_cept=0;
      PositionIndex vac_all=m;
      Vector<char> vac(m+1,0);
      for(WordIndex i=1;i<=l;i++)
	{
	  PositionIndex cur_j=al.als_i[i]; 
	  PositionIndex prev_j=0;
	  PositionIndex k=0;
	  if(cur_j) { // process first word of cept
	    k++;
	    // previous position
	    total*= (x2=d5m.getProb_first(vacancies(vac,cur_j),vacancies(vac,al.get_center(prev_cept)),d5m.fwordclasses.getClass(get_fs(cur_j)),l,m,vac_all-al.fert(i)+k));
	    
	    vac_all--;
	    assert(vac[cur_j]==0);
	    vac[cur_j]=1;
	    
	    if( verb) cerr << "IBM-5: d=1 of " << cur_j << ": " << x2  << " -> " << total << endl;
	    prev_j=cur_j;
	    cur_j=al.als_j[cur_j].next;
	  }
	  while(cur_j) { // process following words of cept
	    k++;
	    // previous position
	    int vprev=vacancies(vac,prev_j);
	    total*= (x2=d5m.getProb_bigger(vacancies(vac,cur_j),vprev,d5m.fwordclasses.getClass(get_fs(cur_j)),l,m,vac_all-vprev/*war weg*/-al.fert(i)+k));
	    
	    
	    vac_all--;
	    vac[cur_j]=1;
	    
	    
	    if( verb) cerr << "IBM-5: d>1 of " << cur_j << ": " << x2  << " -> " << total << endl;
	    prev_j=cur_j;
	    cur_j=al.als_j[cur_j].next;
	  }
	  assert(k==al.fert(i));
	  if( k )
	    prev_cept=i;
	}
      assert(vac_all==al.fert(0));
    }
  total = total?total:almostZero;
  return total;
}


void transpair_model5::computeScores(const alignment&al,vector<double>&d)const
{
  LogProb total1 = 1.0,total2=1.0,total3=1.0,total4=1.0 ;
  total1 *= pow(double(1-p1), m-2.0 * al.fert(0)) * pow(double(p1), double(al.fert(0)));
  for (WordIndex i = 1 ; i <= al.fert(0) ; i++)
    total1 *= double(m - al.fert(0) - i + 1) / i ; // IBM-5 is not deficient!
  for (WordIndex i = 1 ; i <= l ; i++)
    total2 *= get_fertility(i, al.fert(i));
  for (WordIndex j = 1 ; j <= m ; j++)
    total3*= get_t(al(j), j) ;
  PositionIndex prev_cept=0;
  PositionIndex vac_all=m;
  Vector<char> vac(m+1,0);
  for(WordIndex i=1;i<=l;i++)
    {
      PositionIndex cur_j=al.als_i[i]; 
      PositionIndex prev_j=0;
      PositionIndex k=0;
      if(cur_j) { // process first word of cept
	k++;
	total4*=d5m.getProb_first(vacancies(vac,cur_j),vacancies(vac,al.get_center(prev_cept)),d5m.fwordclasses.getClass(get_fs(cur_j)),l,m,vac_all-al.fert(i)+k);
	vac_all--;
	assert(vac[cur_j]==0);
	vac[cur_j]=1;
	prev_j=cur_j;
	cur_j=al.als_j[cur_j].next;
      }
      while(cur_j) { // process following words of cept
	k++;
	int vprev=vacancies(vac,prev_j);
	total4*=d5m.getProb_bigger(vacancies(vac,cur_j),vprev,d5m.fwordclasses.getClass(get_fs(cur_j)),l,m,vac_all-vprev/*war weg*/-al.fert(i)+k);
	vac_all--;
	vac[cur_j]=1;
	prev_j=cur_j;
	cur_j=al.als_j[cur_j].next;
      }
      assert(k==al.fert(i));
      if( k )
	prev_cept=i;
    }
  assert(vac_all==al.fert(0));
  d.push_back(total1);//13
  d.push_back(total2);//14
  d.push_back(total3);//15
  d.push_back(total4);//16
}
