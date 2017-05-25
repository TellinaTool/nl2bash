/*

Copyright (C) 1998,1999,2000,2001  Franz Josef Och (RWTH Aachen - Lehrstuhl fuer Informatik VI)

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
#include "hmm.h"
#include "Globals.h"
#include "utility.h"
#include "HMMTables.h"
#include "ForwardBackward.h"
#include "Parameter.h"

#define CLASSIFY(i,empty,ianf) bool empty=(i>=l); unsigned int ianf=(i%l);
#define CLASSIFY2(i,ianf) unsigned int ianf=(i%l);


short PredictionInAlignments=0;
short UniformEntryExit=3;
short HMMTrainingSpecialFlags=0;

GLOBAL_PARAMETER2(int,ModelH_Dump_Freq,"HMM DUMP FREQUENCY","th","dump frequency of HMM",PARLEV_OUTPUT,0);

GLOBAL_PARAMETER(short,CompareAlDeps,"emAlignmentDependencies",
		 "lextrain: dependencies in the HMM alignment model. "
		 " &1: sentence length; &2: previous class; &4: previous position; "
		 " &8: French position; &16: French class"
		 ,PARLEV_MODELS,2);
GLOBAL_PARAMETER(double,GLOBALProbabilityForEmpty,"emProbForEmpty",
		 "f-b-trn: probability for empty word",PARLEV_MODELS,0.4);
GLOBAL_PARAMETER(short,SmoothHMM,"emSmoothHMM",
		 "f-b-trn: smooth HMM model &1: modified counts; &2:perform smoothing with -emAlSmooth",PARLEV_SPECIAL,2);
GLOBAL_PARAMETER(double,HMMAlignmentModelSmoothFactor,"emAlSmooth",
		 "f-b-trn: smoothing factor for HMM alignment model (can be ignored by -emSmoothHMM)",PARLEV_SMOOTH,0.2);


/*template<class T>
void smooth_standard(T*a,T*b,double p)
{
  int n=b-a;
  if( n==0 ) 
    return;
  double pp=p/n;
  for(T*i=a;i!=b;++i)
    *i = (1.0-p)*(*i)+pp;
}*/


hmm::hmm(model2& m)
  : model2(m),counts(GLOBALProbabilityForEmpty,ewordclasses,fwordclasses),
    probs(GLOBALProbabilityForEmpty,ewordclasses,fwordclasses)
{  }

void hmm::initialize_table_uniformly(sentenceHandler&){}

int hmm::em_with_tricks(int noIterations)
{
  double minErrors=1.0;int minIter=0;
  string modelName="Hmm",shortModelName="hmm";
  int dumpFreq=ModelH_Dump_Freq;
  time_t it_st, st, it_fn, fn;
  string tfile, afile,afileh, number, alignfile, test_alignfile;
  int pair_no = 0;
  bool dump_files = false ;
  ofstream of2 ;
  st = time(NULL) ;
  sHandler1.rewind();
  cout << "\n==========================================================\n";
  cout << modelName << " Training Started at: " << ctime(&st);
  for(int it=1; it <= noIterations ; it++){
    pair_no = 0;
    it_st = time(NULL) ;
    cout << endl << "-----------\n" << modelName << ": Iteration " << it << '\n';
    dump_files = (dumpFreq != 0) && ((it % dumpFreq) == 0) && !NODUMPS;
    number = "";
    int n = it;
    do{
      number.insert((size_t)0, 1, (char)(n % 10 + '0'));
    } while((n /= 10) > 0);
    tfile = Prefix + ".t" + shortModelName + "." + number ;
    afile = Prefix + ".a" + shortModelName + "." + number ;
    afileh = Prefix + ".h" + shortModelName + "." + number ;
    alignfile = Prefix + ".A" + shortModelName + "." + number ;
    test_alignfile = Prefix + ".tst.A" + shortModelName + "." + number ;
    counts=HMMTables<int,WordClasses>(GLOBALProbabilityForEmpty,ewordclasses,fwordclasses);
    aCountTable.clear();
    initAL();
    em_loop(perp, sHandler1,  dump_files , alignfile.c_str(), trainViterbiPerp, false,it==1,it);
    if( errorsAL()<minErrors )
      {
	minErrors=errorsAL();
        minIter=it;
      }
    if (testPerp && testHandler)
      em_loop(*testPerp, *testHandler, dump_files, test_alignfile.c_str(), *testViterbiPerp,  true,it==1,it); 
    if (dump_files&&OutputInAachenFormat==1)
      tTable.printCountTable(tfile.c_str(),Elist.getVocabList(),Flist.getVocabList(),1);
    tTable.normalizeTable(Elist, Flist);
    aCountTable.normalize(aTable);
    probs=counts;
    cout << modelName << ": ("<<it<<") TRAIN CROSS-ENTROPY " << perp.cross_entropy()
	 << " PERPLEXITY " << perp.perplexity() << '\n';
     if (testPerp && testHandler)
       cout << modelName << ": ("<<it<<") TEST CROSS-ENTROPY " << (*testPerp).cross_entropy()
	    << " PERPLEXITY " << (*testPerp).perplexity() 
	    << '\n';
     cout << modelName << ": ("<<it<<") VITERBI TRAIN CROSS-ENTROPY " << trainViterbiPerp.cross_entropy()
	 << " PERPLEXITY " << trainViterbiPerp.perplexity() << '\n';
    if (testPerp && testHandler)
       cout << modelName << ": ("<<it<<") VITERBI TEST CROSS-ENTROPY " << testViterbiPerp->cross_entropy()
	    << " PERPLEXITY " << testViterbiPerp->perplexity() 
	    << '\n';
    if (dump_files){
      if( OutputInAachenFormat==0)
	tTable.printProbTable(tfile.c_str(),Elist.getVocabList(),Flist.getVocabList(),OutputInAachenFormat);
      ofstream afilestream(afileh.c_str());
      probs.writeJumps(afilestream);
      aCountTable.printTable(afile.c_str());
    }
    it_fn = time(NULL) ;
    cout << "\n" << modelName << " Iteration: " << it<< " took: " <<
      difftime(it_fn, it_st) << " seconds\n";
  } // end of iterations 
  fn = time(NULL) ;
  cout << endl << "Entire " << modelName << " Training took: " << difftime(fn, st) << " seconds\n";
  //cout << "tTable contains " << tTable.getHash().bucket_count() 
  //     << " buckets and  " << tTable.getHash().size() << " entries." ;
  cout << "==========================================================\n";
  return minIter;
}

/*template<class T>
T normalize_if_possible_with_increment(T*a,T*b,int increment)
{
  T sum=0;
  for(T*i=a;i!=b;i+=increment)
    sum+=*i;
  if( sum )
    for(T*i=a;i!=b;i+=increment)
      *i/=sum;
  else
    {
      T factor=increment/(b-a);
      for(T*i=a;i!=b;i+=increment)
	*i=factor;
    }
  return sum;
}*/

void hmm::load_table(const char* aname){
  cout << "Hmm: loading a table not implemented.\n";
  abort();
  ifstream anamefile(aname);
  probs.readJumps(anamefile);
}

HMMNetwork *hmm::makeHMMNetwork(const Vector<WordIndex>& es,const Vector<WordIndex>&fs,bool doInit)const
{
  unsigned int i,j;
  unsigned int l = es.size() - 1;
  unsigned int m = fs.size() - 1;
  unsigned int I=2*l,J=m;
  int IJ=I*J;
  bool DependencyOfJ=(CompareAlDeps&(16|8))||(PredictionInAlignments==2);
  bool DependencyOfPrevAJ=(CompareAlDeps&(2|4))||(PredictionInAlignments==0);
  HMMNetwork *net = new HMMNetwork(I,J);
  fill(net->alphainit.begin(),net->alphainit.end(),0.0);
  fill(net->betainit.begin(),net->betainit.end(),0.0);
  for(j=1;j<=m;j++)
    {
      for(i=1;i<=l;i++)
	net->n(i-1,j-1)=tTable.getProb(es[i], fs[j]) ;
      double emptyContribution=0;  
      emptyContribution=tTable.getProb(es[0],fs[j]) ;
      for(i=1;i<=l;i++)
	net->n(i+l-1,j-1)=emptyContribution;
      net->finalMultiply*=max(normalize_if_possible_with_increment(&net->n(0,j-1),&net->n(0,j-1)+IJ,J),double(1e-12));
    }
  if( DependencyOfJ )
    net->e.resize(m-1);
  else
    net->e.resize(J>1);
  for(j=0;j<net->e.size();j++)
    {
      int frenchClass=fwordclasses.getClass(fs[1+min(int(m)-1,int(j)+1)]);
      net->e[j].resize(I,I,0);
      for(unsigned int i1=0;i1<I;++i1) {
	Array<double> al(l);
	CLASSIFY2(i1,i1real);
	for(unsigned int i2=0;i2<l;i2++)
	  al[i2]=probs.getAlProb(i1real,i2,l,m,ewordclasses.getClass(es[1+i1real]),frenchClass
				 ,j+1);
	normalize_if_possible(conv<double>(al.begin()),conv<double>(al.end()));
	if( SmoothHMM&2 )
	  smooth_standard(conv<double>(al.begin()),conv<double>(al.end()),HMMAlignmentModelSmoothFactor);
	for(unsigned int i2=0;i2<I;i2++) {
	  CLASSIFY(i2,empty_i2,i2real);
	  net->e[j](i1,i2)	    = al[i2real];
	  
	  if( empty_i2 )
	    if(i1real!=i2real)
	      {
		net->e[j](i1,i2)=0;
	      }
	    else
	      {
		net->e[j](i1,i2)=doInit?al[0]:(probs.getProbabilityForEmpty()); // make first HMM iteration like IBM-1
	      }
	}
	normalize_if_possible(&net->e[j](i1,0),&net->e[j](i1,0)+I);
      }
    }
  if( doInit )
    {
      for(unsigned int i=0;i<I;++i)
	{
	  net->alphainit[i]=net->betainit[i]=(i<I/2)?1:(2.0/I);
	  net->betainit[i]=1.0;
	}
    }
  else
    {
      if( DependencyOfPrevAJ==0 )
	{
	  for(i=0;i<I;i++)
	    {
	      CLASSIFY2(i,ireal);
	      net->alphainit[i]=probs.getAlProb(-1,ireal,l,m,0,fwordclasses.getClass(fs[1+0]),0);
	    }
	}
      else
	{
	  if( UniformEntryExit&2 )probs.getBetaInit(I,net->betainit);
	  if( UniformEntryExit&1 )probs.getAlphaInit(I,net->alphainit);
	}
    }
  massert( net->alphainit.size()==I );massert( net->betainit.size()==I );
  normalize_if_possible(conv<double>(net->alphainit.begin()),conv<double>(net->alphainit.end()));
  normalize_if_possible(conv<double>(net->betainit.begin()),conv<double>(net->betainit.end()));
  transform(net->betainit.begin(),net->betainit.end(),net->betainit.begin(),bind1st(multiplies<double>(),2*l));
  return net;
}
extern float MINCOUNTINCREASE;

void hmm::em_loop(Perplexity& perp, sentenceHandler& sHandler1, 
		  bool dump_alignment, const char* alignfile, Perplexity& viterbi_perp, 
		     bool test,bool doInit,int 
)
{
  WordIndex i, j, l, m ;
  double cross_entropy;
  int pair_no=0 ;
  perp.clear();
  viterbi_perp.clear();
  ofstream of2;
  // for each sentence pair in the corpus
  if (dump_alignment||FEWDUMPS )
    of2.open(alignfile);
  sentPair sent ;
  sHandler1.rewind();
  while(sHandler1.getNextSentence(sent)){
    const Vector<WordIndex>& es = sent.get_eSent();
    const Vector<WordIndex>& fs = sent.get_fSent();
    const float so  = sent.getCount();
    l = es.size() - 1;
    m = fs.size() - 1;
    cross_entropy = log(1.0);
    Vector<WordIndex> viterbi_alignment(fs.size());

    unsigned int I=2*l,J=m;
    bool DependencyOfJ=(CompareAlDeps&(16|8))||(PredictionInAlignments==2);
    bool DependencyOfPrevAJ=(CompareAlDeps&(2|4))||(PredictionInAlignments==0);
    HMMNetwork *net=makeHMMNetwork(es,fs,doInit);
    Array<double> gamma;
    Array<Array2<double> > epsilon(DependencyOfJ?(m-1):1);
    double trainProb;
      trainProb=ForwardBackwardTraining(*net,gamma,epsilon);
    if( !test )
      {
	double *gp=conv<double>(gamma.begin());
	for(unsigned int i2=0;i2<J;i2++)for(unsigned int i1=0;i1<I;++i1,++gp)
	  if( *gp>MINCOUNTINCREASE )
	    {
	      COUNT add= *gp*so;
	      if( i1>=l )
		{
		  tTable.incCount(es[0],fs[1+i2],add);
		  aCountTable.getRef(0,i2+1,l,m)+=add;
		}
	      else
		{
		  tTable.incCount(es[1+i1],fs[1+i2],add);
		  aCountTable.getRef(1+i1,1+i2,l,m)+=add;
		}
	    }
	double p0c=0.0,np0c=0.0;
	for(unsigned int jj=0;jj<epsilon.size();jj++)
	  {
	    int frenchClass=fwordclasses.getClass(fs[1+min(int(m)-1,int(jj)+1)]);
	    double *ep=epsilon[jj].begin();
	    if( ep )
	      {
		//for(i=0;i<I;i++)
		//  normalize_if_possible_with_increment(ep+i,ep+i+I*I,I);
		//		for(i=0;i<I*I;++i)
		//  ep[i] *= I;
		//if( DependencyOfJ )
		//  if( J-1 )
		//    for(i=0;i<I*I;++i)
		//      ep[i] /= (J-1);
		double mult=1.0;
		mult*=l;
		//if( DependencyOfJ && J-1)
		//  mult/=(J-1);
		for(i=0;i<I;i++)
		  {
		    for(unsigned int i_bef=0;i_bef<I;i_bef++,ep++)
		      {
			CLASSIFY(i,i_empty,ireal);
			CLASSIFY2(i_bef,i_befreal);
			if( i_empty )
			  p0c+=*ep * mult;
			else
			  {
			    counts.addAlCount(i_befreal,ireal,l,m,ewordclasses.getClass(es[1+i_befreal]),
					      frenchClass ,jj+1,*ep * mult,0.0);
			    np0c+=*ep * mult; 
			  }
			massert( &epsilon[jj](i,i_bef)== ep);
		      }
		  }
	      }
	  }
	double *gp1=conv<double>(gamma.begin()),*gp2=conv<double>(gamma.end())-I;
	Array<double>&ai=counts.doGetAlphaInit(I);
	Array<double>&bi=counts.doGetBetaInit(I);
	int firstFrenchClass=(fs.size()>1)?(fwordclasses.getClass(fs[1+0])):0;
	for(i=0;i<I;i++,gp1++,gp2++)
	  {
	    CLASSIFY(i,i_empty,ireal);
	    ai[i]+= *gp1;
	    bi[i]+= *gp2;
	    if( DependencyOfPrevAJ==0 )
	      {
		if( i_empty )
		  p0c+=*gp1;
		else
		  {
		    counts.addAlCount(-1,ireal,l,m,0,firstFrenchClass,0,*gp1,0.0);
		    np0c+=*gp1;
		  }
	      }
	  }
    if( Verbose )
      cout << "l: " << l << "m: " << m << " p0c: " << p0c << " np0c: " << np0c << endl;
      }
    cross_entropy+=log(max(trainProb,1e-100))+log(max(net->finalMultiply,1e-100));
    Array<int>vit;
    double viterbi_score=1.0;
    if( (HMMTrainingSpecialFlags&1) )
      HMMViterbi(*net,gamma,vit);
    else
      viterbi_score=HMMRealViterbi(*net,vit);
    for(j=1;j<=m;j++)
      {
	viterbi_alignment[j]=vit[j-1]+1;
	if( viterbi_alignment[j]>l)
	  viterbi_alignment[j]=0;
      }
    sHandler1.setProbOfSentence(sent,cross_entropy);
    perp.addFactor(cross_entropy, so, l, m,1);
    viterbi_perp.addFactor(log(viterbi_score)+log(max(net->finalMultiply,1e-100)), so, l, m,1);
    if( Verbose )
      cout << "Viterbi-perp: " << log(viterbi_score) << ' ' << log(max(net->finalMultiply,1e-100)) << ' ' << viterbi_score << ' ' << net->finalMultiply << ' ' << *net << "gamma: " << gamma << endl;
    delete net;net=0;
    if (dump_alignment||(FEWDUMPS&&sent.getSentenceNo()<1000) )
      printAlignToFile(es, fs, Elist.getVocabList(), Flist.getVocabList(), of2, viterbi_alignment, sent.getSentenceNo(), viterbi_score);
    addAL(viterbi_alignment,sent.getSentenceNo(),l);    
    pair_no++;
  } /* of while */
  sHandler1.rewind();
  perp.record("HMM");
  viterbi_perp.record("HMM");
  errorReportAL(cout,"HMM");
}

#include "HMMTables.cpp"
template class HMMTables<int,WordClasses>;
 
