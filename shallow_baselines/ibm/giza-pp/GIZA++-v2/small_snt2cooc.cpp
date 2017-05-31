#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>
#include <algorithm>


using namespace std;

class myset {
  private:
    vector<int> data;
    void check_cap() {
      size_t dc = data.capacity();
      if (dc - data.size() < 3) {
        if (dc < 4) { dc = 2; }
        if (dc < 18) { dc*=2; } else { dc+=15; }
	data.reserve(dc);
      }
    }
  public:
    typedef vector<int>::iterator iterator;
    void insert(int x) {
      if (data.size() == 0) { data.push_back(x); return; }
      vector<int>::iterator p = lower_bound(data.begin(), data.end(), x);
      int i = p - data.begin();
      if (i >= data.size()) { check_cap(); data.push_back(x); return; }
      if (*p == x) return;
      check_cap();
      data.insert(data.begin() + i,x);
    }
    iterator begin() { return data.begin(); }
    iterator end() { return data.end(); }
};

//#include <set>
// typedef std::set<int> intset;
//#include <ext/hash_set>
// typedef __gnu_cxx::hash_set<int> intset;
typedef myset intset;


int main(int argc,char **argv)
{
  if( argc!=2 )
    {
      cerr << "Usage: " << argv[0] << " snt12 \n";
      cerr << "Converts GIZA++ snt-format into plain text.\n";
      exit(1);
    }
  ifstream t(argv[1]);
  string line1,line2,line3;
  vector<intset> vsi(400000);
  int nLine=0;
  int totalElems=0;
  while(getline(t,line1)&&getline(t,line2)&&getline(t,line3))
    {
      istringstream eingabe1(line1.c_str()),eingabe2(line2.c_str()),eingabe3(line3.c_str());
      double count;
      string word;
      eingabe1>>count;
      vector<int>l1,l2;
      while(eingabe2>>word)
	l1.push_back(atoi(word.c_str()));
      while(eingabe3>>word)
	l2.push_back(atoi(word.c_str()));
      if( ((++nLine)%1000)==0 )
	cerr << "line " << nLine << '\n'; 
      for(unsigned int j=0;j<l2.size();++j)
	vsi[0].insert(l2[j]);
      for(unsigned int i=0;i<l1.size();++i)
	{
	  if( l1[i]>=int(vsi.size()) )
	    {
	      cerr << "I have to resize: " << l1[i] << endl;
	      vsi.resize(l1[i]+1000);
	    }
	  intset&theset=vsi[l1[i]];
	  for(unsigned int j=0;j<l2.size();++j)
	    theset.insert(l2[j]);
	}
     }
  int vi = 0;
  for(vector<intset>::iterator i=vsi.begin();i != vsi.end(); ++i) {
    for(intset::iterator j=i->begin();j!=i->end();++j)
      cout << vi << " " << *j << endl;
    ++vi;
  }
}

