/*

Copyright (C) 1997,1998,1999,2000,2001  Franz Josef Och

mkcls - a program for making word classes .

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






#ifndef GDAOPTIMIZATION
#define GDAOPTIMIZATION
#include "IterOptimization.h"

class GDAOptimization : public IterOptimization
{
  
   private:
     double temperatur;  
     double alpha;       
     short gdaEndFlag; 
                       

   protected:
      virtual void zInitialize();
     

      virtual short accept(double delta); 
     
     
      virtual void  abkuehlen();
     

      virtual short end();
     

      virtual void makeGraphOutput();
     

   public:
      GDAOptimization(Problem &p,double temperatur,double alpha,
     int maxIter=-1);
     

      GDAOptimization(Problem &p,int maxIter=-1);
     

      GDAOptimization(GDAOptimization &o);
     

      static double optimizeValue(Problem &p,int proParameter,
     int numParameter,int typ,int schritte= -1,int verbose=1);
     

     
     static double defaultTemperatur; 
     static double defaultAlpha;      

};
#endif


