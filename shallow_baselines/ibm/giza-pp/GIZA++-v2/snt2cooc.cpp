#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <map>
#include <vector>
#include <set>
#include <cstdlib>

using namespace std;

void readVoc(istream&in,map<string,string>&voc)
{
  string line,s1,s2; 
  voc["1"]="UNK";
  if( !in )cerr <<"Vocabulary does not exist.\n";
  while(getline(in,line))
    {
      istringstream eingabe(line); 
      if( !(eingabe>>s1>>s2))
	cerr << "ERROR in vocabulary '" << line << "'\n";
      voc[s1]=s2;
    }
}

int maxElems=0;
int main(int argc,char **argv)
{
  if( argc!=4&&argc!=5 )
    {
      cerr << "Usage: " << argv[0] << " vcb1 vcb2 snt12 \n";
      cerr << "Converts GIZA++ snt-format into plain text.\n";
      exit(1);
    }
  bool counts=0;
  if( argc==5 )
    {
      if(string(argv[4])!="-counts")
	cerr << "ERROR: wrong option " << argv[5] << endl;
      counts=1;
	maxElems=10000000;
    }
  ifstream v1(argv[1]),v2(argv[2]),t(argv[3]);
  map<string,string>voc1,voc2;
  readVoc(v1,voc1);
  readVoc(v2,voc2);
  string line1,line2,line3;
  vector<map<int,int> > vsi(voc1.size()+1000);
  int nLine=0;
  int totalElems=0;
  while(getline(t,line1)&&getline(t,line2)&&getline(t,line3))
    {
      istringstream eingabe1(line1),eingabe2(line2),eingabe3(line3);
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
      totalElems-=vsi[0].size();
      for(unsigned int j=0;j<l2.size();++j)
	vsi[0][l2[j]]++;
      totalElems+=vsi[0].size();
      for(unsigned int i=0;i<l1.size();++i)
	{
	  if( l1[i]>=int(vsi.size()) )
	    {
	      cerr << "I have to resize: " << l1[i] << endl;
	      vsi.resize(l1[i]+1);
	    }
	  map<int,int>&theset=vsi[l1[i]];
	  totalElems-=theset.size();
	  for(unsigned int j=0;j<l2.size();++j)
	    theset[l2[j]]++;
	  totalElems+=theset.size();
	}
      if( totalElems>maxElems&&maxElems )
	{
	  cerr << "INFO: print out " << totalElems << " entries.\n";
	  for(unsigned int i=0;i<vsi.size();++i)
	    for(map<int,int>::const_iterator j=vsi[i].begin();j!=vsi[i].end();++j)
	      {
		if(counts==1 )
		  cout << j->second << " " << i << " " << j->first << '\n';
		else
		  cout << i << " " << j->first << '\n';
	      }
	  totalElems=0;
	  vsi.clear();
	  vsi.resize(voc1.size()+1000);
	}
    }
  cerr << "END.\n";
  for(unsigned int i=0;i<vsi.size();++i)
    for(map<int,int>::const_iterator j=vsi[i].begin();j!=vsi[i].end();++j)
      {
	if(counts==1 )
	  cout << j->second << " " << i << " " << j->first << '\n';
	else
	  cout << i << " " << j->first << '\n';
      }
}

