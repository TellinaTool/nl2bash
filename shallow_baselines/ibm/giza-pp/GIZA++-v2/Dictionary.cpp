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
/* Noah A. Smith
   Dictionary object for dictionary filter in Model 1 training

   Dictionary file must be in order (sorted) by Foreign vocab id, but English
   vocab ids may be in any order.

   9 August 1999
*/

#include "Dictionary.h"

#include <cstring>

Dictionary::Dictionary(const char *filename){
  if(!strcmp(filename, "")){
    dead = true;
    return;
  }
  dead = false;
  cout << "Reading dictionary from:  " << filename << '\n';
  ifstream dFile(filename);
  if(!dFile){
    cerr << "ERROR: Can't open dictionary: " << filename << '\n';
    exit(1);
  }

  currindexmin = 0;
  currindexmax = 0;
  currval = 0;
  int p, q;
  while((dFile >> p >> q)){
    pairs[0].push_back(p);
    pairs[1].push_back(q);
  }
  cout << "Dictionary read; " << pairs[0].size() << " pairs loaded." << '\n';
  dFile.close();
}


bool Dictionary::indict(int p, int q){
  if(dead) return false;
  if(p == 0 && q == 0) return false;
  if(currval == p){
    for(int i = currindexmin; i <= currindexmax; i++)
      if(pairs[1][i] == q) return true;
    return false;
  }
  else{
    int begin = 0, end = pairs[0].size() - 1, middle = 0;
    unsigned int t;
    bool ret = false;
    while(begin <= end){
      middle = begin + ((end - begin) >> 1);
      if(p < pairs[0][middle]) end = middle - 1;
      else if(p > pairs[0][middle]) begin = middle + 1;
      else{
	break;
      }
    }
    t = middle;
    while(pairs[0][t] == p )
      if(pairs[1][t--] == q) ret = true;
    currindexmin = t + 1;
    t = middle + 1;
    while(pairs[0][t] == p && t < pairs[0].size())
      if(pairs[1][t++] == q) ret = true;
    currindexmax = t - 1;
    currval = p;
    return ret;
  }
}
  

