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
MoveSwapMatrix: Efficient representation for moving and swapping
around in IBM3 training.
Franz Josef Och (30/07/99)
--*/
#ifndef moveswap2_costs_h_defined
#define moveswap2_costs_h_defined
#include "alignment.h"
#include "transpair_model3.h"
#include "myassert.h"

extern short DoViterbiTraining;

template<class TRANSPAIR>
class MoveSwapMatrix : public alignment
{
 private:
  const TRANSPAIR&ef;
  const WordIndex l, m;
  Array2<LogProb, Vector<LogProb> > _cmove, _cswap;
  Array2<char,Vector<char> > delmove,delswap;
  Vector<int> changed;
  int changedCounter;
  const int modelnr;
  bool lazyEvaluation;
  bool centerDeleted;
 public:
  bool check()const
    {
	  return 1;
    }
  const TRANSPAIR&get_ef()const
    {return ef;}
  bool isCenterDeleted()const
    {return centerDeleted;}
  bool isLazy()const
    {return lazyEvaluation;}
  MoveSwapMatrix(const TRANSPAIR&_ef, const alignment&_a);
  void updateJ(WordIndex j, bool,double thisValue);
  void updateI(WordIndex i,double thisValue);
  void doMove(WordIndex _i, WordIndex _j);
  void doSwap(WordIndex _j1, WordIndex _j2);
  void delCenter()
    {
      centerDeleted=1;
    }
  void delMove(WordIndex x, WordIndex y)
    {
      delmove(x,y)=1;
    }
  void delSwap(WordIndex x, WordIndex y)
    {
      massert(y>x);
      delswap(x,y)=1;
      delswap(y,x)=1;
    }
  bool isDelMove(WordIndex x, WordIndex y)const
    {
      return DoViterbiTraining||delmove(x,y);
    }
  bool isDelSwap(WordIndex x, WordIndex y)const
    {
      massert(y>x);
      return DoViterbiTraining||delswap(x,y);
    }
  LogProb cmove(WordIndex x, WordIndex y)const
    {
      massert( get_al(y)!=x );
      massert( delmove(x,y)==0 );
      if( lazyEvaluation )
	return ef.scoreOfMove(*this,x,y);
      else
	{
	  return _cmove(x, y);
	}
    }
  LogProb cswap(WordIndex x, WordIndex y)const
    {
      massert(x<y);
      massert(delswap(x,y)==0);
      massert(get_al(x)!=get_al(y));
      if( lazyEvaluation )
	return ef.scoreOfSwap(*this,x,y);
      else
	{
	  massert(y>x);
	  return _cswap(x, y);
	}
    }
  void printWrongs()const;
  bool isRight()const;
  friend ostream&operator<<(ostream&out, const MoveSwapMatrix<TRANSPAIR>&m)
    {return out << (alignment)m << "\nEF:\n"<< m.ef << "\nCMOVE\n"<<m._cmove << "\nCSWAP\n" << m._cswap << endl;};
};
#endif
