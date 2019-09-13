library(corrplot)
library(dagitty)
library(ggdag)
## N ind
nind<-10000
## data read of interaction terms between variable
## first column is effector 
##second column is what variable influes
## third column beta values
## fourth column sd of beta value
### example case 
###   A  E
##   / \/  \
##  B  C   |
##  \  / \ /
##    D   F
dataI<-read.table('ressource/Pheno.sim.info',stringsAsFactors=F)

## plot DAG
DataIPlot<-dataI
dag <- dagitty(paste("dag{",paste(paste(DataIPlot[,1],"->",DataIPlot[,2],paste=""),collapse=";"),"}",sep=""))
jpeg('ressource/Dag_datasettest.jpeg')
ggdag(dag)
dev.off()



phenolist<-as.character(unique(c(dataI[,1],dataI[,2])))
## we added NA for var without effect
VarNoEffect<-dataI[!(dataI[,2] %in% dataI[,1]),2]
data<-rbind(dataI,cbind(V1=unique(VarNoEffect),V2=NA,V3=NA,V4=NA))

### algorihtm to generate phenotype
## selectio of parents
phenolistrun<-phenolist
datatmp<-data
## data frame of initial phenotype : normal law
DataGenerated<-as.data.frame(matrix(rnorm(length(phenolist)*nind), nrow=nind, ncol=length(phenolist)))
names(DataGenerated)<-as.character(phenolist)
## while all variables have not been generated
Cmt<-1
while(length(phenolistrun)>0){
## select parents where there is not in children
listvarstudy<-unique(datatmp[!(datatmp[,1] %in% datatmp[!is.na(datatmp[,2]),2]),1])
print(listvarstudy)
if(length(listvarstudy)==0){
print('error in data ')
print(datatmp)
q()
}
## for each var 
for(var in listvarstudy){
## for each var select parents should be influence variables
listparents=dataI[dataI[,2]==var,1]
#select for each parents B value and Sd change variables with normal law
for(parents in listparents)DataGenerated[,var]=DataGenerated[,var]+DataGenerated[,parents]*rnorm(length(DataGenerated[,var]) ,dataI[dataI[,2]==var & dataI[,1]==parents,3], dataI[dataI[,2]==var & dataI[,1]==parents,4])
}
## deleted variables have been study
phenolistrun<-phenolistrun[!(phenolistrun %in% listvarstudy)]
datatmp<-datatmp[!(datatmp[,1] %in% listvarstudy),]
Cmt<-Cmt+1
}

## plot data

## relation between variable
jpeg('ressource/corrplot_datasettest.jpeg')
corrplot(cor(DataGenerated))
dev.off()
if(!file.exists())write.csv(cbind(ID=1:nrow(DataGenerated),DataGenerated),file="ressource/test_data.csv", row.names=F)




