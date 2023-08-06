# CubiCal: a radio interferometric calibration suite
# (c) 2017 Rhodes University & Jonathan S. Kenyon
# http://github.com/ratt-ru/CubiCal
# This code is distributed under the terms of GPLv2, see LICENSE.md for details

# This module has been adapted from the DDFacet package,
# (c) Cyril Tasse et al., see http://github.com/saopicc/DDFacet
from __future__ import print_function
from builtins import range
import os
import sys
from . import ModColor

class ClassPrint():
    def __init__(self,HW=20,quote='"'):
        self.LeftW=HW
        self.WV0=50
        self.WV1=30
        self.WidthHelp=30
        self.quote=quote
        self.proto=" - %s %s %s : "
        self.Lproto=len(self.proto.replace("%s",""))


    def getWidth(self):
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(columns)

    def Print(self,par,value,value2=None,dest=sys.stdin):
        parout=" - %s %s"%(par,"."*(self.LeftW-len(par)))
        if value2 is None:
            valueOut=value
        else:
            valueOut="%s%s"%(value.ljust(self.WV0),(""" "%s" """%value2).rjust(self.WV1))
        print("%s = %s"%(parout,valueOut), file=dest)
        
    def Print2(self,par,value,helpit,col="white"):
        WidthTerm=self.getWidth()
        Lpar=len(str(par))
        Lval=len(str(value))
        SFill="."*max(self.LeftW-self.Lproto-Lpar-Lval,2)
        WidthHelp=WidthTerm-(self.Lproto+Lpar+Lval+len(SFill))
        Spar="%s"%ModColor.Str(str(par),col=col,Bold=False)
        Sval="%s"%ModColor.Str(str(value),col=col,Bold=False)
        if helpit=="":
            helpit="Help yourself"
        Shelp="%s"%helpit
        if WidthHelp<0:
             print(self.proto%(Spar,SFill,Sval)+Shelp)
             return
        Lhelp=len(str(helpit))
        listStrHelp=list(range(0,Lhelp,WidthHelp))
        
        if listStrHelp[-1]!=Lhelp: listStrHelp.append(Lhelp)
        
        
        
        print(self.proto%(Spar,SFill,Sval)+Shelp[0:WidthHelp])
        for i in range(1,len(listStrHelp)-1):
            parout="%s: %s"%(" "*(self.LeftW-2),Shelp[listStrHelp[i]:listStrHelp[i+1]])
            print(parout)
