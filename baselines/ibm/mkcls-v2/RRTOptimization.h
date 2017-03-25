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







#ifndef RRTOPTIMIZATION
#define RRTOPTIMIZATION
#include "IterOptimization.h"

class RRTOptimization : public IterOptimization {
  

   private:
     double deviation;       
     double deltaDeviation;  
     double record;          

   protected:
      virtual void zInitialize();
     

      virtual short accept(double delta); 
     
     
      virtual void  abkuehlen();
     

      virtual short end();
     

      virtual void makeGraphOutput();
     

   public:
      RRTOptimization(Problem &p,double temperatur,
     double deltaTemperatur,int maxIter=-1);
     

      RRTOptimization(Problem &p,int maxIter=-1);
     

      RRTOptimization(RRTOptimization &o);
     

      static double optimizeValue(Problem &p,int proParameter,
                      int numParameter,int typ,int schritte= -1,int verbose=1);
     

     static double defaultAnnRate;  
                                  
     static double defaultMultiple; 
                                  
};

#endif
