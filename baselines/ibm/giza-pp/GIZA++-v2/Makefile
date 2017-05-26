.SUFFIXES: .out .o .c .e .r .f .y .l .s .p .cpp .alpha2o .pentiumo .sgio .alphao

INSTALLDIR ?= /usr/local/bin/

#CXX = g++

CFLAGS = $(CFLAGS_GLOBAL) -Wall -Wno-parentheses
#CFLAGS_OPT = $(CFLAGS) -O3 -DNDEBUG -DWORDINDEX_WITH_4_BYTE -O3 -DNDEBUG -DWORDINDEX_WITH_4_BYTE -ffast-math
CFLAGS_OPT = $(CFLAGS) -O3 -funroll-loops -DNDEBUG -DWORDINDEX_WITH_4_BYTE -DBINARY_SEARCH_FOR_TTABLE -DWORDINDEX_WITH_4_BYTE
CFLAGS_PRF = $(CFLAGS) -O2 -pg -DNDEBUG -DWORDINDEX_WITH_4_BYTE
CFLAGS_DBG = $(CFLAGS) -g -DDEBUG -DWORDINDEX_WITH_4_BYTE
CFLAGS_NRM = $(CFLAGS) -DWORDINDEX_WITH_4_BYTE
CFLAGS_VDBG = $(CFLAGS) -g -DDEBUG -DWORDINDEX_WITH_4_BYTE -DVDEBUG
SRC = *.cpp
TYPE = 
LDFLAGS =

include Makefile.src

OBJ_DIR_PRF = profile/
OBJ_DIR_OPT = optimized/
OBJ_DIR_DBG = debug/
OBJ_DIR_VDBG = vdebug/
OBJ_DIR_NRM = norm/
OBJ_OPT2 = ${SRC2:%.cpp=$(OBJ_DIR_OPT)%.o}
OBJ_OPT = ${SRC:%.cpp=$(OBJ_DIR_OPT)%.o}
OBJ_DBG = ${SRC:%.cpp=$(OBJ_DIR_DBG)%.o}
OBJ_VDBG = ${SRC:%.cpp=$(OBJ_DIR_VDBG)%.o}
OBJ_NRM = ${SRC:%.cpp=$(OBJ_DIR_NRM)%.o}
OBJ_PRF = ${SRC:%.cpp=$(OBJ_DIR_PRF)%.o}
OBJ_DIR = 
DATE = `date +%d-%m-%Y`

opt: GIZA++ snt2plain.out plain2snt.out snt2cooc.out

GIZA++: $(OBJ_DIR_OPT) $(OBJ_OPT) 
	$(CXX) $(CFLAGS_OPT) $(OBJ_OPT) $(LDFLAGS) -o GIZA++

prf: GIZA++.prf

GIZA++.prf: $(OBJ_DIR_PRF) $(OBJ_PRF) 
	$(CXX) $(CFLAGS_PRF) $(OBJ_PRF) -o GIZA++.prf $(LDFLAGS)

dbg: GIZA++.dbg

GIZA++.dbg: $(OBJ_DIR_DBG) $(OBJ_DBG) 
	$(CXX) $(CFLAGS_DBG) $(OBJ_DBG) -o GIZA++.dbg $(LDFLAGS)

vdbg: GIZA++.vdbg

GIZA++.vdbg: $(OBJ_DIR_VDBG) $(OBJ_VDBG) 
	$(CXX) $(CFLAGS_VDBG) $(OBJ_VDBG) -o GIZA++.vdbg $(LDFLAGS)

nrm: GIZA++.nrm 

GIZA++.nrm: $(OBJ_DIR_NRM) $(OBJ_NRM) 
	$(CXX) $(CFLAGS_NRM) $(OBJ_NRM) -o GIZA++.nrm $(LDFLAGS)

all: dbg opt nrm prf 

$(OBJ_DIR_PRF): $(OBJ_DIR)
	-mkdir $(OBJ_DIR_PRF)

$(OBJ_DIR_OPT): $(OBJ_DIR)
	-mkdir $(OBJ_DIR_OPT)

$(OBJ_DIR_DBG): $(OBJ_DIR)
	-mkdir $(OBJ_DIR_DBG)

$(OBJ_DIR_VDBG): $(OBJ_DIR)
	-mkdir $(OBJ_DIR_VDBG)

$(OBJ_DIR_NRM): $(OBJ_DIR)
	-mkdir $(OBJ_DIR_NRM)

$(OBJ_DIR):
	-mkdir $(OBJ_DIR)

$(OBJ_DIR_DBG)%.o: %.cpp
	$(CXX)  $(CFLAGS_DBG)  -c $< -o $@

$(OBJ_DIR_VDBG)%.o: %.cpp
	$(CXX)  $(CFLAGS_VDBG)  -c $< -o $@

$(OBJ_DIR_NRM)%.o: %.cpp
	$(CXX)  $(CFLAGS_NRM)  -c $< -o $@

$(OBJ_DIR_PRF)%.o: %.cpp
	$(CXX)  $(CFLAGS_PRF) -c $< -o $@

$(OBJ_DIR_OPT)%.o: %.cpp
	$(CXX)  $(CFLAGS_OPT)  -c $< -o $@

iinstall: opt prf dbg
	-mkdir $(INSTALLDIR)/$(ARCH)
	-cp GIZA++ $(INSTALLDIR)/GIZA++
	-cp GIZA++.prf $(INSTALLDIR)/GIZA++.prf
	-cp GIZA++.dbg $(INSTALLDIR)/GIZA++.dbg

install: opt 
	-mkdir $(INSTALLDIR)
	-cp GIZA++ $(INSTALLDIR)/GIZA++

clean:
	-rm -f $(OBJ_DIR_NRM)/*.o $(OBJ_DIR_DBG)/*.o $(OBJ_DIR_VDBG)/*.o $(OBJ_DIR_PRF)/*.o $(OBJ_DIR_OPT)/*.o
	-rm -rf $(OBJ_DIR_NRM) $(OBJ_DIR_DBG) $(OBJ_DIR_VDBG) $(OBJ_DIR_PRF) $(OBJ_DIR_OPT)
	-rm -f snt2plain.out plain2snt.out snt2cooc.out GIZA++


backup: clean
	tar cf - . | gzip -9 > ../GIZA++src.tar.gz

depend: depend_CLEAN dependencies

depend_CLEAN:
	rm dependencies

dependencies:
	@(echo "#Automatically generated dependecy list" >>  dependencies ;\
	$(CXX) -MM *.cpp $(CFLAGS_OPT) | perl -e 'while(<>){s?^([^\:]+\.o:)?$(OBJ_DIR_OPT)\1?g;print;}'>>  dependencies)
	@(echo "#Automatically generated dependecy list" >>  dependencies ;\
	$(CXX) -MM *.cpp $(CFLAGS_DBG) | perl -e 'while(<>){s?^([^\:]+\.o:)?$(OBJ_DIR_DBG)\1?g;print;}'>>  dependencies)
	@(echo "#Automatically generated dependecy list" >>  dependencies ;\
	$(CXX) -MM *.cpp $(CFLAGS_VDBG) | perl -e 'while(<>){s?^([^\:]+\.o:)?$(OBJ_DIR_VDBG)\1?g;print;}'>>  dependencies)
	@(echo "#Automatically generated dependecy list" >>  dependencies ;\
	$(CXX) -MM *.cpp $(CFLAGS_NRM) | perl -e 'while(<>){s?^([^\:]+\.o:)?$(OBJ_DIR_NRM)\1?g;print;}'>>  dependencies)
	@(echo "#Automatically generated dependecy list" >>  dependencies ;\
	$(CXX) -MM *.cpp $(CFLAGS_PRF) | perl -e 'while(<>){s?^([^\:]+\.o:)?$(OBJ_DIR_PRF)\1?g;print;}'>>  dependencies)

-include dependencies

snt2plain.out: snt2plain.cpp
	$(CXX) $(LDFLAGS) -O3 -W -Wall snt2plain.cpp -o snt2plain.out

plain2snt.out: plain2snt.cpp
	$(CXX) $(LDFLAGS) -O3 -W -Wall plain2snt.cpp -o plain2snt.out

snt2cooc.out: snt2cooc.cpp
	$(CXX) $(LDFLAGS) -O3 -g -W -Wall snt2cooc.cpp -o snt2cooc.out

