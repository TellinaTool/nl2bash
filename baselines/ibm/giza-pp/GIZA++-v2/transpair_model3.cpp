/*

EGYPT Toolkit for Statistical Machine Translation
Written by Yaser Al-Onaizan, Jan Curin, Michael Jahr, Kevin Knight, John Lafferty, Dan Melamed, David Purdy, Franz Och, Noah Smith, and David Yarowsky.

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
/*--
transpair_model3: representation of a translation pair for model3 training
allowing for fast access (esp. to t table).

Franz Josef Och (30/07/99)
--*/
#include "transpair_model3.h"
#include <algorithm>

transpair_model3::transpair_model3(const Vector<WordIndex>&es, const Vector<WordIndex>&fs, tmodel<COUNT, PROB>&tTable, amodel<PROB>&aTable, amodel<PROB>&dTable, nmodel<PROB>&nTable, double _p1, double _p0, void*)
  : transpair_model2(es,fs,tTable,aTable),d(es.size(), fs.size()),n(es.size(), MAX_FERTILITY+1), p0(_p0), p1(_p1)
{ 
  WordIndex l=es.size()-1,m=fs.size()-1;
  for(WordIndex i=0;i<=l;i++)
    {
      for(WordIndex j=1;j<=m;j++)
	d(i, j)=dTable.getValue(j, i, l, m);
      if( i>0 )
	{
	  for(WordIndex f=0;f<MAX_FERTILITY;f++)
	    n(i, f)=nTable.getValue(es[i], f);
	  n(i,MAX_FERTILITY)=PROB_SMOOTH;
	}
    }
}

LogProb transpair_model3::scoreOfMove(const alignment&a, WordIndex new_i, WordIndex j, double,bool forModel3)const
{
  LogProb change;
  const WordIndex old_i=a(j);
  WordIndex f0=a.fert(0);
  if (old_i == new_i)
    change=1.0;
  else if (old_i == 0)
    change=((double)p0*p0/p1) *
      (( (DeficientDistortionForEmptyWord?(max(2,int(m))/DeficientDistortionForEmptyWord):f0)*(m-f0+1.0)) / ((m-2*f0+1)*(m-2*f0+2.0))) *
      ((PROB)(forModel3?(a.fert(new_i)+1.0):1.0)) *
      (get_fertility(new_i, a.fert(new_i)+1) / get_fertility(new_i, a.fert(new_i)))*
      (t(new_i, j)/t(old_i, j))*
      (forModel3?d(new_i, j):1.0);
  else if (new_i == 0)
    change=(double(p1) / (p0*p0)) *
      (double((m-2*f0)*(m-2*f0-1))/( (DeficientDistortionForEmptyWord?(max(2,int(m))/DeficientDistortionForEmptyWord):(1+f0))*(m-f0))) *
      (forModel3?(1.0/a.fert(old_i)):1.0) *
      (get_fertility(old_i, a.fert(old_i)-1) /get_fertility(old_i, a.fert(old_i)))*
      (t(new_i, j) /t(old_i, j)) *
      (forModel3?(1.0 / d(old_i, j)):1.0);
  else
    change=(forModel3?((a.fert(new_i)+1.0)/a.fert(old_i)):1.0) *
      (get_fertility(old_i,a.fert(old_i)-1) / get_fertility(old_i,a.fert(old_i))) *
      (get_fertility(new_i,a.fert(new_i)+1) /get_fertility(new_i,a.fert(new_i))) *
      (t(new_i,j)/t(old_i,j)) *
      (forModel3?(d(new_i,j)/d(old_i,j)):1.0);
  return change;
}

LogProb transpair_model3::scoreOfSwap(const alignment&a, WordIndex j1, WordIndex j2, double,bool forModel3)const 
{
  PROB score=1;
  assert(j1<j2);
  WordIndex i1=a(j1), i2=a(j2);
  if (i1!=i2) 
    {
      score=(t(i2, j1)/t(i1, j1))*(t(i1, j2)/t(i2, j2));
      if( forModel3 )
	{
	  if (i1)
	    score *= d(i1, j2)/d(i1, j1);
	  if (i2)
	    score *= d(i2, j1)/d(i2, j2);    
	}
    }
  return score;
}

ostream&operator<<(ostream&out, const transpair_model3&m)
{
  for(WordIndex i=0;i<=m.get_l();i++)
    {
      out << "EF-I:"<<i<<' ';
      for(WordIndex j=1;j<=m.get_m();j++)
	out << "("<<m.t(i,j)<<","<<m.d(i,j)<<")";
      for(WordIndex j=1;j<MAX_FERTILITY;j++)
	if( i>0 )
	  out << "(fert:"<<m.get_fertility(i,j)<<")";
      out << '\n';
    }
  out << "T:" << m.t << "D:" << m.d << "A:" << m.a  << "N:" << m.n << m.p0 << m.p1 << '\n';
  return out;
}

LogProb transpair_model3::_scoreOfMove(const alignment&a, WordIndex new_i, WordIndex j,double)const
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

LogProb transpair_model3::_scoreOfSwap(const alignment&a, WordIndex j1, WordIndex j2,double thisValue)const
{
  alignment b(a);
  b.set(j1, a(j2));
  b.set(j2, a(j1));
  LogProb a_prob=thisValue;
  if( a_prob<0.0 )
    a_prob=prob_of_target_and_alignment_given_source(a);
  massert(a_prob==prob_of_target_and_alignment_given_source(a));
  LogProb b_prob=prob_of_target_and_alignment_given_source(b);
  if( a_prob )
    return b_prob/a_prob;
  else if( b_prob )
    return 1e20;
  else
    return 1.0;
}

LogProb transpair_model3::prob_of_target_and_alignment_given_source(const alignment&al,bool verb)const
{
  LogProb total = 1.0 ;
  static const LogProb zero = 1E-299 ; 
  total *= pow(double(1-p1), m-2.0 * al.fert(0)) * pow(double(p1), double(al.fert(0)));
  if( verb) cerr << "IBM-3: (1-p1)^(m-2 f0)*p1^f0: " << total << '\n';
  for (WordIndex i = 1 ; i <= al.fert(0) ; i++)
    total *= double(m - al.fert(0) - i + 1) / (double(DeficientDistortionForEmptyWord?(max(2,int(m))/DeficientDistortionForEmptyWord):i)) ;
  if( verb) cerr << "IBM-3: +NULL:binomial+distortion " << total << '\n';
  for (WordIndex i = 1 ; i <= l ; i++)
    {
      total *= get_fertility(i, al.fert(i)) * (LogProb) factorial(al.fert(i));
      if( verb) cerr << "IBM-3: fertility of " << i << " with factorial " << get_fertility(i, al.fert(i)) * (LogProb) factorial(al.fert(i)) << " -> " << total << '\n';
    }
  for (WordIndex j = 1 ; j <= m ; j++)
    {
      total*= get_t(al(j), j) ;
      massert( get_t(al(j), j)>=PROB_SMOOTH );
      if( verb) cerr << "IBM-3: t of " << j << " " << al(j) << ": " << get_t(al(j), j)  << " -> " << total << '\n';
      if (al(j))
	{
	  total *= get_d(al(j), j);
	  if( verb) cerr << "IBM-3: d of " << j << ": " << get_d(al(j), j)  << " -> " << total << '\n';
	}
    }
  return total?total:zero;
}


void transpair_model3::computeScores(const alignment&al,vector<double>&d)const
{
  LogProb total1 = 1.0,total2=1.0,total3=1.0,total4=1.0 ;
  total1 *= pow(double(1-p1), m-2.0 * al.fert(0)) * pow(double(p1), double(al.fert(0)));
  for (WordIndex i = 1 ; i <= al.fert(0) ; i++)
    total1 *= double(m - al.fert(0) - i + 1) / (double(DeficientDistortionForEmptyWord?(max(2,int(m))/DeficientDistortionForEmptyWord):i)) ;
  for (WordIndex i = 1 ; i <= l ; i++)
    {
      total2 *= get_fertility(i, al.fert(i)) * (LogProb) factorial(al.fert(i));
    }
  for (WordIndex j = 1 ; j <= m ; j++)
    {
      total3*= get_t(al(j), j) ;
      massert( get_t(al(j), j)>=PROB_SMOOTH );
      if (al(j))
	{
	  total4 *= get_d(al(j), j);
	}
    }
  d.push_back(total1);//5
  d.push_back(total2);//6
  d.push_back(total3);//7
  d.push_back(total4);//8
}
