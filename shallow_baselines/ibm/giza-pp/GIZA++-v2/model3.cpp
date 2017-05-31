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
#include "model3.h"
#include "collCounts.h"
#include "Globals.h"
#include "utility.h"
#include "D5Tables.h"
#include "transpair_model5.h"
#include "transpair_modelhmm.h"
#include "Parameter.h"

#define TRICKY_IBM3_TRAINING

GLOBAL_PARAMETER(int,M4_Dependencies,"depm4","d_{=1}: &1:l, &2:m, &4:F, &8:E, d_{>1}&16:l, &32:m, &64:F, &128:E",PARLEV_MODELS,76);
GLOBAL_PARAMETER(int,M5_Dependencies,"depm5","d_{=1}: &1:l, &2:m, &4:F, &8:E, d_{>1}&16:l, &32:m, &64:F, &128:E",PARLEV_MODELS,68);
GLOBAL_PARAMETER4(int,Model3_Dump_Freq,"MODEL 345 DUMP FREQUENCY","MODEL 3 DUMP FREQUENCY","t3","t345","dump frequency of Model 3/4/5",PARLEV_OUTPUT,0);


extern int Transfer_Dump_Freq;

model3::model3(model2& m2) : 
  model2(m2),dTable(true), dCountTable(true), 
  nTable(m2.getNoEnglishWords()+1, MAX_FERTILITY), 
  nCountTable(m2.getNoEnglishWords()+1, MAX_FERTILITY),h(0)
{}

void model3::load_tables(const char *nfile, const char *dfile, const char *p0file){
  cout << "Model3: loading n, d, p0 tables \n";

  nTable.readNTable(nfile);
  dTable.readTable(dfile);
  ifstream inf(p0file);
  if( !inf )
    cerr << "Can not open: " << p0file << '\n';
  else
    {
      cout << "Reading p0 value from " << p0file << "\n";
      inf >> p0;
      inf.close();
      p1 = 1 - p0;
    }
  cout << "p0 is: " << p0 << " p1:" << p1 << '\n';
}
  
model3::~model3()
{
  dTable.clear();
  dCountTable.clear();
  nTable.clear();
  nCountTable.clear();
}


void model3::em(int noIterations, sentenceHandler& sHandler1)
{

  LogProb all_prob, aprob, temp ;
  WordIndex i, j, l, m ;
  time_t it_st, st, it_fn, fn ;
  string tfile, dfile, nfile, p0file, afile, number;
  
  st = time(NULL) ;
  if (Log)
    logmsg << "\n" << "Starting Model3:  Training";
  cout << "\n" << "Starting Model3:  Training";
  //  sentenceHandler sHandler1(efFilename.c_str());
  sHandler1.rewind();
  for(int it=1; it <= noIterations; it++){
    it_st = time(NULL) ;
    if (Log)
      logmsg << "\n" << "Model3: Iteration " << it;
    cout << "\n" << "Model3: Iteration " << it;
    
    // set up the names of the files where the tables will be printed 
    int n = it;
    number = "";
    do{
      //mj changed next line
      number.insert((size_t) 0, 1, (char)(n % 10 + '0'));
    } while((n /= 10) > 0);
    tfile = Prefix + ".t3." + number ;
    afile = Prefix + ".a3." + number ;
    nfile = Prefix + ".n3." + number ;
    dfile = Prefix + ".d3." + number ;
    p0file = Prefix + ".p0_3." + number ;
    //    tCountTable.clear();
    dCountTable.clear();
    nCountTable.clear();
    p0_count = p1_count = 0 ;
    all_prob = 0 ;
    sentPair sent ;
    while(sHandler1.getNextSentence(sent)){
      Vector<WordIndex>& es = sent.eSent;
      Vector<WordIndex>& fs = sent.fSent;
      const float count  = sent.getCount();
      if ((sent.sentenceNo % 1000) == 0)
      cout <<sent.sentenceNo << '\n'; 
      Vector<WordIndex> A(fs.size(),/*-1*/0);
      Vector<WordIndex> Fert(es.size(),0);
      LogProb lcount=(LogProb)count;
      l = es.size()-1;
      m = fs.size()-1;
      WordIndex x, y ;
      all_prob = prob_of_target_given_source(tTable, fs, es);
      if (all_prob == 0)
	cout << "\n" <<"all_prob = 0"; 
	
      for ( x = 0 ; x < pow(l+1.0, double(m)) ; x++){ // For all possible alignmets A
	y = x ;
	for (j = 1 ; j <= m ; j++){
	  A[j] = y % (l+1) ;
	  y /= (l+1) ;
	}
	for(i = 0 ; i <= l ; i++)
	  Fert[i] = 0 ;
	for (j = 1 ; j <= m ; j++)
	  Fert[A[j]]++;
	if (2 * Fert[0] <= m){ /* consider alignments that has Fert[0] less than
				 half the number of words in French sentence */
	  aprob = prob_of_target_and_alignment_given_source(A, Fert, tTable, fs, es);
	  temp = aprob/all_prob ;
	  LogProb templcount = temp*lcount;

	  for (j = 1 ; j <= m ; j++){
	    tTable.incCount(es[A[j]], fs[j], templcount);
	    if (0 != A[j])
	      dCountTable.getRef(j, A[j], l, m)+=templcount;
	  }
	  for(i = 0 ; i <= l ; i++)
	    {
	      nCountTable.getRef(es[i], Fert[i])+=templcount;
	      //cout << "AFTER INC2: " << templcount << " " << nCountTable.getRef(es[i], Fert[i]) << '\n';
	    }
	  p1_count +=  double(temp) * (Fert[0] * count) ;
	  p0_count +=  double(temp) * ((m - 2 * Fert[0]) * count) ;
	}
      } /* of looping over all alignments */
    } /* of sentence pair E, F */
    sHandler1.rewind();
    
    // normalize tables
    if( OutputInAachenFormat==1 )
      tTable.printCountTable(tfile.c_str(),Elist.getVocabList(),Flist.getVocabList(),1);
    tTable.normalizeTable(Elist, Flist);
    aCountTable.normalize(aTable);
    dCountTable.normalize(dTable);
    nCountTable.normalize(nTable,&Elist.getVocabList());

    // normalize p1 & p0 
    
    if (p1_count + p0_count != 0){
      p1 = p1_count / ( p1_count + p0_count ) ;
      p0 = 1 - p1 ;
    }
    else {
      p1 = p0 = 0 ;
    }
    // print tables 
    if( OutputInAachenFormat==0 )
      tTable.printProbTable(tfile.c_str(),Elist.getVocabList(),Flist.getVocabList(),OutputInAachenFormat);
    dTable.printTable(dfile.c_str());
    nTable.printNTable(Elist.uniqTokens(), nfile.c_str(), Elist.getVocabList(),OutputInAachenFormat);
    ofstream of(p0file.c_str());
    of << p0;
    of.close();
    it_fn = time(NULL) ;
    cout << "\n" << "Model3 Iteration "<<it<<" took: " << difftime(it_fn, it_st) << " seconds\n";
    
  } /* of iterations */
  fn = time(NULL) ;
  cout << "\n" << "Entire Model3 Training took: " << difftime(fn, st) << " seconds\n";
}



      
	  
	
	
//-----------------------------------------------------------------------

/*
void simpleModel3Test()
{
  PositionIndex l=6;
  PositionIndex m=8;
  alignment al(l,m);
  al.set(1,1);
  al.set(2,2);
  al.set(3,3);
  al.set(4,2);
  al.set(5,0);
  al.set(6,6);
  al.set(7,3);
  al.set(8,4);
  cout << al;
  PositionIndex prev_cept=0;
  PositionIndex vac_all=m;
  Vector<char> vac(m+1,0);
  for(PositionIndex i=1;i<=l;i++)
    {
      PositionIndex cur_j=al.als_i[i]; 
      cout << "LOOP: " << i << " " << cur_j << '\n';
      PositionIndex prev_j=0;
      PositionIndex k=0;
      if(cur_j) { // process first word of cept
	k++;
	vac_all--;
	assert(vac[cur_j]==0);
	vac[cur_j]=1;
	for(unsigned int q=0;q<vac.size();q++)cout << (vac[q]?'1':'0') << ' ';
	cout << '\n';	       
	cout << i << " " << cur_j << ": d1(" << vacancies(vac,cur_j) << "|" << vacancies(vac,al.get_center(prev_cept)) << "," << vac_all << "+" << -al.fert(i)<< "+" << +k << ")\n" << '\n';
	prev_j=cur_j;
	cur_j=al.als_j[cur_j].next;
      } 
      while(cur_j) { // process following words of cept
	k++;
	vac_all--;
	vac[cur_j]=1;
	int vprev=vacancies(vac,prev_j);
	cout << "PREV: " << prev_j << '\n';
	for(unsigned int q=0;q<vac.size();q++)cout << (vac[q]?'1':'0') << ' ';
	cout << '\n';	       
	cout << i << " " << cur_j << ": d>1(" << vacancies(vac,cur_j) << "-" << vprev << "|" << vac_all<< "+" << -al.fert(i)<< "+" << +k << ")\n" << '\n';
	prev_j=cur_j;
	cur_j=al.als_j[cur_j].next;
      }
      assert(k==al.fert(i));
      if( k )
	prev_cept=i;
    }
  assert(vac_all==al.fert(0));
}
*/

extern short DoViterbiTraining;

int model3::viterbi(int noIterationsModel3, int noIterationsModel4,int noIterationsModel5,int noIterationsModel6)
{
  double minErrors=1.0;int minIter=0;
  d4model d4m(MAX_SENTENCE_LENGTH);
  d4m.makeWordClasses(Elist,Flist,SourceVocabFilename+".classes",TargetVocabFilename+".classes");
  d5model d5m(d4m);
  d5m.makeWordClasses(Elist,Flist,SourceVocabFilename+".classes",TargetVocabFilename+".classes");
  time_t it_st, st, it_fn, fn;
  bool dump_files = false ;
  string tfile, tfile_actual, dfile, afile, nfile, nfile_actual, p0file, alignfile, number, test_alignfile, d4file,d5file,zeroFertFile;
  st = time(NULL);
  sHandler1.rewind();
  if (testPerp && testHandler)
    (*testHandler).rewind();
  string trainingString;
  trainingString+=(h?'H':'3');
  for(int i=0;i<noIterationsModel3;++i) trainingString+='3';
  for(int i=0;i<noIterationsModel4;++i) trainingString+='4';
  for(int i=0;i<noIterationsModel5;++i) trainingString+='5';
  for(int i=0;i<noIterationsModel6;++i) trainingString+='6';
  
  cout << "\n==========================================================\n";
  cout << "Starting "<<trainingString<<":  Viterbi Training";
  if (Log){
    logmsg << "\n==========================================================\n";
    logmsg << "Starting "<<trainingString<<":  Viterbi Training";
  }
  cout << "\n "<<trainingString<<" Training Started at: "<< ctime(&st) << '\n';
  for(unsigned int it=1; it < trainingString.length(); it++){
  bool final=0;
    if( it==trainingString.length()-1 )
      final=1;
    string modelName;
    char fromModel=trainingString[it-1],toModel=trainingString[it];
    if(fromModel==toModel)
      modelName=string("Model")+fromModel;
    else
      modelName=string("T")+fromModel+"To"+toModel;
    it_st = time(NULL);
    cout <<"\n---------------------\n"<<modelName<<": Iteration " << it<<'\n';
    if (Log) 
      logmsg <<"\n---------------------\n"<<modelName<<": Iteration " << it<<'\n';
    dump_files = (final || ((Model3_Dump_Freq != 0) && ((it % Model3_Dump_Freq) == 0))) && !NODUMPS ;
    string d4file2;
    {
      // set up the names of the files where the tables will be printed 
      int n = it;
      number = "";
      do{
	//mj changed next line
	number.insert((size_t) 0, 1, (char)(n % 10 + '0'));
      } while((n /= 10) > 0);
      if( final )
	number="final";
      tfile = Prefix + ".t3." + number ;
      tfile_actual = Prefix + ".actual.t3." + number ;
      afile = Prefix + ".a3." + number ;
      nfile = Prefix + ".n3." + number ;
      nfile_actual = Prefix + ".actual.n3." + number ;
      dfile = Prefix + ".d3." + number ;
      d4file = Prefix + ".d4." + number ;
      d4file2 = Prefix + ".D4." + number ;
      d5file = Prefix + ".d5." + number ;
      alignfile = Prefix + ".A3." + number ;
      test_alignfile = Prefix + ".tst.A3." + number ;
      p0file = Prefix + ".p0_3." + number ;
    }
    // clear count tables 
    //    tCountTable.clear();
    dCountTable.clear();
    aCountTable.clear();
    initAL();
    nCountTable.clear();
    d4m.clear();
    p0_count = p1_count = 0 ;

#ifdef TRICKY_IBM3_TRAINING
    
#define TRAIN_ARGS perp,      trainViterbiPerp, sHandler1,    dump_files, alignfile.c_str(),     true,  modelName,final
#define TEST_ARGS  *testPerp, *testViterbiPerp, *testHandler, dump_files, test_alignfile.c_str(),false, modelName,final


    switch( toModel )
      {
      case '3':
	switch(fromModel )
	  {
	  case 'H':
	    viterbi_loop_with_tricks  <transpair_modelhmm,const hmm>(TRAIN_ARGS,h,(void*)0);
	    if (testPerp && testHandler)
	      viterbi_loop_with_tricks<transpair_modelhmm,const hmm>(TEST_ARGS, h,(void*)0);
	    break;
	  case '3':
	    viterbi_loop_with_tricks<transpair_model3>( TRAIN_ARGS, (void*)0,(void*)0);
	    if (testPerp && testHandler)
	      viterbi_loop_with_tricks<transpair_model3>( TEST_ARGS, (void*)0,(void*)0);
	    break;
	  default: abort();
	  }
	break;
      case '4':
	{
	  switch(fromModel)
	    {
	    case 'H':
	      viterbi_loop_with_tricks  <transpair_modelhmm,const hmm,d4model>(TRAIN_ARGS,h,&d4m);
	      if (testPerp && testHandler)
		viterbi_loop_with_tricks<transpair_modelhmm,const hmm,d4model>(TEST_ARGS, h,&d4m);
	      break;
	    case '3':
	      viterbi_loop_with_tricks<transpair_model3, void,d4model>(TRAIN_ARGS, (void*)0,&d4m);
	      if (testPerp && testHandler)
		viterbi_loop_with_tricks<transpair_model3, void,d4model>( TEST_ARGS , (void*)0,&d4m);	
	      break;
	    case '4':
	      viterbi_loop_with_tricks<transpair_model4, d4model,d4model>(TRAIN_ARGS , &d4m,&d4m);
	      if (testPerp && testHandler)
		viterbi_loop_with_tricks<transpair_model4, d4model,d4model>( TEST_ARGS, &d4m,&d4m);
	      break;
	    default: abort();
	    }
	  d4m.normalizeTable();
	  if( dump_files )
	    d4m.printProbTable(d4file.c_str(),d4file2.c_str());
	}
	break;
      case '5':
	{
	  switch(fromModel)
	    {
	    case 'H':
	      viterbi_loop_with_tricks  <transpair_modelhmm,const hmm,d5model>(TRAIN_ARGS,h,&d5m);
	      if (testPerp && testHandler)
		viterbi_loop_with_tricks<transpair_modelhmm,const hmm,d5model>(TEST_ARGS, h,&d5m);
	      break;
	    case '3':
	      viterbi_loop_with_tricks<transpair_model3, void,d5model>(TRAIN_ARGS, (void*)0,&d5m);
	      if (testPerp && testHandler)
		viterbi_loop_with_tricks<transpair_model3, void,d5model>( TEST_ARGS , (void*)0,&d5m);	
	      break;
	    case '4':
	      viterbi_loop_with_tricks<transpair_model4, d4model,d5model>(TRAIN_ARGS, &d4m,&d5m);
	      if (testPerp && testHandler)
		viterbi_loop_with_tricks<transpair_model4, d4model,d5model>( TEST_ARGS, &d4m,&d5m);	
	      break;
	    case '5':
	      viterbi_loop_with_tricks<transpair_model5, d5model, d5model>(TRAIN_ARGS, &d5m,&d5m);
	      if (testPerp && testHandler)
		viterbi_loop_with_tricks<transpair_model5, d5model, d5model>( TEST_ARGS, &d5m,&d5m);	
	      break;
	    default: abort();
	    }
	  d5m.d4m.normalizeTable();
	  if( dump_files )
	    d5m.d4m.printProbTable(d4file.c_str(),d4file2.c_str());
	  d5m.normalizeTable();
	  if( dump_files )
	    {
	      ofstream d5output(d5file.c_str());
	      d5output << d5m;
	    }
	}
      break;
      default: abort();
      }
    
#else
    viterbi_loop(perp, trainViterbiPerp, sHandler1, dump_files, 
		 alignfile.c_str(), true, model);
    if (testPerp && testHandler)
      viterbi_loop(*testPerp, *testViterbiPerp, *testHandler, 
		   dump_files, test_alignfile.c_str(), false, model);
 
#endif		 
    if( errorsAL()<minErrors )
      {
	minErrors=errorsAL();
        minIter=it;
      }

    // now normalize count tables 
    if( dump_files&&OutputInAachenFormat==1 )
      tTable.printCountTable(tfile.c_str(),Elist.getVocabList(),Flist.getVocabList(),1);
    tTable.normalizeTable(Elist, Flist);
    aCountTable.normalize(aTable);
    dCountTable.normalize(dTable);
    nCountTable.normalize(nTable,&Elist.getVocabList());

    //    cout << "tTable contains " << 
    //      tTable.getHash().bucket_count() << " buckets and "<<
    //tTable.getHash().size() << " entries.\n";
    
    // normalize p1 & p0 
    
   cout << "p0_count is " << p0_count << " and p1 is " << p1_count << "; "; 
      if(P0!=-1.0)
      {
	p0 = P0;
	p1 = 1-P0;
      }
    else {
      if (p1_count + p0_count != 0){
	p1 = p1_count / ( p1_count + p0_count ) ;
	p0 = 1 - p1 ;
      }
      else {
	p1 = p0 = 0 ;
	cerr << "ERROR: p0_count+p1_count is zero!!!\n";
      }
    }
    cout << "p0 is " << p0 << " p1: " << p1 << '\n';
    
    cout << modelName<<": TRAIN CROSS-ENTROPY " << perp.cross_entropy()
	 << " PERPLEXITY " << perp.perplexity() << '\n';
    if (testPerp && testHandler)
      cout << modelName << ":("<<it<<" TEST CROSS-ENTROPY " << (*testPerp).cross_entropy()
	   << " PERPLEXITY " << (*testPerp).perplexity() << " sum: " << (*testPerp).getSum()<<
	" wc: " << (*testPerp).word_count() << '\n';
    cout << modelName << ": ("<<it<<") TRAIN VITERBI CROSS-ENTROPY " << trainViterbiPerp.cross_entropy()
	 << " PERPLEXITY " << trainViterbiPerp.perplexity() << '\n';
    if (testPerp && testHandler)
      cout << modelName << ":  ("<<it<<")TEST VITERBI CROSS-ENTROPY " << (*testViterbiPerp).cross_entropy()
	   << " PERPLEXITY " << (*testViterbiPerp).perplexity() << " Sum: " << (*testViterbiPerp).getSum() <<
	" wc: " << (*testViterbiPerp).word_count() << '\n';
    if (dump_files)
      {
	if( OutputInAachenFormat==0 )
	  tTable.printProbTable(tfile.c_str(),Elist.getVocabList(),Flist.getVocabList(),OutputInAachenFormat);
	aTable.printTable(afile.c_str());
	dTable.printTable(dfile.c_str());
	nTable.printNTable(Elist.uniqTokens(), nfile.c_str(), Elist.getVocabList(), OutputInAachenFormat);
	ofstream of(p0file.c_str());
	of << p0;
	of.close();
      }
    
    it_fn = time(NULL) ;
    cout << "\n" << modelName << " Viterbi Iteration : "<<it<<  " took: " <<
      difftime(it_fn, it_st) << " seconds\n";
  } /* of iterations */
  fn = time(NULL);
  cout << trainingString <<" Training Finished at: " << ctime(&fn) << "\n";
  cout << "\n" << "Entire Viterbi "<<trainingString<<" Training took: " << difftime(fn, st) << " seconds\n";
  cout << "==========================================================\n";
  if( noIterationsModel4||noIterationsModel5 )
    minIter-=noIterationsModel3;
  if( noIterationsModel5 )
    minIter-=noIterationsModel4;
  return minIter;
}




