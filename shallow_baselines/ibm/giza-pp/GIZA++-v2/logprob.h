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
#ifndef _LOGPROB_H
#define _LOGPROB_H

// Routines to perform integer exponential arithmetic.
// A number x is represented as n, where x = b**n
// It is assumed that b > 1, something like b = 1.001

#include <iostream>
#include <math.h>
#include <algorithm>

//#define  MAX(A,B) ((A) > (B) ? (A) : (B))
//#define  MIN(A,B) ((A) > (B) ? (B) : (A))


class LogProb {
public:
  // mj for cross entropy
  double base2() const {
    return (logr * logb2 / log(2));
  }
  
  // Constructors
  LogProb() : logr(zeron) {}
  LogProb(const LogProb &obj) : logr(obj.logr) {}
  LogProb(double x) : logr(x == 0.0 ? zeron : round(log(x)/logb2)) {}
  // destructor
  ~LogProb() {}                  // default destructor

  operator double() const    // converts logr to (double) b**logr
    {
      if (logr < nmin) return ntof[0];
      if (logr > nmax) return ntof[nmax-nmin];
      return ntof[logr-nmin];
    }

  LogProb &operator=(const LogProb &obj) { logr = obj.logr; return *this; }
  int operator!() const { return logr == zeron; }
  
  // iostream friend specifications
  friend std::ostream& operator<<(std::ostream& os, const LogProb &obj);
  friend std::istream& operator>>(std::istream& is, LogProb &obj);
  friend std::ostream& operator<<=(std::ostream& os, const LogProb &obj);
  friend std::istream& operator>>=(std::istream& is, LogProb &obj);

  // arithmetic operators 
  LogProb &operator+=(const LogProb &add)   // logr2 = logb ( b**logr2 + b**logr1 )
    // Add two numbers represented as logarithms. Use the following method:
    //   b**n + b**m = b**n(1 + b**(m-n)), assuming n >= m.
    {
      if (add.logr == zeron)
	return *this;
      if (logr == zeron)
	{
	  logr = add.logr;
	  return *this;
	}
      int a = add.logr - logr;
      if (a > 0)
	{
	  a = -a;
	  logr = add.logr;
	}
      if (a < tblbnd)
	return *this;
      logr += addtbl[a-tblbnd];
      return *this;
    }

  LogProb &operator-=(const LogProb &);   // logr2 = logb ( b**logr2 + b**logr1 )
  LogProb operator*(const LogProb &mul) const  // logr3 = logr2 + logr1
    {
      LogProb result;		// start out with result == 0
      if ((logr != zeron) && (mul.logr != zeron))
	result.logr = std::max(logr+mul.logr, zeron);
      return result;
    }
  LogProb operator*(double x) const  // logr3 = logr2 + logr1
    {
      return (*this)*(LogProb)x;
    }
  LogProb operator^(const int i) const  // logr2 = logr1 * i
    {
      LogProb result;		// start out with result == 0
      //      if ((logr != zeron) && (mul.logr != zeron))
      	result.logr = logr * i ;
	return result;
    }
  LogProb &operator*=(const LogProb &mul) // logr2 += logr1
    { 
      if ((logr == zeron) || (mul.logr == zeron))
	logr = zeron;
      else
	logr = std::max(logr+mul.logr, zeron);
      return *this;
    }
  LogProb operator/(const LogProb &div) const  // logr3 = logr2 -logr1
    {
      LogProb result;
      if (logr != zeron)
	result.logr = std::max(logr - div.logr, zeron);
      return result;
    }
  LogProb &operator/=(const LogProb &div) // logr2 -= logr1
    {
      if (logr != zeron)
	logr = std::max(logr - div.logr, zeron);
      return *this;
    }
  LogProb operator+(const LogProb &l) const // logr3 = logb ( b**logr2 + b**logr1 )
    { LogProb result(*this); result += l; return result; }
  LogProb operator-(const LogProb &l) const // logr3 = logb ( b**logr2 - b**logr1 )
    { LogProb result(*this); result -= l; return result; }
  LogProb power(const int n) const // logr2 = logr1 * int
    { LogProb result(*this); result.logr *= n; return result; }
  
  // Conditional operators
  int operator<(const LogProb &obj)  const { return logr <  obj.logr; }
  int operator<=(const LogProb &obj) const { return logr <= obj.logr; }
  int operator>(const LogProb &obj)  const { return logr >  obj.logr; }
  int operator>=(const LogProb &obj) const { return logr >= obj.logr; }
  int operator==(const LogProb &obj) const { return logr == obj.logr; }
  int operator!=(const LogProb &obj) const { return logr != obj.logr; }
  int operator<(double d)  const { return ((double)*this) < d;  }
  int operator<=(double d) const { return ((double)*this) <= d; }
  int operator>(double d)  const { return ((double)*this) >  d; }
  int operator>=(double d) const { return ((double)*this) >= d; }
  int operator==(double d) const { return ((double)*this) == d; }
  int operator!=(double d) const { return ((double)*this) != d; }
  

  LogProb &SetZero() { logr = zeron; return *this; } // representation of 0,
  LogProb &SetOne() { logr = onen; return *this; }   // 1, and
  LogProb &SetInf() { logr = infn; return *this; }   // inf in logarithm domain 

private:
  int logr;			// a representation of logarithm
  // static constants
  static const  int    initialized; // initialization flag
  static const  double b;
  static const  double logb2;
  static const  int    nmin, nmax;
  static const  int    tblbnd;
  static const  int    zeron, onen, infn;  // zero, one, and inf in log domain
  static const  int    max_2byte_integer, min_2byte_integer;
  
  // Arithmetic computation Tables
  static double *ntof;
  static int   *addtbl;
  static int   *subtbl;

  static int Initialize();

public:
  static void FreeTables();
  // constants for initializing LogProbs to 0 or 1
  static const LogProb zero;
  static const LogProb one;
  static const LogProb minus2;
  static const LogProb minus4;
  static const LogProb minus6;
  static const LogProb minus8;
  static const LogProb minus10;
  static const LogProb minus12;
  static const LogProb minus14;
  static const LogProb minus16;
};

// iostream friend operators
inline std::ostream &operator<<(std::ostream& os, const LogProb &obj)
{
  return os << (double) obj;         // output in linear domain, b**logr
}

inline std::istream &operator>>(std::istream& is, LogProb &obj)
{
  double d;
  is >> d;
  obj = d;
  return is;
}

inline std::ostream &operator<<=(std::ostream& os, const LogProb &obj) // write binary
{
  os.write((const char *)&obj.logr, sizeof(obj.logr));
  return os;
}

inline std::istream &operator>>=(std::istream& is, LogProb &obj)
{
  is.read((char *)&obj.logr, sizeof(obj.logr));
  return is;
}

#endif

