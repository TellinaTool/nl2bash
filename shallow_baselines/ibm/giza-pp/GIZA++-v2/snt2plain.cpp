#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <map>
#include <vector>
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

int main(int argc,char **argv)
{
  if( argc!=5&&argc!=6 )
    {
      cerr << "Usage: " << argv[0] << " vcb1 vcb2 snt12 output_prefix [ -counts ]\n";
      cerr << "Converts GIZA++ snt-format into plain text.\n";
      exit(1);
    }
  bool counts=0;
  if( argc==6 )
    {
      if(string(argv[5])!="-counts")
	cerr << "ERROR: wrong option " << argv[5] << endl;
      counts=1;
    }
  ifstream v1(argv[1]),v2(argv[2]),t(argv[3]);
  string prefix(argv[4]);
  string outfil1=prefix+"1.txt";
  string outfil2=prefix+"2.txt";
  ofstream out1(outfil1.c_str());
  ofstream out2(outfil2.c_str());
  map<string,string>voc1,voc2;
  readVoc(v1,voc1);
  readVoc(v2,voc2);
  int source=0,target=0;
  string line1,line2,line3;
  int printed=0;
  while(getline(t,line1)&&getline(t,line2)&&getline(t,line3))
    {
      istringstream eingabe1(line1),eingabe2(line2),eingabe3(line3);
      double count;
      string word;
      eingabe1>>count;
      vector<string>l1,l2;
      while(eingabe2>>word)
	l1.push_back(word);
      while(eingabe3>>word)
	l2.push_back(word);
      if( counts ) 
	cout << count << '\n';
      for(unsigned int p=0;p<l1.size();p++)
	{
	  if(voc1.count(l1[p])==0)
	    {
	      if( printed++==0)
		cerr << "ERROR: source vocabulary entry " << l1[p] << " unknown.\n";
	      out1 << l1[p]<<' ';
	    }
	  else
	    out1 << voc1[l1[p]] << ' ';
	  source++;
	}
      for(unsigned int p=0;p<l2.size();p++)
	{
	  if(voc2.count(l2[p])==0)
	    {
	      if( printed++ ==0)
		cerr << "ERROR: target vocabulary entry " << l2[p] << " unknown.\n";
	      out2 <<l2[p]<<' ';
	    }
	  out2 << voc2[l2[p]] << ' ';
	  target++;
	}
      out1<<'\n';
      out2<<'\n';
    }
}
