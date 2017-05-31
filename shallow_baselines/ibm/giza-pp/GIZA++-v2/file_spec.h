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
#ifndef FILE_SPEC_H
#define FILE_SPEC_H

#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* This function returns a string, locally called file_spec. This
   string is the concatenation of the date and time of execution
   and the user who is performing the execution */
/* Originally implemented in C by Yaser Al-Onaizan; 
   editions for C++ and formatting by Noah A. Smith, 9 July 1999 */

char *Get_File_Spec (){
  struct tm *local;
  time_t t;
  const char *user;
  char time_stmp[19];
  char *file_spec = 0;
  
  t = time(NULL);
  local = localtime(&t);
  
  sprintf(time_stmp, "%02d-%02d-%02d.%02d%02d%02d.", local->tm_year, 
	  (local->tm_mon + 1), local->tm_mday, local->tm_hour, 
	  local->tm_min, local->tm_sec);
  user = getenv("USER");
  if (!user) { user = "no_user"; }

  file_spec = (char *)malloc(sizeof(char) * 
			     (strlen(time_stmp) + strlen(user) + 1));
  file_spec[0] = '\0';
  strcat(file_spec, time_stmp) ;
  strcat(file_spec, user);
  return file_spec;
}

#endif
