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
#include "vocab.h" 

void vcbList::readVocabList()
     // reads a vocabulary file from fname. It expects the following format:
     // 
     // token_id token_string frequency
{

  int freq=0;
  WordIndex word_id ;
  WordEntry entry("NULL",0) ;

  string line, word ;
  cerr << "Reading vocabulary file from:" << fname << "\n";    
  //  total = 0 ;
  ifstream vFile(fname);
  if(!vFile){
    cerr <<  "\nCannot open vocabulary file " << fname << "file";
    exit(1);
  }
  
  list.push_back(entry);
  s2i[entry.word]=list.size()-1;

  while(getline(vFile, line)){
    istringstream buffer(line);
    if(!(buffer >> word_id >> word >> freq))
      cerr << "ERROR: reading vocabulary; " << word_id << ' ' << word << ' ' << freq << endl;
    if (word_id == 0){
      cerr << "ERROR: TOKEN ID 0 is reserved for special token NULL, in line: \n"<< line<<"\n" ;
      exit(-1);
    }
    else if (word_id >= MAX_VOCAB_SIZE){
      cerr << "ERROR: TOKEN ID is greater than maximum vocabulary size "
	   << MAX_VOCAB_SIZE << " in line :\n"<< line <<"\n" ;
      exit(-1);
    }	
    else if (freq < 0){
      cerr << "ERROR: frequency must be a positive integer, in line :\n"
	   << line <<"\n";
      exit(-1);
    }
    else if(word_id >= list.size()){
      list.resize(word_id+1);
      list[word_id].word = word ;
      s2i[word]=word_id;
      list[word_id].freq = 0 ;
      noUniqueTokens = word_id + 1 ;
      //      noUniqueTokens++ ;
      //      total += freq ;
    }      
    else if(list[word_id].word != "\0"){
      cerr << "ERROR: TOKEN ID must be unique for each token, in line :\n"
	   << line <<"\n";
      cerr << "TOKEN ID " << word_id << " has already been assigned to: " <<
	list[word_id].word << "\n";
      exit(-1);
    }
    else { // line  has valid information
      list[word_id].word = word ;
      s2i[word]=word_id;
      list[word_id].freq = 0 ;
      //      noUniqueTokens++ ;
      noUniqueTokens  = word_id + 1 ;
      //      total += freq ;
    }
  } // end of while
}

