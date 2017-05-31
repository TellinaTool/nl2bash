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



#ifndef MY_ASSERT_DEFINED
#define MY_ASSERT_DEFINED
void myerror(int line,const char *file,const char *expression);
void imyerror(int line,const char *file,const char *expression);

#define iassert(expression) do {if (!(expression)) {imyerror(__LINE__,__FILE__,#expression);}} while (0)

#define massert(expr) do {} while(0)

#define vassert(expr) do {} while(0)

#include <assert.h>

#endif





