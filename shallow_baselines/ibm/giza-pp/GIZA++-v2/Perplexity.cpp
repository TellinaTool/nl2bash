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
/* Perplexity.cc
 * =============
 * Mike Jahr, 7/21/99
 * Machine Translation group, WS99
 * Center for Language and Speech Processing
 * 
 * Last Modified by: Yaser Al-Onaizan, August 17, 1999
 *
 * Simple class used to calculate cross entropy and perplexity
 * of models.
 */

#include "Perplexity.h"

void Perplexity::record(string model){
  modelid.push_back(model);
  perp.push_back(perplexity());
  ce.push_back(cross_entropy());
}
