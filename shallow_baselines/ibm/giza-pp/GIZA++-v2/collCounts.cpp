/*

Copyright (C) 1999,2000,2001  Franz Josef Och (RWTH Aachen - Lehrstuhl fuer Informatik VI)

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
#include "alignment.h"
#include "transpair_model3.h"
#include <map>
#include "collCounts.h"
#include "MoveSwapMatrix.h"
#include "D5Tables.h"
#include "transpair_model5.h"
#include "transpair_modelhmm.h"
#include "Parameter.h"

extern float COUNTINCREASE_CUTOFF_AL;
// unifies collectCountsOverAlignments and findAlignmentNeighborhood FJO-20/07/99
template<class TRANSPAIR>
int collectCountsOverNeighborhood(const MoveSwapMatrix<TRANSPAIR>&msc,LogProb ascore,Array2<LogProb,Vector<LogProb> >&dtcount,Array2<LogProb,Vector<LogProb> >&ncount,LogProb&p1count,LogProb&p0count,LogProb&total_count)
{
  int nAl=0;
  const PositionIndex l=msc.get_l(),m=msc.get_m();
  Array2<LogProb,Vector<LogProb> > cmove(l+1,m+1),cswap(l+1,m+1);
  Vector<LogProb> negmove(m+1),negswap(m+1),plus1fert(l+1),minus1fert(l+1);
  LogProb total_move,total_swap;
  if( msc.isCenterDeleted()==0 )
    {
      total_move+=ascore;
      nAl++;
    }
  for(PositionIndex j=1;j<=m;j++)
      for(PositionIndex i=0;i<=l;i++)
	if( msc(j)!=i && !msc.isDelMove(i,j) )
	  {
	    LogProb newscore=ascore*msc.cmove(i,j);
	    total_move+=newscore;
	    nAl++;
	    cmove(i,j)+=newscore;
	    negmove[j]+=newscore;
	    plus1fert[i]+=newscore;
	    minus1fert[msc(j)]+=newscore;
	  }
  for(PositionIndex j1=1;j1<=m;j1++)
    for(PositionIndex j2=j1+1;j2<=m;j2++)
      if( msc(j1)!=msc(j2) && !msc.isDelSwap(j1,j2) )
	{
	  LogProb newscore=ascore*msc.cswap(j1,j2);
	  total_swap+=newscore;
	  nAl++;
	  cswap(msc(j1),j2)+=newscore;
	  cswap(msc(j2),j1)+=newscore;
	  negswap[j1]+=newscore; 
	  negswap[j2]+=newscore;
	}
  total_count+=total_move+total_swap;
  for(PositionIndex j=1;j<=m;j++)
    for(PositionIndex i=0;i<=l;i++)
      dtcount(i,j) += ((i==msc(j)) ? (total_count-(negmove[j]+negswap[j])) : (cswap(i,j)+cmove(i,j)));
  for(PositionIndex i=1;i<=l;i++)
    {
      LogProb temp=minus1fert[i]+plus1fert[i];
      if( msc.fert(i)<MAX_FERTILITY )
	ncount(i,msc.fert(i))+=total_count-temp;
      if(msc.fert(i)>0&&msc.fert(i)-1<MAX_FERTILITY)
	ncount(i,msc.fert(i)-1)+=minus1fert[i];
      else
	if( minus1fert[i]!=0.0 )
	  cerr << "ERROR: M1Fa: " << minus1fert[i] << ' ' << i << ' ' << msc.fert(i)<< endl;
      if(msc.fert(i)+1<MAX_FERTILITY) 
	ncount(i,msc.fert(i)+1)+=plus1fert[i];
    }
  LogProb temp=minus1fert[0]+plus1fert[0];
  p1count += (total_count-temp)*(LogProb)msc.fert(0);
  p0count += (total_count-temp)*(LogProb)(m-2*msc.fert(0));
  if( msc.fert(0)>0 )
    {
      p1count += (minus1fert[0])*(LogProb)(msc.fert(0)-1);
      p0count += (minus1fert[0])*(LogProb)(m-2*(msc.fert(0)-1));
    }
  else 
    if( minus1fert[0]!=0.0 )
      cerr << "ERROR: M1Fb: " << minus1fert[0] << endl;
  if(int(m)-2*(int(msc.fert(0))+1)>=0)
    {
      p1count += (plus1fert[0])*(LogProb)(msc.fert(0)+1);
      p0count += (plus1fert[0])*(LogProb)(m-2*(msc.fert(0)+1));
    }
  msc.check();
  return nAl;
};

template<class TRANSPAIR>
double collectCountsOverNeighborhoodForSophisticatedModels(const MoveSwapMatrix<TRANSPAIR>&,LogProb,void*)
{
  return 0.0;
}

template<class TRANSPAIR>
void _collectCountsOverNeighborhoodForSophisticatedModels(const MoveSwapMatrix<TRANSPAIR>&Mmsc,const alignment&msc,const TRANSPAIR&ef,LogProb normalized_ascore,d4model*d4Table)
{
  Mmsc.check();
  const PositionIndex m=msc.get_m(),l=msc.get_l();
  for(PositionIndex j=1;j<=m;++j)
    if( msc(j)!=0 )
      if( msc.get_head(msc(j))==j)
	{
	  int ep=msc.prev_cept(msc(j));
	  //massert( &d4Table->getCountRef_first(j,msc.get_center(ep),d4Table->ewordclasses.getClass(ef.get_es(ep)),d4Table->fwordclasses.getClass(ef.get_fs(j)),l,m) ==  ef.getCountFirst(ep,j,msc.get_center(ep)));
	  d4Table->getCountRef_first(j,msc.get_center(ep),d4Table->ewordclasses.getClass(ef.get_es(ep)),d4Table->fwordclasses.getClass(ef.get_fs(j)),l,m)+=normalized_ascore;
	}
      else
	{
	  //massert( &d4Table->getCountRef_bigger(j,msc.prev_in_cept(j),0,d4Table->fwordclasses.getClass(ef.get_fs(j)),l,m) == ef.getCountSecond(j,msc.prev_in_cept(j) ));
	  d4Table->getCountRef_bigger(j,msc.prev_in_cept(j),0,d4Table->fwordclasses.getClass(ef.get_fs(j)),l,m)+=normalized_ascore;
	}
}

template<class TRANSPAIR>
void _collectCountsOverNeighborhoodForSophisticatedModels(const MoveSwapMatrix<TRANSPAIR>&Mmsc,const alignment&msc,const TRANSPAIR&ef,LogProb normalized_ascore,d5model*d5Table)
{
  Mmsc.check();
  _collectCountsOverNeighborhoodForSophisticatedModels(Mmsc,msc,ef,normalized_ascore,&d5Table->d4m);
  Mmsc.check();
  const PositionIndex m=msc.get_m(),l=msc.get_l();
  PositionIndex prev_cept=0;
  PositionIndex vac_all=m;
  Vector<char> vac(m+1,0);
  for(PositionIndex i=1;i<=l;i++)
    {
      PositionIndex cur_j=msc.als_i[i]; 
      PositionIndex prev_j=0;
      PositionIndex k=0;
      if(cur_j) { // process first word of cept
	k++;
	d5Table->getCountRef_first(vacancies(vac,cur_j),vacancies(vac,msc.get_center(prev_cept)),
				   d5Table->fwordclasses.getClass(ef.get_fs(cur_j)),l,m,vac_all-msc.fert(i)+k)+=normalized_ascore;
	vac_all--;
	assert(vac[cur_j]==0);
	vac[cur_j]=1;
	Mmsc.check();
	prev_j=cur_j;
	cur_j=msc.als_j[cur_j].next;
      }
      while(cur_j) { // process following words of cept
	k++;
	int vprev=vacancies(vac,prev_j);
	d5Table->getCountRef_bigger(vacancies(vac,cur_j),vprev,d5Table->fwordclasses.getClass(ef.get_fs(cur_j)),l,m,vac_all-vprev/*war weg*/-msc.fert(i)+k)+=normalized_ascore;
	vac_all--;
	vac[cur_j]=1;
	Mmsc.check();
	prev_j=cur_j;
	cur_j=msc.als_j[cur_j].next;
      }
      assert(k==msc.fert(i));
      if( k )
	prev_cept=i;
    }
  assert(vac_all==msc.fert(0));
}

extern int NumberOfAlignmentsInSophisticatedCountCollection;

template<class TRANSPAIR,class MODEL>
double collectCountsOverNeighborhoodForSophisticatedModels(const MoveSwapMatrix<TRANSPAIR>&msc,LogProb normalized_ascore,MODEL*d5Table)
{
  const PositionIndex m=msc.get_m(),l=msc.get_l();
  alignment x(msc);
  double sum=0;
  msc.check();
  if( !msc.isCenterDeleted() )
    {
      _collectCountsOverNeighborhoodForSophisticatedModels<TRANSPAIR>(msc,x,msc.get_ef(),normalized_ascore,d5Table);
      NumberOfAlignmentsInSophisticatedCountCollection++;
      sum+=normalized_ascore;
    }
  msc.check();
  for(WordIndex j=1;j<=m;j++)for(WordIndex i=0;i<=l;i++)
    {
      WordIndex old=x(j);
      if( i!=old&& !msc.isDelMove(i,j) )
	{
	  msc.check();
	  double c=msc.cmove(i,j)*normalized_ascore;
	  if(c > COUNTINCREASE_CUTOFF_AL )
	    {
	      x.set(j,i);
	      _collectCountsOverNeighborhoodForSophisticatedModels<TRANSPAIR>(msc,x,msc.get_ef(),c,d5Table);
	      NumberOfAlignmentsInSophisticatedCountCollection++;
	      x.set(j,old);
	      sum+=c;
	    }
	  msc.check();
	}
    }      
  for(PositionIndex j1=1;j1<=m;j1++)
    for(PositionIndex j2=j1+1;j2<=m;j2++)
      if( msc(j1)!=msc(j2) && !msc.isDelSwap(j1,j2) )
	{
	  double c=msc.cswap(j1,j2)*normalized_ascore;
	  msc.check();
	  if(c > COUNTINCREASE_CUTOFF_AL )
	    {
	      int old1=msc(j1),old2=msc(j2);
	      x.set(j1,old2);
	      x.set(j2,old1);
	      _collectCountsOverNeighborhoodForSophisticatedModels<TRANSPAIR>(msc,x,msc.get_ef(),c,d5Table);
	      NumberOfAlignmentsInSophisticatedCountCollection++;
	      x.set(j1,old1);
	      x.set(j2,old2);
	      sum+=c;
	    }
	  msc.check();
	}
  msc.check();
  return sum;
}

template<class TRANSPAIR,class MODEL>
int collectCountsOverNeighborhood(const Vector<pair<MoveSwapMatrix<TRANSPAIR>*,LogProb> >&smsc,Vector<WordIndex>&es,Vector<WordIndex>&fs,tmodel<COUNT,PROB>&tTable,amodel<COUNT>&aCountTable,amodel<COUNT>&dCountTable,nmodel<COUNT>&nCountTable,double&p1count,double&p0count,LogProb&_total,float count,bool addCounts,MODEL*d4Table)
{
  int nAl=0;
  const PositionIndex l=es.size()-1,m=fs.size()-1;
  Array2<LogProb,Vector<LogProb> > dtcount(l+1,m+1),ncount(l+1,MAX_FERTILITY+1);
  LogProb p0=0,p1=0,all_total=0;
  for(unsigned int i=0;i<smsc.size();++i)
    {
      LogProb this_total=0;
      nAl+=collectCountsOverNeighborhood(*smsc[i].first,smsc[i].second,dtcount,ncount,p1,p0,this_total);
      all_total+=this_total;
    }
  _total=all_total;
  all_total/=(double)count;
  double sum2=0;
  if( addCounts && d4Table )
    {
      for(unsigned int i=0;i<smsc.size();++i)
	{
	  //for(WordIndex j=1;j<=m;j++)for(WordIndex ii=0;ii<=l;ii++)
	  //  (*smsc[i].first).cmove(ii,j);
	  sum2+=collectCountsOverNeighborhoodForSophisticatedModels(*smsc[i].first,smsc[i].second/all_total,d4Table);    
	}
      if(!(fabs(count-sum2)<0.05))
	cerr << "WARNING: DIFFERENT SUMS: (" << count << ") (" << sum2 << ")\n";
    }
 if( addCounts )
    {
      for(PositionIndex i=0;i<=l;i++) 
	{
	  for(PositionIndex j=1;j<=m;j++)
	    {
	      LogProb ijadd=dtcount(i,j)/all_total;
	      if( ijadd>COUNTINCREASE_CUTOFF_AL )
		{
		  tTable.incCount(es[i],fs[j],ijadd);
		  dCountTable.getRef(j,i,l,m)+=ijadd;
		  aCountTable.getRef(i,j,l,m)+=ijadd;
		}
	    }
	  if( i>0 )
	    for(PositionIndex n=0;n<MAX_FERTILITY;n++)
	      nCountTable.getRef(es[i],n)+=ncount(i,n)/all_total;
	}
      p0count+=p0/all_total;
      p1count+=p1/all_total;
    }
 return nAl;
}









