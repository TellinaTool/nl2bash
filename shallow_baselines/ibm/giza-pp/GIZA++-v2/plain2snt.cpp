#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <map>
#include <vector>
#include <cstdlib>

using namespace std;

int main(int argc,char**argv)
{
  vector<double>weights;
  vector<string>filenames;
  for(int i=1;i<argc;++i)
    if(string(argv[i])=="-weight")
      weights.push_back(atof(argv[++i]));
    else
      filenames.push_back(argv[i]);
  
  if((filenames.size()%2)==1||filenames.size()==0 )
    {
      cerr << argv[0] << " txt1 txt2 [txt3 txt4 -weight w]\n";
      cerr << " Converts plain text into GIZA++ snt-format.\n";
      exit(1);
    }
  string line1,line2,word;
  map<string,int> v1,v2;
  map<string,int> id1,id2;
  vector<string> iid1(2),iid2(2);
  
  string w1(filenames[0]);
  string w2(filenames[1]);
  
  if( w1.length()>4&&w2.length()>4&&((w1.substr(w1.length()-4,w1.length())==".tok" && w2.substr(w2.length()-4,w2.length())==".tok" )||
				     (w1.substr(w1.length()-4,w1.length())==".txt" && w2.substr(w2.length()-4,w2.length())==".txt" ) ))
    {
      w1=w1.substr(0,w1.length()-4);
      w2=w2.substr(0,w2.length()-4);
      cerr << "w1:"<< w1 << " w2:" << w2 << endl;
    } 
      

  string vocab1(w1),vocab2(w2),snt1,snt2;
  unsigned int slashpos=vocab1.rfind('/')+1;
  if( slashpos>=vocab1.length() ) slashpos=0;
  string vocab1x(vocab1.substr(slashpos,vocab1.length()));
  cout << vocab1 << " -> " << vocab1x << endl;
  slashpos=vocab2.rfind('/')+1;
  if( slashpos>=vocab2.length() ) slashpos=0;
  string vocab2x(vocab2.substr(slashpos,vocab2.length()));
  cout << vocab2 << " -> " << vocab2x << endl;  
  snt1=vocab1+"_"+vocab2x+string(".snt");
  snt2=vocab2+"_"+vocab1x+string(".snt");
  vocab1+=string(".vcb");
  vocab2+=string(".vcb");

  ofstream ovocab1(vocab1.c_str()),ovocab2(vocab2.c_str()),osnt1(snt1.c_str()),osnt2(snt2.c_str());
  for(unsigned int i=0;i<filenames.size();i+=2)
    {
      ifstream i1(filenames[i].c_str()),i2(filenames[i+1].c_str());
      if(!i1)cerr << "WARNING: " << filenames[i] << " cannot be read.\n";
      if(!i2)cerr << "WARNING: " << filenames[i+1] << " cannot be read.\n";
      while(getline(i1,line1) && getline(i2,line2) )
	{
	  vector<string> t1,t2;
	  istringstream ii1(line1);
	  while(ii1>>word)
	    {
	      t1.push_back(word);
	      v1[word]++;
	      if( id1.find(word)==id1.end() )
		{
		  iid1.push_back(word);
		  id1[word]=iid1.size()-1;
		}
	    }
	  istringstream ii2(line2);
	  while(ii2>>word)
	    {
	      t2.push_back(word);
	      v2[word]++;
	      if( id2.find(word)==id2.end() )
		{
		  iid2.push_back(word);
		  id2[word]=iid2.size()-1;
		}
	    }
	  double w=1.0;
	  if( i/2<weights.size() )
	    w=weights[i/2];
	  if( t1.size()&&t2.size() )
	    {
	      osnt1 << w << "\n";
	      for(unsigned int j=0;j<t1.size();++j)osnt1 << id1[t1[j]] << ' ';
	      osnt1 << '\n';
	      for(unsigned int j=0;j<t2.size();++j)osnt1 << id2[t2[j]] << ' ';
	      osnt1 << '\n';

	      osnt2 << w << "\n";
	      for(unsigned int j=0;j<t2.size();++j)osnt2 << id2[t2[j]] << ' ';
	      osnt2 << '\n';
	      for(unsigned int j=0;j<t1.size();++j)osnt2 << id1[t1[j]] << ' ';
	      osnt2 << '\n';
	    }
	  else
	    cerr << "WARNING: filtered out empty sentence (source: " << filenames[i] << " " << t1.size() <<
	      " target: " << filenames[i+1] << " " << t2.size() << ").\n";
	}
    }
  
  for(unsigned int i=2;i<iid1.size();++i)
    ovocab1 << i << ' ' << iid1[i] << ' ' << v1[iid1[i]] << '\n';
  for(unsigned int i=2;i<iid2.size();++i)
    ovocab2 << i << ' ' << iid2[i] << ' ' << v2[iid2[i]] << '\n';
}
