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
#ifndef Globals_asdf_defined
#define Globals_asdf_defined
#include <string>
#include <fstream>
#include <map>
#include "defs.h"
#include "Vector.h"

extern float PROB_SMOOTH;
extern bool Verbose, Log, Peg, Transfer, Transfer2to3, useDict ;
extern string Prefix, LogFilename, OPath, 
  SourceVocabFilename, TargetVocabFilename, CorpusFilename, TestCorpusFilename, 
  t_Filename, a_Filename, p0_Filename, d_Filename, n_Filename, dictionary_Filename;
extern ofstream logmsg ;
extern double M5P0,P0 ;
extern bool NODUMPS, FEWDUMPS  ;
extern string Usage ;
extern unsigned int MAX_SENTENCE_LENGTH ;
extern int PegUntil;

extern short DeficientDistortionForEmptyWord;

extern int M4_Dependencies;
extern int M5_Dependencies;

extern short OutputInAachenFormat;

#define DEP_MODEL_l 1
#define DEP_MODEL_m 2
#define DEP_MODEL_F 4
#define DEP_MODEL_E 8

#define DEP_MODELb_l 16
#define DEP_MODELb_m 32
#define DEP_MODELb_F 64
#define DEP_MODELb_E 128

#define DEP_SUM 256

class vcbList;

extern vcbList *globeTrainVcbList, *globfTrainVcbList;

extern short PredictionInAlignments;
extern short SmoothHMM;
#define VERB Verbose

double ErrorsInAlignment(const map< pair<int,int>,char >&reference,const Vector<WordIndex>&test,int l,int&missing,int&toomuch,int&eventsMissing,int&eventsToomuch,int);
extern Vector<map< pair<int,int>,char > > ReferenceAlignment;
void printGIZAPars(ostream&out);

#endif
