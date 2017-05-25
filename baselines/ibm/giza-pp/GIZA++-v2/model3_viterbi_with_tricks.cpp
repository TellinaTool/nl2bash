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
#include "mystl.h"
#include "model3.h"
#include "collCounts.h"
#include "utility.h"
#include "Globals.h"
#include "D5Tables.h"
#include "transpair_model5.h"
#include "transpair_modelhmm.h"
#include "myassert.h"
#include "Parameter.h"

GLOBAL_PARAMETER(float,PrintN,"nbestalignments","for printing the n best alignments",PARLEV_OUTPUT,0);

const short LogHillClimb=0,LogPeg=0;
const short UseHMMViterbiAlignmentIfPossible=1;
short DoViterbiTraining=0;

GLOBAL_PARAMETER(int,VerboseSentence,"VerboseSentence","number of sentence for which a lot of information should be printed (negative: no output)",PARLEV_OUTPUT,-10);
GLOBAL_PARAMETER(double,PEGGED_CUTOFF,"PEGGED_CUTOFF","relative cutoff probability for alignment-centers in pegging",PARLEV_OPTHEUR,3e-2);
GLOBAL_PARAMETER2(float, COUNTINCREASE_CUTOFF_AL,"COUNTINCREASE CUTOFF AL","countCutoffAl","Counts increment cutoff threshold for alignments in training of fertility models",PARLEV_OPTHEUR,1e-5);

int SentNr;
bool UseLinkCache=1;    /// optimization for pegging
int NumberOfAlignmentsInSophisticatedCountCollection;

extern bool ONLYALDUMPS;

int PrintHillClimbWarning=0;
int PrintZeroScoreWarning=0;


LogProb model3::viterbi_model2(const transpair_modelhmm&ef, alignment&output, int 
#ifdef STORE_HMM_ALIGNMENTS
pair_no
#endif
, int i_peg , int j_peg )const
{
  static Vector<pair<alignment,LogProb> > viterbis;
  Vector<int>vit;
  int m=ef.get_m();
  int l=ef.get_l();
  double ret=0.0;
  //#define STORE_HMM_ALIGNMENTS
#ifdef STORE_HMM_ALIGNMENTS
  if( i_peg==-1 && j_peg==-1 && viterbis.size()>pair_no )
    {
      output=viterbis[pair_no].first;
      ret=viterbis[pair_no].second;
      massert( ret==HMMRealViterbi(*ef.net,vit,i_peg-1,j_peg-1)*ef.net->finalMultiply );
    }
  else
    {
      ret=HMMRealViterbi(*ef.net,vit,i_peg-1,j_peg-1)*ef.net->finalMultiply;
      for(int j=1;j<=m;j++)
	{
	  if( vit[j-1]+1>l )
	    output.set(j,0);
	  else
	    output.set(j,vit[j-1]+1);
	  massert( (j==j_peg&&int(output(j))==i_peg) || j_peg!=j);
	}
      if( i_peg==-1 && j_peg==-1 )
	{
	  iassert(viterbis.size()==pair_no);
	  viterbis.push_back(make_pair(output,ret));
	}
    }
#else
  ret=HMMRealViterbi(*ef.net,vit,i_peg-1,j_peg-1)*ef.net->finalMultiply;
  for(int j=1;j<=m;j++)
    {
      if( vit[j-1]+1>l )
	output.set(j,0);
      else
	output.set(j,vit[j-1]+1);
      massert( (j==j_peg&&int(output(j))==i_peg) || j_peg!=j);
      }
#endif
  massert( j_peg==-1 || int(output(j_peg))==i_peg );
  if( j_peg!=-1 )
    massert(int(output(j_peg))==i_peg);
  if( output.valid() )
    return ret;
  else
    {
      return _viterbi_model2(ef,output,i_peg,j_peg);
    }
}

LogProb model3::_viterbi_model2(const transpair_model2&ef, alignment&output, int i_peg, int j_peg)const
{
  WordIndex best_i=0;
  LogProb ss=1;
  PositionIndex l = ef.get_l(), m=ef.get_m();
  Vector<WordIndex> Fert(l+1, (WordIndex)0);
  if ((j_peg != -1) && (i_peg != -1))
    {
      output.set(j_peg, i_peg);
      ss *= ef.get_t(i_peg, j_peg) * ef.get_a(i_peg, j_peg);
      if( ss==0 )
	cerr << "WARNING: already starting is zero: " << ef.get_t(i_peg, j_peg) << " " << ef.get_a(i_peg, j_peg) << '\n';
    }
  else
    ss=1;
  for (PositionIndex j = 1 ; j <= m ; j++)if (int(j) != j_peg)
    {
      LogProb score = 0 ;
      for (PositionIndex i = 0 ; i <= l ; i++)
	{
	  if( Fert[i]+1<MAX_FERTILITY && (i != 0 ||  m>=(2 * (Fert[0] + 1))))
	    {
	      LogProb temp = ef.get_t(i, j) * ef.get_a(i, j);
	      if (temp > score )
		{
		  best_i = i ;
		  score = temp ;
		}
	    } 
	}
      if (score == 0){
	cerr << "WARNING: In searching for model2 best alignment\n";
	cerr << "Nothing was set for target token at position j: " << j << "\n";
	for (PositionIndex i = 0 ; i <= l ; i++){
	  cerr << "i: " << i << "ttable("<<i<<", "<<j<<") = " <<
	    ef.get_t(i, j) << " atable(" << i<<", "<<j<<", "<<
	    l<<", "<<m<<") = "<< ef.get_a(i, j) << " product " <<
	    ef.get_t(i, j) * ef.get_a(i, j) ;
	  if ((Fert[i]+1 < MAX_FERTILITY) && ((i == 0 &&  (m >= 2*(Fert[0]+1)))
					      || (i != 0)))
	    cerr <<"Passed fertility condition \n";
	  else 
	    cerr <<"Failed fertility condition \n";
	}	    
      }
      else
	{
	  output.set(j, best_i);
	  Fert[best_i]++;
	}
      ss *= score;
    } 
  if (ss <= 0){
    //cerr << ef;
    cerr << "WARNING: Model2 viterbi alignment has zero score.\n" ;
    cerr << "Here are the different elements that made this alignment probability zero \n";
    cerr << "Source length " << l << " target length " << m << '\n';
    LogProb gg=1 ; // for debugging only ..... 
    for (PositionIndex j = 1 ; j <= m ; j++)if (int(j) != j_peg){
      LogProb score = 0 ;
      LogProb a = 0, t =0 ;
      for (PositionIndex i = 0 ; i <= l ; i++){
	//	if( Debug_Fert[i]+1<MAX_FERTILITY && (i != 0 ||  m>=(2 * (Debug_Fert[0] + 1)))){
	  LogProb temp = ef.get_t(i, j) * ef.get_a(i, j);
	  if (temp > score ){
	    score = temp ;
	    best_i = i ;
	    a = ef.get_a(i, j);
	    t =  ef.get_t(i, j) ;
	  }
	  //      }
      }
      gg *= score ;
      cerr << "best: fs[" << j << "] "<< j <<"  : es[" << best_i << "] " <<
	best_i << " ,  a: " << ef.get_a(best_i, j) << " t: " << t << " score " << score << "  product : " << gg << " ss " <<
	ss << '\n';
    }
    for(PositionIndex i = 0 ; i <= l ; i++)
      cerr << "Fert["<<i<<"] selected " << Fert[i] << '\n';
  }
  massert(output.valid());
  return ss;
}
LogProb model3::viterbi_model2(const transpair_model3&ef, alignment&output, int pair_no,int i_peg , int j_peg )const
{
  if( h&&UseHMMViterbiAlignmentIfPossible )
    {
      transpair_modelhmm efhmm(ef.E,ef.F,tTable,aTable,dTable,nTable,0.0,0.0,h);
      LogProb ret=viterbi_model2(efhmm,output,pair_no,i_peg,j_peg);
      massert(output.valid());
      return ret;
    }
  return _viterbi_model2(ef,output,i_peg,j_peg);
}

int HillClimbingSteps=0;

template<class TRANSPAIR>
LogProb greedyClimb_WithIBM3Scoring(MoveSwapMatrix<TRANSPAIR>&msc2,int j_peg=-1)
{
  PositionIndex l = msc2.get_l(), m=msc2.get_m();
  int changed=0;
  int iter=0;
  bool hereVERB=0;
  do
    {
      MoveSwapMatrix<typename TRANSPAIR::simpler_transpair_model> msc_IBM3(msc2.get_ef(),alignment(msc2));
      vector<pair<double,OneMoveSwap> > msvec;
      for (PositionIndex j = 1 ; j <= m ; j++)if (int(j) != j_peg)
	{
	  WordIndex aj=msc2(j);
	  for (PositionIndex j1 = j + 1 ; j1 <= m; j1++)
	    if((aj != msc2(j1)) && (int(j1) != j_peg))
	      msvec.push_back(pair<double,OneMoveSwap>(-msc_IBM3.cswap(j,j1),OneMoveSwap(1,j,j1)));
	  for (PositionIndex i = 0 ; i <= l ; i++)
	    if(i != aj &&(i != 0 || (m >= 2 * (msc2.fert(0)+1)))  && msc2.fert(i)+1<MAX_FERTILITY)
	      msvec.push_back(pair<double,OneMoveSwap>(-msc_IBM3.cmove(i,j),OneMoveSwap(2,i,j)));
	}
      sort(msvec.begin(),msvec.end());
      HillClimbingSteps++;
      int iused=-1;
      changed=0;
      for(unsigned int i=0;i<msvec.size()&&changed==0;++i)
	{
	  LogProb csts;
	  const OneMoveSwap &oms=msvec[i].second;
	  if( oms.type==1&&(csts=msc2.cswap(oms.a,oms.b))>1.0001 )
	    {
	      if( hereVERB==1 )
		cerr << "SWAP: " << csts << '\n';
	      msc2.doSwap(oms.a,oms.b);
	      changed=1;
	      iused=i;
	      break;
	    }
	  if( oms.type==2&&(csts=msc2.cmove(oms.a,oms.b))>1.0001 )
	    {
	      if( hereVERB==1 )
		cerr << "MOVE: " << csts << '\n';
	      msc2.doMove(oms.a,oms.b);
	      changed=1;
	      iused=i;
	      break;
	    }
	}
      if( ++iter>30 )
	{
	  //msc2.ef.verboseTP=1;
	  hereVERB=1;
	  cerr << "ERROR: more than 30 iterations in hill-climbing: " << iused 
	       << " improvement: " << msvec[iused].first << " value:" << msvec[iused].second 
	       << '\n' << msc2 << '\n';
	  for(int a=0;a<20;++a)
	    cout << a << ' ' << msvec[a].first << ' ' << msvec[a].second << '\n';
	  //cerr << msvec << '\n';
	}
      if( iter>50 )
	break;
    } while(changed);
  return msc2.get_ef().prob_of_target_and_alignment_given_source(msc2);  
}

template<class TRANSPAIR>
LogProb greedyClimb(MoveSwapMatrix<TRANSPAIR>&msc2, int j_peg = -1)
{
  if( msc2.get_ef().greedyHillClimbing()==1 )
    return greedyClimb_WithIBM3Scoring(msc2,j_peg);
  PositionIndex l = msc2.get_l(), m=msc2.get_m();
  int changed=0;
  do 
    {
      HillClimbingSteps++;
      changed=0;
      for (PositionIndex j = 1 ; j <= m ; j++)if (int(j) != j_peg)
	{
	  WordIndex aj=msc2(j);
	  for (PositionIndex j1 = j + 1 ; j1 <= m; j1++)if((aj != msc2(j1)) && (int(j1) != j_peg)&&msc2.cswap(j, j1) > 1.0)
	    msc2.doSwap(j, j1), changed=1;
	  for (PositionIndex i = 0 ; i <= l ; i++)if(i != aj &&(i != 0 || (m >= 2 * (msc2.fert(0)+1)))  && msc2.fert(i)+1<MAX_FERTILITY && msc2.cmove(i, j)>1.0)
	    msc2.doMove(i, j), changed=1;
	}
    } while (changed);
  return msc2.get_ef().prob_of_target_and_alignment_given_source(msc2);
}

template<class TRANSPAIR>
LogProb hillClimb_std(MoveSwapMatrix<TRANSPAIR>&msc2, int= -1,int j_peg = -1)
{
  if( msc2.isLazy() )
    return greedyClimb_WithIBM3Scoring(msc2,j_peg);                             
  if( LogHillClimb>1 )
    cout << msc2 << '\n';
  PositionIndex l = msc2.get_l(), m=msc2.get_m();
  int changes=0;
  int best_change_type=-1, best_change_v1=-1, best_change_v2=-1;
  do 
    {
      HillClimbingSteps++;
      LogProb best_change_so_far = 1.00001 ;  
      best_change_type=0;
      for (PositionIndex j = 1 ; j <= m ; j++)if (int(j) != j_peg)
	{
	  WordIndex aj=msc2(j);
	  for (PositionIndex j1 = j + 1 ; j1 <= m; j1++)if((aj != msc2(j1)) && (int(j1) != j_peg))
	    {
	      LogProb change = msc2.cswap(j, j1);
	      if (change > best_change_so_far)
		{
		  best_change_so_far = change ;
		  best_change_type=1;
		  best_change_v1=j;
		  best_change_v2=j1;
		  if( LogHillClimb )
		    cerr << "CLIMB: " << best_change_type << " " << best_change_v1 << " " << best_change_v2 << " " << best_change_so_far << msc2 << '\n';
		  massert(msc2.get_ef().isSubOptimal()==1);
		} 
	    } 
	  for (PositionIndex i = 0 ; i <= l ; i++)if(i != aj &&(i != 0 || (m >= 2 * (msc2.fert(0)+1))) && msc2.fert(i)+1<MAX_FERTILITY)
	    {
	      LogProb change = msc2.cmove(i, j);
	      if (change > best_change_so_far)
		{ 
		  best_change_so_far = change ;
		  best_change_type=2;
		  best_change_v1=j;
		  best_change_v2=i;
		  if( LogHillClimb )
		    cerr << "CLIMB: " << best_change_type << " " << best_change_v1 << " " << best_change_v2 << " " << best_change_so_far << msc2 << '\n';
		  massert(msc2.get_ef().isSubOptimal()==1);
		} 
	    }
	}
      if (best_change_type==1)
	{
	  msc2.doSwap(best_change_v1, best_change_v2);
	  if( LogHillClimb )
	    cerr << "SW-CLIMB-DONE: " << j_peg << msc2 << '\n';
	}
      if (best_change_type==2)
	{
	  msc2.doMove(best_change_v2, best_change_v1);
	  if( LogHillClimb )
	    cerr << "MO-CLIMB-DONE: " << j_peg << msc2 << '\n';
	}
      changes++;
      if( changes>40 )
	{
	  if( PrintHillClimbWarning++<1000 )
	    cerr << "WARNING: already " << changes << " iterations in hillclimb: " << best_change_so_far << " " << best_change_type << " " << best_change_v1 << " " << best_change_v2 << '\n';
	  else if (PrintHillClimbWarning==1000)
	    cerr << "ERROR: too many hill climbing warnings => I do not print more.\n";
	}
      if(changes>60 )
	{
	  cerr << msc2 << '\n';
	  break;
	}
    } while (best_change_type);
  return msc2.get_ef().prob_of_target_and_alignment_given_source(msc2);
}

template<class MODEL_TYPE>
bool extendCenterList(Vector<pair<MoveSwapMatrix<MODEL_TYPE>*,LogProb> >&setOfGoodCenters,MoveSwapMatrix<MODEL_TYPE> *msc,double peggedAlignmentScore)
{
  unsigned int l=msc->get_ef().get_l();
  set<OneMoveSwap> alreadyCovered;
  for(unsigned int nr=0;nr<setOfGoodCenters.size();nr++)
    makeOneMoveSwap(*setOfGoodCenters[nr].first,*msc,alreadyCovered);
  for(set<OneMoveSwap>::const_iterator i=alreadyCovered.begin();i!=alreadyCovered.end();++i)
    {
      if( i->type==1||i->type==4)
	msc->delCenter();
      if( i->type==1 )
	{
	  for(unsigned int ii=0;ii<=l;++ii)
	    if( (*msc)(i->a)!=ii )
	      msc->delMove(ii,i->a);
	}
      else if( i->type==2||i->type==4 )
	  msc->delSwap(i->a,i->b);
      else if( i->type==3 )
	  msc->delMove(i->b,i->a);
      else abort();
    }   
  setOfGoodCenters.push_back(make_pair(msc,peggedAlignmentScore));
  return 1;
}

bool OldLog=0;
short OldLogPeg=0,OldLogHillClimb=0;
class Als
{
public:
  int s,a,b;
  double v;
  Als(int _s,int _a,int _b,double _v)
    : s(_s),a(_a),b(_b),v(_v) {}
};

inline bool operator<(const Als&x,const Als&y)
{return x.v>y.v;}

template<class MODEL_TYPE, class ADDITIONAL_MODEL_DATA_IN,class ADDITIONAL_MODEL_DATA_OUT>
void model3::viterbi_loop_with_tricks(Perplexity& perp, Perplexity& viterbiPerp, sentenceHandler& sHandler1, 
				      bool dump_files, const char* alignfile, 
				      bool collect_counts, string model, bool final,
				      ADDITIONAL_MODEL_DATA_IN*dm_in,
				      ADDITIONAL_MODEL_DATA_OUT*dm_out)
{
  ofstream *writeNBestErrorsFile=0;
  if( (dump_files||FEWDUMPS)&&PrintN&&ReferenceAlignment.size()>0 )
    {
      string x=alignfile+string("NBEST");
      writeNBestErrorsFile= new ofstream(x.c_str());
    }
  ofstream *of3=0;
  PositionIndex i, j, l, m ;
  ofstream of2;
  int pair_no;
  HillClimbingSteps=0;
  NumberOfAlignmentsInSophisticatedCountCollection=0;
  if (dump_files||FEWDUMPS||(final&&(ONLYALDUMPS)) )
    of2.open(alignfile);
  if( dump_files&&PrintN&&final )
    {
      string x=alignfile+string("NBEST");
      of3= new ofstream(x.c_str());
    }
  pair_no = 0 ; // sentence pair number 
  // for each sentence pair in the corpus
  perp.clear() ; // clears cross_entrop & perplexity 
  viterbiPerp.clear() ; // clears cross_entrop & perplexity 
  sentPair sent ;
  int NCenter=0,NHillClimbed=0,NAlignment=0,NTotal=0,NBetterByPegging=0;
  while(sHandler1.getNextSentence(sent)){
    if( sent.eSent.size()==1||sent.fSent.size()==1 )
      continue;
    SentNr=sent.sentenceNo;
    Vector<WordIndex>& es = sent.eSent;
    Vector<WordIndex>& fs = sent.fSent;
    const float count  = sent.getCount();    
    if ((sent.sentenceNo % 10000) == 0)
      cerr <<sent.sentenceNo << '\n'; 
    time_t sent_s = time(NULL) ;
    pair_no++ ;
    l = es.size() - 1 ;
    m = fs.size() - 1 ;
    if (Log){
      logmsg << "Processing sentence pair:\n\t";
      printSentencePair(es, fs, logmsg);
      for (i = 0 ; i <= l ; i++)
	  logmsg << Elist.getVocabList()[es[i]].word << " ";
	logmsg << "\n\t";
	for (j = 1 ; j <= m ; j++)
	  logmsg << Flist.getVocabList()[fs[j]].word << " ";
	logmsg << "\n";
      } 

      LogProb align_total_count=0;
      alignment viterbi2alignment(l,m);
      MODEL_TYPE ef(es,fs,tTable,aTable,dTable,nTable,p1,p0,dm_in);
      viterbi_model2(ef,viterbi2alignment,pair_no-1);
      Vector<pair<MoveSwapMatrix<MODEL_TYPE>*,LogProb> >setOfGoodCenters(1);
      set<alignment> alignments;
      MoveSwapMatrix<MODEL_TYPE> *best = (setOfGoodCenters[0].first  = new MoveSwapMatrix<MODEL_TYPE>(ef, viterbi2alignment));
      MoveSwapMatrix<MODEL_TYPE> _viterbi(*best), *viterbi=&_viterbi; // please, don't delete this line (FJO)
      if (Log)
	logmsg << "VITERBI: " << alignment(_viterbi);
      if( ef.isSubOptimal() )
	setOfGoodCenters[0].second = hillClimb_std(*best);
      else
	{
	  setOfGoodCenters[0].second = best->get_ef().prob_of_target_and_alignment_given_source(*best);
	  if( setOfGoodCenters[0].second==0 )
	    {
	      cerr << "PROBLEM: alignment is 0.\n";
	      best->get_ef().prob_of_target_and_alignment_given_source(*best,1);
	    }
	}
      int bestAlignment=0;


      for(unsigned int i=0;i<setOfGoodCenters.size();++i)
	setOfGoodCenters[i].first->check();
      alignments.insert(*best); 
      if (setOfGoodCenters[bestAlignment].second <= 0){
	if( PrintZeroScoreWarning++<100 )
	  {
	    cerr << "WARNING: Hill Climbing yielded a zero score viterbi alignment for the following pair:\n";
	    cerr << alignment(*setOfGoodCenters[bestAlignment].first) ;
	    printSentencePair(es, fs, cerr);      
	    if(Log){
	      logmsg << "WARNING: Hill Climbing yielded a zero score viterbi alignment for the following pair:\n";
	      printSentencePair(es, fs, logmsg);
	    }
	  }
	else if(PrintZeroScoreWarning==100) 
	  {
	    cerr << "ERROR: too many zero score warnings => no additional one will be printed\n";
	  }
	setOfGoodCenters[bestAlignment].second=1e-300;
	continue;
      }
      int nHillClimbed=1,nAlignment=1;
      bool flagBetterByPegging=0;
      if ( Peg )
	{
	  const MoveSwapMatrix<MODEL_TYPE> *useMatrix=viterbi;  // it is faster using 'best', ... (FJO)
	  Array2<short, vector<short> > linkCache(l+1, m+1, false);
	  if(UseLinkCache)for(unsigned int j=1;j<=m;j++)linkCache((*useMatrix)(j), j)=1;
	  for(PositionIndex j=1;j<=m;j++)for(PositionIndex i=0;i<=l;i++)
	    {
	      nAlignment++;
	      if( i!=(*useMatrix)(j) && (UseLinkCache==0||linkCache(i,j)==0) && 
		  ef.get_t(i,j)>ef.get_t((*useMatrix)(j),j)*PEGGED_CUTOFF && 
		  (i != 0 || (m >= 2 * (useMatrix->fert(0)+1))))
		{
		  MoveSwapMatrix<MODEL_TYPE> *BESTPEGGED=0;
		  LogProb peggedAlignmentScore;
		  nHillClimbed++;
		  if( ef.isSubOptimal() )
		    {
		      BESTPEGGED = new MoveSwapMatrix<MODEL_TYPE>(*useMatrix);
		      BESTPEGGED->doMove(i, j);
		      peggedAlignmentScore= hillClimb_std(*BESTPEGGED, i,j);
		    }
		  else
		    {
		      alignment pegAlignment(l,m);
		      peggedAlignmentScore=viterbi_model2(ef,pegAlignment,pair_no-1,i,j);
		      BESTPEGGED = new MoveSwapMatrix<MODEL_TYPE>(ef,pegAlignment);
		      massert( pegAlignment(j)==i );
		    }
		  if(UseLinkCache)
		    for(unsigned int j=1;j<=m;j++)
		      linkCache((*BESTPEGGED)(j), j)=1;
		  if( peggedAlignmentScore>setOfGoodCenters[bestAlignment].second*(LogProb)PEGGED_CUTOFF && alignments.count(*BESTPEGGED)==0 )
		    {
		      if(extendCenterList(setOfGoodCenters,BESTPEGGED,peggedAlignmentScore))
			{
			  alignments.insert(*BESTPEGGED);
			  if( peggedAlignmentScore>1.00001*setOfGoodCenters[bestAlignment].second )
			    {
			      if( LogPeg )
				{
				  cerr << "found better alignment by pegging " << pair_no << " " << peggedAlignmentScore/setOfGoodCenters[bestAlignment].second << '\n';
				  cerr << "NEW BEST: " << alignment(*BESTPEGGED);
				  cerr << "OLD     : " << alignment(*setOfGoodCenters[bestAlignment].first);
				}
			      flagBetterByPegging=1;
			      bestAlignment=alignments.size()-1;
			    }
			}
		      assert( differences(*BESTPEGGED, *best)!=0 );
		      BESTPEGGED=0;		    }
		  else
		    delete BESTPEGGED;
		}
	    }
	} // end of if(Peg)
      NBetterByPegging+=flagBetterByPegging;
      for(unsigned int i=0;i<setOfGoodCenters.size();++i)
	setOfGoodCenters[i].first->check();
      if( LogPeg>1 )
	cout << "PEGGED: " << setOfGoodCenters.size() << " HILLCLIMBED:" << nHillClimbed << " TOTAL:" << nAlignment << " alignments." << '\n';
      int alTotal=collectCountsOverNeighborhood(setOfGoodCenters,es, fs, tTable, aCountTable, 
						dCountTable, nCountTable, p1_count, p0_count, 
						align_total_count, count, collect_counts, dm_out);
      if( LogPeg>1 )
	{
	  cout << "ALL: " << alTotal << " from " << pow(float(l+1),float(m)) << '\n';
	  massert(alTotal<=pow(double(l+1),double(m)));
	}
      NCenter+=setOfGoodCenters.size();NHillClimbed+=nHillClimbed;NAlignment+=nAlignment;NTotal+=alTotal;
      perp.addFactor(log(double(align_total_count)), count, l, m,0);
      viterbiPerp.addFactor(log(double(setOfGoodCenters[bestAlignment].second)), count, l, m,0);
      massert(log(double(setOfGoodCenters[bestAlignment].second)) <= log(double(align_total_count)));
      if (dump_files||(FEWDUMPS&&sent.sentenceNo<1000)||(final&&(ONLYALDUMPS)) )
	printAlignToFile(es, fs, Elist.getVocabList(), Flist.getVocabList(), of2, (setOfGoodCenters[bestAlignment].first)->getAlignment(), pair_no, 
			 setOfGoodCenters[bestAlignment].second);
      for(unsigned int i=0;i<setOfGoodCenters.size();++i)
	setOfGoodCenters[i].first->check();
      if( of3||(writeNBestErrorsFile&&pair_no<int(ReferenceAlignment.size())) )
	{
	  vector<Als> als;
	  for(unsigned int s=0;s<setOfGoodCenters.size();++s)
	    {
	      const MoveSwapMatrix<MODEL_TYPE>&msc= *setOfGoodCenters[s].first;
	      msc.check();
	      double normalized_ascore=setOfGoodCenters[s].second;
	      if( !msc.isCenterDeleted() )
		als.push_back( Als(s,0,0,normalized_ascore) );
	      
	      for(WordIndex j=1;j<=m;j++)
		for(WordIndex i=0;i<=l;i++)
		  if( i!=msc(j)&& !msc.isDelMove(i,j) )
		    als.push_back( Als(s,i,j,msc.cmove(i,j)*normalized_ascore));
	      for(PositionIndex j1=1;j1<=m;j1++)
		for(PositionIndex j2=j1+1;j2<=m;j2++)
		  if( msc(j1)!=msc(j2) && !msc.isDelSwap(j1,j2) )
		    als.push_back( Als(s,-j1,-j2,msc.cswap(j1,j2)*normalized_ascore));
	    }
	  sort(als.begin(),als.end());
	  double sum=0,sum2=0;
	  for(unsigned int i=0;i<als.size();++i)
	    sum+=als[i].v;
	  for(unsigned int i=0;i<min((unsigned int)als.size(),(unsigned int)PrintN);++i)
	    {
	      alignment x=*setOfGoodCenters[als[i].s].first;
	      if( !(als[i].a==0 && als[i].b==0) )
		{
		  if( als[i].a<=0&&als[i].b<=0 )
		    x.doSwap(-als[i].a,-als[i].b);
		  else
		    x.doMove(als[i].a,als[i].b);
		}
	      if( of3&&i<PrintN )
		printAlignToFile(es, fs, Elist.getVocabList(), Flist.getVocabList(),*of3,x.getAlignment(), pair_no, 
				 als[i].v/sum*count);
	      sum2+=als[i].v;
	      if( writeNBestErrorsFile )
		{
		  if( pair_no<int(ReferenceAlignment.size()) )
		    {
		      int ALmissing=0,ALtoomuch=0,ALeventsMissing=0,ALeventsToomuch=0;
		      vector<double> scores;
		      ErrorsInAlignment(ReferenceAlignment[pair_no-1],x.getAlignment(),l,ALmissing,ALtoomuch,ALeventsMissing,ALeventsToomuch,pair_no);
		      ef.computeScores(x,scores);
		      *writeNBestErrorsFile << ALmissing+ALtoomuch << ' ';
		      for(unsigned int i=0;i<scores.size();++i)
			*writeNBestErrorsFile << ((scores[i]>0.0)?(-log(scores[i])):1.0e6) << ' ';
		      *writeNBestErrorsFile << '\n';
		    }
		}
	    }
	  if( writeNBestErrorsFile )
	    *writeNBestErrorsFile << '\n';
	}
      addAL((setOfGoodCenters[bestAlignment].first)->getAlignment(),sent.sentenceNo,l);
      if (Log)
      	logmsg << "processing this sentence pair ("<<l+1<<"x"<<m<<") : "<<
      	  (l+1)*m << " prob : " << align_total_count << " " << (setOfGoodCenters[bestAlignment].second) << alignment(*setOfGoodCenters[bestAlignment].first) << " \n";
      for(unsigned int i=0;i<setOfGoodCenters.size();i++)
	delete setOfGoodCenters[i].first;
      double period = difftime(time(NULL), sent_s);
      if (Verbose)
	cerr << "processing this sentence pair took : " << period
	     << " seconds\n";
      
    } /* of sentence pair E, F */
    sHandler1.rewind();
    perp.record(model);
    errorReportAL(cerr,model);
    viterbiPerp.record(model);
    if (dump_files||FEWDUMPS||(final&&(ONLYALDUMPS)) )
      of2.close();
    delete of3;
    delete writeNBestErrorsFile;
    double FSent=pair_no;
    cout << "#centers(pre/hillclimbed/real): " << NAlignment/FSent << " " << NHillClimbed/FSent << " " << NCenter/FSent << "  #al: " << NTotal/FSent << " #alsophisticatedcountcollection: " <<   NumberOfAlignmentsInSophisticatedCountCollection/FSent << " #hcsteps: " << HillClimbingSteps/FSent << '\n';
    cout << "#peggingImprovements: " << NBetterByPegging/FSent << '\n';
    }



#include "collCounts.cpp"
#define INSTANTIATE(A,B,C) template \
void model3::viterbi_loop_with_tricks<A,B,C>(Perplexity& perp, Perplexity& viterbiPerp, sentenceHandler& sHandler1,  \
					     bool dump_files, const char* alignfile,bool collect_counts, string, bool final,\
					     B*d4m,C*d5m);

INSTANTIATE(transpair_model3, void, void);
INSTANTIATE(transpair_modelhmm, const hmm, void);
INSTANTIATE(transpair_modelhmm, const hmm, d4model);
INSTANTIATE(transpair_modelhmm, const hmm, d5model);
INSTANTIATE(transpair_model3, void,d4model);
INSTANTIATE(transpair_model3, void,d5model);
INSTANTIATE(transpair_model4, d4model,d4model);
INSTANTIATE(transpair_model4, d4model,d5model);
INSTANTIATE(transpair_model5, d5model,d5model);
