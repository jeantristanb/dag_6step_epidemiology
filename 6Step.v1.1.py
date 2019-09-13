import itertools
import sys
import argparse


class node :
    def __init__(self, name):
       self.list_parents=[]
       self.list_children=[]
       self.listnorient=[]
       self.name=name
       self.checked=False
    def initlist_children(self, list_children) :
        self.list_children=list_children
        for son in list_children :
             son.appendfather(self)
    def appendfather(self,father) :
        if father not in self.list_parents :
           self.list_parents.append(father)
    def __str__(self):
        return "name "+self.name+":  list_children "+",".join([x.name for x in self.list_children]) + " list father "+",".join([x.name for x in self.list_parents]) + " status" + str(self.checked)+" list no oriente"+ ",".join([x.name for x in self.listnorient])
    def deleteconnexionorient(self):
        for son in self.list_children :
            son.list_parents.remove(self)
        for father in self.list_parents :
            father.list_children.remove(self)
    def getancestor(self):
        if self.checked :
            return []
        self.checked=True
        listancestor=[]
        for x in self.list_parents :
           if x.checked==False :
               listancestor.append(x.name)
               listancestor+=x.getancestor()
        return listancestor
    def getdescent(self) :
       if self.checked :
           return []
       self.checked=True
       listdescent=[]
       for x in self.list_children :
           if x.checked==False :
              listdescent.append(x.name)
              listdescent+=x.getdescent()
       return listdescent
    def dellinkson(self):
        for x in self.list_children :
            x.list_parents.remove(self)
        self.list_children=[]
    def appendnorient(self, node):
        if node not in self.listnorient :
           self.listnorient.append(node)
           if self not in node.listnorient :
              node.listnorient.append(self)
    def connectparents(self) :
        npar=len(self.list_parents)
        for cmtp in range(0,npar-1):
            for cmtp2 in range(cmtp+1,npar):
                self.list_parents[cmtp].appendnorient(self.list_parents[cmtp2])
                self.list_parents[cmtp2].appendnorient(self.list_parents[cmtp])
    def unoriented(self) :
        for x in self.list_parents :
            self.appendnorient(x)
        for x in self.list_children :
            self.appendnorient(x)
        self.list_parents=[]
        self.list_children=[]
    def getallconnexion(self) :
        if self.checked :
            return []
        self.checked=True
        listconnect=[]
        for x in self.listnorient:
           if x.checked==False :
               listconnect.append(x.name)
               listconnect+=x.getallconnexion()
        return listconnect
    def delconnexun(self) :
        for x in self.listnorient :
            x.listnorient.remove(self)
        self.listnorient=[]
    def checkdirected(self) :
        listun=[] 
        for x in self.list_children :
            #if self.name in ["CKD","HTP"] and x.name in ["HTP", "CKD"]:
            #  print self.name,x.name, [y.name for y in x.list_children],self in x.list_children
            if self in x.list_children :
              listun.append([self.name,x.name])
        return listun
class network :
    def __init__(self, listinfo=None) :
       self.dicnode={}
       if listinfo :
          for x in listinfo :
            self.addnodelink(x[0],x[1])
    def addnodelink(self, namefather,listnameson) :
        list_children=[]
        for son in listnameson :
            list_children.append(self.createnode(son))
        father=self.createnode(namefather) 
        father.initlist_children(list_children)
    def createnode(self,name) :
        if name in self.dicnode :
            return self.dicnode[name]
        self.dicnode[name]=node(name)
        return self.dicnode[name]
    def __str__(self):
         chain="node number "+str(len(self.dicnode))+"\n"
         for name in self.dicnode.keys() :
             chain+=self.dicnode[name].__str__()+"\n"
         return chain
    def deletednode(self,nodename):
        self.dicnode[nodename].deleteconnexionorient()
        del self.dicnode[nodename]
    def initcheck(self) :
        for x in self.dicnode :
            self.dicnode[x].checked=False
    def getancestor(self,nodename):
        lancestor=self.dicnode[nodename].getancestor()
        self.initcheck()
        return lancestor
    def getdescent(self,nodename):
        ldescent=self.dicnode[nodename].getdescent()
        self.initcheck()
        return ldescent
    def checknodename(self, namenode):
        if namenode not in self.dicnode :
            return False
        return True
    def getnodename(self) :
        return self.dicnode.keys()
    def dellinkson(self,namenode):
        self.dicnode[namenode].dellinkson()
    def connectallparent(self) :
        for x in self.dicnode.keys() :
            self.dicnode[x].connectparents()
    def unorientedall(self) :
        for x in self.dicnode.keys() :
            self.dicnode[x].unoriented()
    def delconnexun(self, listnamenode):
        for x in listnamenode :
            self.dicnode[x].delconnexun()
    def checkconnexion(self, node1name, node2name):
        lconnode1=self.dicnode[node1name].getallconnexion()
        self.initcheck()
        lconnode2=self.dicnode[node2name].getallconnexion()  
        self.initcheck()
        bal1=False
        bal2=False
        if node2name in lconnode1 :
            bal1=True
        if node1name in lconnode2 :
            bal2=True
        if bal1!=bal2 :
            raise OtherException("algoritms problem : discordant information in networl")
        return bal1
    def checkdirected(self) :
        listun=[]
        for x in self.dicnode.keys() :
            listunnode=self.dicnode[x].checkdirected()
            if len(listunnode)>0:
               listun.append(listunnode)
        return listun

class alg6step :
    def __init__(self, listinfo=None, effector=None, outcome=None,covariates=[]) :
       self.network=network(listinfo)
       self.effector=effector
       self.outcome=outcome
       self.covariates=covariates
       self.checknetwork()
    def checknetwork(self) :
        if self.network.checknodename(self.effector)==False:
            raise ValueError("effector "+self.effector+" not found in network")
        if self.network.checknodename(self.outcome)==False:
            raise ValueError("outcome "+self.outcome+" not found in network")
        for cov in self.covariates :
            if self.network.checknodename(cov)==False:
              raise ValueError("outcome "+cov+" not found in network")
        list_parentsson=self.network.checkdirected()
        if len(list_parentsson)>0 :
            raise ValueError("not directed connection :\n"+"\n".join(["=>".join(y) for x in list_parentsson for y in x]))
    def __str__(self):
        chaine="effector : "+ self.effector+" outcome : "+self.outcome+ " covariable test "+",".join(self.covariates)+"\n"
        chaine+=self.network.__str__()+"\n"
        return chaine
    def step1(self) :
        """
        the covariates chosen to reduce bias should not be descendants of effector (i.e. they should not be caused by warming up)
        """
        listdescent=self.network.getdescent(self.effector) 
        balise=True
        for cov in self.covariates :
            if cov in listdescent :
               balise=False
        return balise
    def step2(self) :
        """
        Delete all variables that satisfy all of the following: 1) non-ancestors (an ancestor is a variable that causes another variable either directly or indirectly) of X, 2) non-ancestors of the Outcome and 3) non-ancestors of the covariates that one is including to reduce bias (Z1 and Z2in this example)
        """
        allcov=[self.effector,self.outcome]
        allcov+=self.covariates
        listanceff=self.network.getancestor(self.effector)
        allcov+=listanceff
        listancanc=self.network.getancestor(self.outcome)
        allcov+=listancanc
        listancov=[]
        for cov in self.covariates :
            listancov+=self.network.getancestor(cov)
        allcov+=listancov
        allcov=set(allcov)
        diff=list(set(self.network.getnodename()) - set(allcov))
        for node in diff :
            self.network.deletednode(node)
        return diff
    def step3(self) :
        """
        Step 3 (figure 3a): Delete all lines emanating from X
        """
        self.network.dellinkson(self.effector)
    def step4(self) :
        """
        Step 4 (figure 3b): Connect any two parents (direct causes of a variable) sharing a common child (this step appears simple but it requires practice not to miss any)
        """
        self.network.connectallparent()
    def step5(self) :
        """
        Step 5 (figure 4a): Strip all arrowheads from lines
        """
        self.network.unorientedall() 
    def step6(self):
            self.network.delconnexun(self.covariates)
    def CheckConnectEffOut(self) :
        return self.network.checkconnexion(self.effector,self.outcome)
    def launchalgo(self) :
       checkst=self.step1()
       if checkst==False :
         return ('step1',False)
       self.step2()
       self.step3()
       self.step4()
       self.step5()
       self.step6()
       checkconnect=self.CheckConnectEffOut() 
       if checkconnect :
           return ('connect', False)
       return ('ok', True)

def getlistinfo(FileInfo, listexcl) :
   Lire=open(FileInfo)
   listinfo=[]
   for line in Lire :
    spl=line.split()
    namefather=spl[0]
    if namefather not in listexcl :
       list_children=spl[1].split(',')
       for x in listexcl :
           if x in list_children :
               list_children.remove(x)
       listinfo.append([namefather,list_children])
   return listinfo
def TestCov(listinfo,listcov,effector, Outcome) :
    allreswithcov=[]
    for cov in listcov :
       al=alg6step(listinfo,effector,Outcome,cov)
       res=al.launchalgo()
       #print al,cov
       allreswithcov.append([cov,res])
    return allreswithcov
#effector="HIV"
#Outcome="CKD"
#FileInfo="../arcgs2.txt"
#Out=""
def parseArguments():
    parser = argparse.ArgumentParser(description='apply 6 step algorithm see XX')
    parser.add_argument('--input_file',type=str,help="input file",required=True)
    parser.add_argument('--out_file',type=str,help="output file",required=True)
    parser.add_argument("--effector", help="effector to analys", type=str,required=True)
    parser.add_argument("--outcome", help="outcome to analyse",type=str, required=True)
    parser.add_argument("--excl", help="exclude some labels separate by ,", type=str)
    parser.add_argument("--model", help="model for 6steps : mc : minimal variable or mmc : merge minimal variable in multiple solution", type=str, default="mc")
    args = parser.parse_args()
    return args

def MinimalCovar(effector, Outcome,listallvar, listinfo, Out) :
    listcov=[[x] for x in listallvar]
    ## first step of algo we deleted 
    AllResCon=TestCov(listinfo,listcov,effector, Outcome)
    listcovnodes=[x[0][0] for x in AllResCon if x[1][0]!='step1']
    balise=True
    r=1
    while balise :
           perm=list(itertools.combinations(listcovnodes, r))
           listcov=[list(x) for x in perm]
           AllResCon=TestCov(listinfo,listcov,effector, Outcome)
           goodsol=[x for x in AllResCon if x[1][1]]
           if len(goodsol)>0 :
              break
           r+=1
           if r>len(listcovnodes) and balise:
              print "no solution found check your network :",Outcome, r, listcovnodes, effector
              raw_input()
              raise OtherException("no solution found check your network")
    Ecrire=open(Out, 'w')
    Ecrire.write("\n".join(["\t".join(x[0]) for x in goodsol])+"\n")
    Ecrire.close()

def MinimalCovarMergMult(effector, Outcome,listallvar, listinfo, Out) :
    listcov=[[x] for x in listallvar]
    ## first step of algo we deleted 
    AllResCon=TestCov(listinfo,listcov,effector, Outcome)
    listcovnodes=[x[0][0] for x in AllResCon if x[1][0]!='step1']
    balise=True
    r=1
    while balise :
       perm=list(itertools.combinations(listcovnodes, r))
       listcov=[list(x) for x in perm]
       AllResCon=TestCov(listinfo,listcov,effector, Outcome)
       goodsol=[x for x in AllResCon if x[1][1]]
       if len(goodsol)>0 :
          break
       r+=1
       if r>len(listcovnodes) and balise:
           print "no solution found check your network :",Outcome, r, listcovnodes, effector
           raw_input()
           raise OtherException("no solution found check your network")
    if len(goodsol)==1 :
       Ecrire=open(Out, 'w')
       Ecrire.write("\n".join(["\t".join(x[0]) for x in goodsol])+"\n")
       Ecrire.close()
    else : 
       allcovbon=list(set([item for sublist in goodsol for item in sublist[0]]))
       print allcovbon
       al=alg6step(listinfo,effector,Outcome,allcovbon)
       res=al.launchalgo()
       if res[1]==False :
           print "mmc have a problem "+ Outcome+" "+effector +" ".join(allcovbon)
           raw_input()
           sys.exit()
       Ecrire=open(Out, 'w')
       Ecrire.write("\t".join(allcovbon)+"\n")
       Ecrire.close()

def LargeCovar(effector, Outcome,listallvar, listinfo, Out) :
    listcov=[[x] for x in listallvar]
    ## first step of algo we deleted
    AllResCon=TestCov(listinfo,listcov,effector, Outcome)
    listcovnodes=[x[0][0] for x in AllResCon if x[1][0]!='step1']
    balise=True
    r=len(listcovnodes)
    while balise :
       perm=list(itertools.combinations(listcovnodes, r))
       listcov=[list(x) for x in perm]
       AllResCon=TestCov(listinfo,listcov,effector, Outcome)
       goodsol=[x for x in AllResCon if x[1][1]]
       if len(goodsol)>0 :
          break
       r-=1
       if r==0 and balise:
           print "no solution found check your network :",Outcome, r, listcovnodes, effector
           raw_input()
           raise OtherException("no solution found check your network")
    Ecrire=open(Out, 'w')
    Ecrire.write("\n".join(["\t".join(x[0]) for x in goodsol])+"\n")
    Ecrire.close()


        




args=parseArguments()

effector=args.effector
Outcome=args.outcome
FileInfo=args.input_file
Out=args.out_file
listexcl=[]
if args.excl :
   listexcl=args.excl.split(",")

listinfo=getlistinfo(FileInfo, listexcl)

listallvar=[x[0] for x in listinfo]
for x in listinfo :
    listallvar+=x[1]
listallvar=list(set(listallvar))
if effector not in listallvar :
    print "Effector "+effector+ " not found"
    sys.exit()

listallvar.remove(effector)
if Outcome not in listallvar :
    print "Outcome "+Outcome+ " not found"
    sys.exit()
listallvar.remove(Outcome)

if args.model=="mc" :
   MinimalCovar(effector, Outcome,listallvar, listinfo, Out)
elif args.model=="mmc":
   MinimalCovarMergMult(effector, Outcome,listallvar, listinfo, Out)
elif args.model=="lc":
   LargeCovar(effector, Outcome,listallvar, listinfo, Out)





