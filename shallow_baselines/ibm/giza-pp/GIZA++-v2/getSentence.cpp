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
/* --------------------------------------------------------------------------*
 *                                                                           *
 * Module : getSentece                                                       *
 *                                                                           *
 * Method Definitions File: getSentence.cc                                   *
 *                                                                           *
 * Objective: Defines clases and methods for handling I/O for the parallel   *
 *            corpus.                                                        *
 *****************************************************************************/


#include "getSentence.h"
#include <iostream>
#include <sstream>
#include "Parameter.h"
#include "errno.h"

int PrintedTooLong=0;

/* -------------- Method Defnitions for Class sentenceHandler ---------------*/

GLOBAL_PARAMETER(double,ManlexMAX_MULTIPLICITY,"manlexMAX_MULTIPLICITY","",PARLEV_EM,20.0);
GLOBAL_PARAMETER(double,Manlexfactor1,"manlexfactor1","",PARLEV_EM,0.0);
GLOBAL_PARAMETER(double,Manlexfactor2,"manlexfactor2","",PARLEV_EM,0.0);

sentenceHandler::sentenceHandler(const char*  filename, vcbList* elist, 
				 vcbList*  flist) : realCount(0)
  // This method is the constructor of the class, it also intitializes the 
  // sentence pair sequential number (count) to zero.

{
  readflag = false ;
  allInMemory = false ;
  inputFilename = filename ;
  inputFile = new ifstream(filename);
  pair_no = 0 ;
  if(!(*inputFile)){
    cerr << "\nERROR:(a) Cannot open " << filename;
    exit(1);
  }
  currentSentence = 0;
  totalPairs1 = 0 ;
  totalPairs2 =0;
  pair_no = 0 ;
  noSentInBuffer = 0 ;
  Buffer.clear();
  bool isNegative=0;
  if (elist && flist){
    cout << "Calculating vocabulary frequencies from corpus " << filename << '\n';
    sentPair s ;
    while (getNextSentence(s, elist, flist))
      {
	totalPairs1++;
	totalPairs2+=s.realCount; 
	// NOTE: this value might change during training 
	// for words from the manual dictionary, yet this is ignored!

	if( s.noOcc<0 )
	  isNegative=1;
      }
  }
  if( isNegative==1 )
    {
      cerr << "WARNING: corpus contains negative occurrency frequencies => these are interpreted as entries of a manual dictionary.\n";
      realCount=new Vector<double>(totalPairs1,1.0);
    }
  else
    realCount=0;
}

void sentenceHandler::rewind()
{
  currentSentence = 0;
  readflag = false ;
  if (!allInMemory || 
      !(Buffer.size() >= 1 && Buffer[currentSentence].sentenceNo == 1)){
    // check if the buffer doe not already has the first chunk of pairs 
    if (Buffer.size() > 0)
      cerr << ' ' <<  Buffer[currentSentence].sentenceNo << '\n';
    //    totalPairs = 0 ;
    pair_no = 0 ;
    noSentInBuffer = 0 ;
    Buffer.clear();
  }
  if (!allInMemory){
    delete inputFile;
    inputFile = new ifstream(inputFilename);
    if(!(*inputFile)){
      cerr << "\nERROR:(b) Cannot open " << inputFilename << " " << (int)errno;
    }
  }
}

  
bool sentenceHandler::getNextSentence(sentPair& sent, vcbList* elist, vcbList* flist)
{
  sentPair s ;
  if (readflag){
    cerr << "Attempting to read from the end of corpus, rewinding\n";
    rewind();
    return(false);
  } 
  if (currentSentence >= noSentInBuffer){
    if (allInMemory)
      return(false);
    /* no more sentences in buffer */
    noSentInBuffer = 0 ;
    currentSentence = 0 ;
    Buffer.clear();
    cout << "Reading more sentence pairs into memory ... \n";
    while((noSentInBuffer < TRAIN_BUFFER_SIZE) && readNextSentence(s)){
      if ((s.fSent.size()-1) > (MAX_FERTILITY-1) * (s.eSent.size()-1)){
	cerr << "WARNING: The following sentence pair has source/target sentence length ration more than\n"<<
	  "the maximum allowed limit for a source word fertility\n"<<
	  " source length = " << s.eSent.size()-1 << " target length = " << s.fSent.size()-1 <<
	  " ratio " << double(s.fSent.size()-1)/  (s.eSent.size()-1) << " ferility limit : " <<
	  MAX_FERTILITY-1 << '\n';
	cerr << "Shortening sentence \n";
	cerr << s;
	s.eSent.resize(min(s.eSent.size(),s.fSent.size()));
	s.fSent.resize(min(s.eSent.size(),s.fSent.size()));
      }
      Buffer.push_back(s) ;
      if (elist && flist){
	if ((*elist).size() > 0)
	  for (WordIndex i= 0 ; i < s.eSent.size() ; i++){
	    if (s.eSent[i] >= (*elist).uniqTokens()){
	      if( PrintedTooLong++<100)
		cerr << "ERROR: source word " << s.eSent[i] << " is not in the vocabulary list \n";
	      exit(-1);
	    }
	    (*elist).incFreq(s.eSent[i], s.realCount);
	  }
	if ((*flist).size() > 0)
	  for (WordIndex j= 1 ; j < s.fSent.size() ; j++){
	    if (s.fSent[j] >= (*flist).uniqTokens()){
	      cerr << "ERROR: target word " << s.fSent[j] << " is not in the vocabulary list \n";
	      exit(-1);
	    }
	    (*flist).incFreq(s.fSent[j], s.realCount);
	  }
      }
      noSentInBuffer++;
    }
    if (inputFile->eof()){
      allInMemory = (Buffer.size() >= 1 && 
		     Buffer[currentSentence].sentenceNo == 1) ;
      if (allInMemory)
	cout << "Corpus fits in memory, corpus has: " << Buffer.size() <<
	  " sentence pairs.\n";
    }
  }
  if(noSentInBuffer <= 0 ){
    //cerr << "# sent in buffer " << noSentInBuffer << '\n';
    readflag = true ;
    return(false);
  }
  sent = Buffer[currentSentence++] ;
  if( sent.noOcc<0 && realCount )
    {
      if( Manlexfactor1 && sent.noOcc==-1.0 )
	sent.realCount=Manlexfactor1;
      else if( Manlexfactor2 && sent.noOcc==-2.0 )
	sent.realCount=Manlexfactor2;
      else
	sent.realCount=(*realCount)[sent.getSentenceNo()-1];
    }
  return true ;
}
bool sentenceHandler::readNextSentence(sentPair& sent)
  /* This method reads in a new pair of sentences, each pair is read from the 
     corpus file as line triples. The first line the no of times this line 
     pair occured in the corpus, the second line is the source sentence and 
     the third is the target sentence. The sentences are represented by a space
     separated positive integer token ids. */
{

  string line;
  bool fail(false) ;
  
  sent.clear();
  if (getline(*inputFile, line)){
    istringstream buffer(line);
    buffer >> sent.noOcc;
    if( sent.noOcc<0 )
      {
	if( realCount )
	  {
	    if( Manlexfactor1 && sent.noOcc==-1.0 )
	      sent.realCount=Manlexfactor1;
	    else if( Manlexfactor2 && sent.noOcc==-2.0 )
	      sent.realCount=Manlexfactor2;
	    else
	      {
		sent.realCount=(*realCount)[pair_no];
	      }
	  }
	else
	  sent.realCount=1.0;
      }
    else
      sent.realCount=sent.noOcc;
  }
  else {
    fail = true ;;
  }
  if (getline(*inputFile, line)){
    istringstream buffer(line);
    WordIndex w;  // w is a local variabe for token id
    sent.eSent.push_back(0); // each source word is assumed to have 0 == 
    // a null word (id 0) at the begining of the sentence. 
    while(buffer>>w){ // read source sentece , word by word .
      if (sent.eSent.size() < MAX_SENTENCE_LENGTH)
	sent.eSent.push_back(w);
      else {
	if( PrintedTooLong++<100)
	  cerr << "{WARNING:(a)truncated sentence "<<pair_no<<"}";
	//cerr << "ERROR: getSentence.cc:getNextSentence(): sentence exceeds preset length limit of : " << MAX_SENTENCE_LENGTH << '\n';
	//cerr << "The following sentence will be truncated\n" << line;
	break ;
      }
    }
  }
  else {
    fail = true ;
  }
  if (getline(*inputFile, line)){
    istringstream buffer(line);
    WordIndex w;  // w is a local variabe for token id
    sent.fSent.push_back(0); //0 is inserted for program uniformity
    while(buffer>>w){ // read target sentece , word by word .
      if (sent.fSent.size() < MAX_SENTENCE_LENGTH)
	sent.fSent.push_back(w);
      else {
	if( PrintedTooLong++<100)
	  cerr << "{WARNING:(b)truncated sentence "<<pair_no<<"}";
	//cerr << "ERROR: getSentence.cc:getNextSentence(): sentence exceeds preset length limit of : " << MAX_SENTENCE_LENGTH << '\n';
	//cerr << "The following sentence will be truncated\n" << line;
	break ;
      }
    }
  }
  else {
    fail = true ;
  }
  if (fail){
    sent.eSent.clear();
    sent.fSent.clear();
    sent.sentenceNo = 0 ;
    sent.noOcc = 0 ;
    sent.realCount=0;
    return(false);
  }  
  if( sent.eSent.size()==1||sent.fSent.size()==1 )
    cerr << "ERROR: Forbidden zero sentence length " << sent.sentenceNo << endl;
  sent.sentenceNo = ++pair_no;
  if(pair_no % 100000 == 0) 
    cout << "[sent:" << sent.sentenceNo  << "]"<< '\n';
  return true;
}

double optimize_lambda(Vector<double>&vd)
{
  Vector<double> l;
  for(double lambda=1.0;lambda<ManlexMAX_MULTIPLICITY;lambda+=0.33)
    {
      double prod=0.0;
      for(unsigned int i=0;i<vd.size();++i)
	{
	  prod += vd[i]*exp(lambda*vd[i])/(exp(lambda*vd[i])-1.0);
	}
      l.push_back(fabs(prod-1.0));
    }
  double lam=double(min_element(l.begin(),l.end())-l.begin())*0.33+1.0;
  if( lam<1.0 )
    {
      cerr << "ERROR: lambda is smaller than one: " << lam << endl;
      for(unsigned int i=0;i<vd.size();++i)
	cerr << vd[i] << ' ';
      cerr << endl;
    }
  return lam;
}

void sentenceHandler::setProbOfSentence(const sentPair&s,double d)
{
  if( realCount==0 )
    return;
  else
    {
      if( s.noOcc<=0 )
	{
	  double ed=exp(d);
	  if( oldPairs.size()>0&&(oldPairs.back().get_eSent()!=s.get_eSent()||oldPairs.back().getSentenceNo()>=s.getSentenceNo()) )
	    {
	      double lambda=optimize_lambda(oldProbs);
	      for(unsigned int i=0;i<oldPairs.size();++i)
		{
		  if( oldProbs[i]<1e-5 )
		    (*realCount)[oldPairs[i].getSentenceNo()-1]=1.0;
		  else
		    (*realCount)[oldPairs[i].getSentenceNo()-1]=lambda*oldProbs[i]/(1-exp(-lambda*oldProbs[i]));		    
		}
	      oldPairs.clear();
	      oldProbs.clear();
	    }
	  oldPairs.push_back(s);
	  oldProbs.push_back(ed);
	}
    }
}

/* ------------- End of Method Definition of Class sentenceHandler ----------*/






