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
/* Perplexity.h
 * ============
 * Mike Jahr, 7/15/99
 * Machine Translation group, WS99
 * Center for Language and Speech Processing
 * 
 * Last Modified by: Yaser Al-Onaizan, August 17, 1999
 *
 * Simple class used to calculate cross entropy and perplexity
 * of models.
 */

#ifndef _PERPLEXITY_H
#define _PERPLEXITY_H

#include <cmath>
#include <fstream>
#include "Vector.h"
#include "defs.h"
#include "Array2.h"
#include "Globals.h"

#define CROSS_ENTROPY_BASE 2

class Perplexity {
 private:
    double sum;
    double wc;
    Array2<double, Vector<double> > *E_M_L;
    Vector<string> modelid;
    Vector<double > perp;
    Vector<double > ce;
    Vector<string> name ;
 public:
    ~Perplexity() { delete E_M_L;}
    Perplexity() {
      E_M_L  = new Array2<double, Vector<double> >(MAX_SENTENCE_LENGTH,MAX_SENTENCE_LENGTH);
      unsigned int l, m ;
      Vector<double> fact(MAX_SENTENCE_LENGTH, 1.0);
      for (m = 2 ; m < MAX_SENTENCE_LENGTH ; m++)
	fact[m] = fact[m-1] * m ;
      for (m = 1 ; m < MAX_SENTENCE_LENGTH ; m++)
	for (l = 1 ; l < MAX_SENTENCE_LENGTH ; l++) {
	  (*E_M_L)(l, m) = log (pow((LAMBDA * l), double(m)) * exp(-LAMBDA * double(l)) / 
				(fact[m])) ;
	}
      sum = 0 ;
      wc = 0;
      perp.clear();
      ce.clear();
      name.clear();
    }
    inline void clear() {
      sum = 0 ;
      wc = 0 ;
    }
    size_t size() const {return(min(perp.size(), ce.size()));}
    inline void addFactor(const double p, const double count, const int l, 
			  const int m,bool withPoisson) {
      wc += count * m ; // number of french words 
      sum += count * ( (withPoisson?((*E_M_L)(l, m)):0.0) + p) ;
    }
    inline double perplexity() const {
	return exp( -1*sum / wc);
    }

    inline double cross_entropy() const {
      return (-1.0*sum / (log(double(CROSS_ENTROPY_BASE)) * wc)); 
    }

    inline double word_count() const {
	return wc;
    }
    
    inline double getSum() const {
      return sum ;
    }

    void record(string model);
    
    friend void generatePerplexityReport(const Perplexity&, const Perplexity&, 
					 const Perplexity&, const Perplexity&, 
					 ostream&, int, int, bool); 
};


#endif
