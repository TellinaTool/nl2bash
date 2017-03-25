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
#ifndef transpair_model3_h_fjo_defined
#define transpair_model3_h_fjo_defined
#include "Array2.h"
#include "defs.h"
#include "Vector.h"
#include "NTables.h"
#include "ATables.h"
#include "TTables.h"
#include "alignment.h"
#include <cmath>
#include "transpair_model2.h"

extern double factorial(int n);
inline bool doubleEqual(const double a, const double b)
{
  if( a==b )
    return 1.0;
  bool bl=fabs(1.0-a/b)<1e-10;
  if( bl )
    return 1;
  else
    {
      cerr << "DIFFERENT: " << a << " " << b << " " << a/b << " " << 1.0-a/b << endl;
      return 0;
    }
}


class transpair_model3 : public transpair_model2
{
 protected:
  Array2<PROB, Vector<PROB> > d, n;
  PROB p0, p1;
 public:
  typedef transpair_model3 simpler_transpair_model;
  transpair_model3(const Vector<WordIndex>&es, const Vector<WordIndex>&fs, tmodel<COUNT, PROB>&tTable, 
		   amodel<PROB>&aTable, amodel<PROB>&dTable, nmodel<PROB>&nTable, 
		   double _p1, double _p0, void*x=0);
  const PROB&get_d(WordIndex i, WordIndex j)const
    {return d(i, j);}
  const PROB&get_a(WordIndex i, WordIndex j)const
    {return a(i, j);}
  const PROB&get_fertility(WordIndex i, WordIndex f)const
    {massert(i>0);return (f>=MAX_FERTILITY)?n(i, MAX_FERTILITY):n(i, f);}
  int modelnr()const{return 3;}
  LogProb scoreOfAlignmentForChange(const alignment&)const
    {return -1.0; }  
  LogProb scoreOfMove(const alignment&a, WordIndex new_i, WordIndex j, double thisValue=-1.0,bool withDistortions=1)const;
  LogProb scoreOfSwap(const alignment&a, WordIndex j1, WordIndex j2, double thisValue=-1.0,bool withDistortions=1)const ;
  LogProb _scoreOfMove(const alignment&a, WordIndex new_i, WordIndex j,double thisValue=-1.0)const;
  LogProb _scoreOfSwap(const alignment&a, WordIndex j1, WordIndex j2,double thisValue=-1.0)const;
  friend ostream&operator<<(ostream&out, const transpair_model3&m);
  LogProb prob_of_target_and_alignment_given_source(const alignment&al,bool verb=0)const;
  bool isSubOptimal()const{return 1;}
  void computeScores(const alignment&al,vector<double>&d)const;
};
#endif
