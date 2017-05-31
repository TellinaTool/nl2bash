/*

Copyright (C) 1997,1998,1999,2000,2001  Franz Josef Och (RWTH Aachen - Lehrstuhl fuer Informatik VI)

This file is part of GIZA++ ( extension of GIZA ).

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
#ifndef HEADER_Pointer_DEFINED
#define HEADER_Pointer_DEFINED

#include <cassert>
#include <ostream>

template<class T>
class SmartPointer
{
 protected:
  T*p;
 public:
  SmartPointer(T*_p=0) 
    : p(_p) {}
  inline T&operator*() const 
    {return *p;}
  inline T*operator->() const 
    {return p;}
  inline operator bool() const 
    {return p!=0;}
  inline T*ptr() const
    { return p; }
};
template<class T> inline ostream &operator<<(ostream&out,const SmartPointer<T>&s)
{if( s.ptr() )return out << *s;else return out <<"nullpointer";}


template<class T>
class SmartPointerConst
{
 protected:
  const T*p;
 public:
  SmartPointerConst(const T*_p=0) 
    : p(_p) {}
  inline const T&operator*() const 
    {return *p;}
  inline const T*operator->() const 
    {return p;}
  inline operator bool() const
    {return p!=0;}
  inline const T*ptr() const
    { return p; }
};
template<class T> inline ostream &operator<<(ostream&out,const SmartPointerConst<T>&s)
{if( s.ptr() )return out << *s;else return out <<"nullpointer";}

template <class T>
class UP : public SmartPointer<T>
{
 public:
  UP(T*_p=0) 
    : SmartPointer<T>(_p) {}
};
template<class T> inline bool operator==(const UP<T>&s1,const UP<T>&s2)
{return s1.ptr()==s2.ptr();}
template<class T>  inline bool operator<(const UP<T>&s1,const UP<T>&s2)
{return s1.ptr() < s2.ptr();}
template<class T> inline int Hash(const UP<T> &wp)
{if(wp.ptr())return Hash(*wp);else return 0;}


template <class T>
class UPConst : public SmartPointerConst<T>
{
 public:
  UPConst(const T*_p=0) 
    : SmartPointerConst<T>(_p) {}
};
template<class T> inline bool operator==(const UPConst<T>&s1,const UPConst<T>&s2)
{return s1.ptr()==s2.ptr();}
template<class T> inline bool operator<(const UPConst<T>&s1,const UPConst<T>&s2)
{return s1.ptr()<s2.ptr();}
template<class T> inline int Hash(const UPConst<T> &wp)
{if(wp.ptr())return Hash(*wp);else return 0;}

	
template <class T>
class MP : public SmartPointer<T>
{
 public:
  MP(T*_p=0) 
    : SmartPointer<T>(_p) {}
};
template <class T> inline bool operator==(const MP<T>&s1,const MP<T>&s2)
{assert(s1);assert(s2);return *s1==*s2;}
template <class T> inline bool operator<(const MP<T>&s1,const MP<T>&s2)
{assert(s1);assert(s2);return *s1 < *s2;}
template <class T> inline int Hash(const MP<T> &wp)
{if(wp.ptr())return Hash(*wp);else return 0;}


template <class T>
class MPConst : public SmartPointerConst<T>
{
 public:
  MPConst(const T*_p=0) 
    : SmartPointerConst<T>(_p) {}
};
template <class T> inline bool operator==(const MPConst<T>&s1,const MPConst<T>&s2)
{assert(s1);assert(s2);return *s1== *s2;}
template <class T> inline bool operator<(const MPConst<T>&s1,const MPConst<T>&s2)
{assert(s1);assert(s2);return *s1 < *s2;}
template <class T> inline int Hash(const MPConst<T> &wp)
{if(wp.ptr())return Hash(*wp);else return 0;}


template <class T> 
class DELP : public SmartPointer<T>
{
 private:
  DELP(const DELP<T>&x);
 public:
  const DELP<T>&operator=(DELP<T>&x)
  {
    delete this->p;
    this->p=x.p;x.p=0;
    return *this;
  }

  ~DELP()
    { delete this->p;this->p=0;}
  DELP(T*_p=0) 
    : SmartPointer<T>(_p) {}
  void set(T*_p)
    {
      delete this->p;
      this->p=_p;
    }
  friend bool operator==(const DELP<T>&s1,const DELP<T>&s2)
    {
      return *(s1.p)== *(s2.p);
    }
  friend bool operator<(const DELP<T>&s1,const DELP<T>&s2)
    {
      return *(s1.p) < *(s2.p);
    }
  friend inline int Hash(const DELP<T> &wp)
    {
      if(wp.p)
	return Hash(*wp.p);
      else 
	return 0;
    }
};
#endif







