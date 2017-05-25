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
#ifndef NO_TRAINING
#include "ForwardBackward.h"
#include "Globals.h"
#include "myassert.h"
#include "HMMTables.h"
#include "mymath.h"


double ForwardBackwardTraining(const HMMNetwork&net,Array<double>&g,Array<Array2<double> >&E){
  const int I=net.size1(),J=net.size2(),N=I*J;
  Array<double> alpha(N,0),beta(N,0),sum(J);
  for(int i=0;i<I;i++)
    beta[N-I+i]=net.getBetainit(i);
  double * cur_beta=conv<double>(beta.begin())+N-I-1;
  for(int j=J-2;j>=0;--j)
    for(int ti=I-1;ti>=0;--ti,--cur_beta) {
      const double *next_beta=conv<double>(beta.begin())+(j+1)*I;
      const double *alprob=&net.outProb(j,ti,0),*next_node=&net.nodeProb(0,j+1);
      for(int ni=0;ni<I;++ni,(next_node+=J)){
	massert(cur_beta<next_beta&& &net.outProb(j,ti,ni)==alprob);
	massert(next_node == &net.nodeProb(ni,j+1));
	/*	if( VERB&&(*next_beta)*(*alprob)*(*next_node) )
	  cout << "B= " << (int)(cur_beta-beta.begin()) << " += " << (*next_beta) << "(" 
	  << next_beta-beta.begin() << ") alprob:" << (*alprob) << "  lexprob:" << (*next_node) << endl;*/
	(*cur_beta)+=(*next_beta++)*(*alprob++)*(*next_node);
      }
    }
  for(int i=0;i<I;i++)  
    alpha[i]=net.getAlphainit(i)*net.nodeProb(i,0);
  double* cur_alpha=conv<double>(alpha.begin())+I;
  cur_beta=conv<double>(beta.begin())+I;
  for(int j=1;j<J;j++){
    Array2<double>&e=E[ (E.size()==1)?0:(j-1) ];
    if( (E.size()!=1) || j==1 )
      {
	e.resize(I,I);
	fill(e.begin(),e.end(),0.0);
      }
    
    for(int ti=0;ti<I;++ti,++cur_alpha,++cur_beta) {
      const double * prev_alpha=conv<double>(alpha.begin())+I*(j-1);
      double *cur_e= &e(ti,0);
      double this_node=net.nodeProb(ti,j);
      const double* alprob= &net.outProb(j-1,0,ti);
      for(int pi=0;pi<I;++pi,++prev_alpha,(alprob+=I)){
	massert(prev_alpha<cur_alpha&& &net.outProb(j-1,pi,ti)==alprob);
	massert(&e(ti,pi)==cur_e);
	const double alpha_increment= *prev_alpha*(*alprob)*this_node;
	(*cur_alpha)+=alpha_increment;
	(*cur_e++)+=alpha_increment*(*cur_beta);
      }
    }
  }
  g.resize(N);
  transform(alpha.begin(),alpha.end(),beta.begin(),g.begin(),multiplies<double>());
  double bsum=0,esum=0,esum2;
  for(int i=0;i<I;i++)
    bsum+=beta[i]*net.nodeProb(i,0)*net.getAlphainit(i);
  for(unsigned int j=0;j<(unsigned int)E.size();j++)
    {
      Array2<double>&e=E[j];
      const double *epe=e.end();
      for(const double*ep=e.begin();ep!=epe;++ep)
	esum+=*ep;
    }
  if( J>1 ) 
    esum2=esum/(J-1);
  else
    esum2=0.0;
  if(!(esum2==0.0||mfabs(esum2-bsum)/bsum<1e-3*I))
    cout << "ERROR2: " << esum2 <<" " <<bsum << " " << esum << net << endl;
  double * sumptr=conv<double>(sum.begin());
  double* ge=conv<double>(g.end());
  for(double* gp=conv<double>(g.begin());gp!=ge;gp+=I)
    {
      *sumptr++=normalize_if_possible(gp,gp+I);
      if(bsum && !(mfabs((*(sumptr-1)-bsum)/bsum)<1e-3*I))
	cout << "ERROR: " << *(sumptr-1) << " " << bsum << " " << mfabs((*(sumptr-1)-bsum)/bsum) << ' ' << I << ' ' << J << endl;
    }
  for(unsigned int j=0;j<(unsigned int)E.size();j++)
    {
      Array2<double>&e=E[j];
      double* epe=e.end();
      if( esum )
	for(double*ep=e.begin();ep!=epe;++ep)
	  *ep/=esum;
      else
	for(double*ep=e.begin();ep!=epe;++ep)
	  *ep/=1.0/(max(I*I,I*I*(J-1)));
    }
  if( sum.size() )
    return sum[0];
  else
    return 1.0;
}
void HMMViterbi(const HMMNetwork&net,Array<int>&vit) {
  const int I=net.size1(),J=net.size2();
  vit.resize(J);
  Array<double>g;
  Array<Array2<double> >e(1);
  ForwardBackwardTraining(net,g,e);
  for(int j=0;j<J;j++) {
    double * begin=conv<double>(g.begin())+I*j;
    vit[j]=max_element(begin,begin+I)-begin;
  }
}
void HMMViterbi(const HMMNetwork&net,Array<double>&g,Array<int>&vit) {
  const int I=net.size1(),J=net.size2();
  vit.resize(J);
  for(int j=0;j<J;j++) {
    double* begin=conv<double>(g.begin())+I*j;
    vit[j]=max_element(begin,begin+I)-begin;
  }
}

double HMMRealViterbi(const HMMNetwork&net,Array<int>&vitar,int pegi,int pegj,bool verbose){
  const int I=net.size1(),J=net.size2(),N=I*J;
  Array<double> alpha(N,-1);
  Array<double*> bp(N,(double*)0);  
  vitar.resize(J);
  if( J==0 )
    return 1.0;
  for(int i=0;i<I;i++)
    {
      alpha[i]=net.getAlphainit(i)*net.nodeProb(i,0);
      if( i>I/2 ) 
	alpha[i]=0; // only first empty word can be chosen
      bp[i]=0;
    }
  double *cur_alpha=conv<double>(alpha.begin())+I;
  double **cur_bp=conv<double*>(bp.begin())+I;
  for(int j=1;j<J;j++)
    {
      if( pegj+1==j)
	for(int ti=0;ti<I;ti++)
	  if( (pegi!=-1&&ti!=pegi)||(pegi==-1&&ti<I/2) )
	    (cur_alpha-I)[ti]=0.0;
      for(int ti=0;ti<I;++ti,++cur_alpha,++cur_bp) {
	double* prev_alpha=conv<double>(alpha.begin())+I*(j-1);
	double this_node=net.nodeProb(ti,j);
	const double *alprob= &net.outProb(j-1,0,ti);
	for(int pi=0;pi<I;++pi,++prev_alpha,(alprob+=I)){
	  massert(prev_alpha<cur_alpha&& &net.outProb(j-1,pi,ti)==alprob);
	  const double alpha_increment= *prev_alpha*(*alprob)*this_node;
	  if( alpha_increment> *cur_alpha )
	    {
	      (*cur_alpha)=alpha_increment;
	      (*cur_bp)=prev_alpha;
	    }
	}
      }
    }
  for(int i=0;i<I;i++)
    alpha[N-I+i]*=net.getBetainit(i);
  if( pegj==J-1)
    for(int ti=0;ti<I;ti++)
      if( (pegi!=-1&&ti!=pegi)||(pegi==-1&&ti<I/2) )
	(alpha)[N-I+ti]=0.0;

  int j=J-1;
  cur_alpha=conv<double>(alpha.begin())+j*I;
  vitar[J-1]=max_element(cur_alpha,cur_alpha+I)-cur_alpha;
  double ret= *max_element(cur_alpha,cur_alpha+I);
  while(bp[vitar[j]+j*I])
    {
      cur_alpha-=I;
      vitar[j-1]=bp[vitar[j]+j*I]-cur_alpha;
      massert(vitar[j-1]<I&&vitar[j-1]>=0);
      j--;
    }
  massert(j==0);
  if( verbose )
    {
      cout << "VERB:PEG: " << pegi << ' ' << pegj << endl;
      for(int j=0;j<J;j++)
	cout << "NP " << net.nodeProb(vitar[j],j) << ' ' << "AP " << ((j==0)?net.getAlphainit(vitar[j]):net.outProb(j-1,vitar[j-1],vitar[j])) << " j:" << j << " i:" << vitar[j] << ";  ";
      cout << endl;
    }
  return ret;
}

double MaximumTraining(const HMMNetwork&net,Array<double>&g,Array<Array2<double> >&E){
  Array<int> vitar;
  double ret=HMMRealViterbi(net,vitar);
  const int I=net.size1(),J=net.size2();
  if( E.size()==1 )
    {
      Array2<double>&e=E[0];
      e.resize(I,I);
      g.resize(I*J);
      fill(g.begin(),g.end(),0.0);
      fill(e.begin(),e.end(),0.0);
      for(int i=0;i<J;++i)
	{
	  g[i*I+vitar[i]]=1.0;
	  if( i>0 )
	    e(vitar[i],vitar[i-1])++;
	}
    }
  else
    {
      g.resize(I*J);
      fill(g.begin(),g.end(),0.0);
      for(int i=0;i<J;++i)
	{
	  g[i*I+vitar[i]]=1.0;
	  if( i>0 )
	    {
	      Array2<double>&e=E[i-1];
	      e.resize(I,I);
	      fill(e.begin(),e.end(),0.0);
	      e(vitar[i],vitar[i-1])++;
	    }
	}
    }    
  return ret;
}

#endif

