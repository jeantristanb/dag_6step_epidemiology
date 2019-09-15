library(corrplot)
##library bnlearn to build dag with data
library(bnlearn)



## charge data : in the case data example generate with script : simulate_phenotype.r
DataPheno<-read.csv('ressource/test_data.csv')
## relation between variable
jpeg('ressource/corrplot_datasettest.jpeg')
corrplot(cor(DataPheno[,-1]))
dev.off()

## plot of  
gsexcl<-gs(DataPheno[,-1])

jpeg('ressource/dagnbnlearn_noexcl.jpeg')
graphviz.plot(gsexcl)
dev.off()

## in this case we see a A<->B so we black list B->A 
RelatEx<-matrix(c("B","A"), ,nrow=1)
gsexcl<-gs(DataPheno[,-1],blacklist=RelatEx)
jpeg('ressource/dagnbnlearn_exclAB.jpeg')
graphviz.plot(gsexcl)
dev.off()

## write in format for 6-step procedure algorithmn
gsexclarcs<-as.data.frame(gsexcl$arcs)
gsexclarcs<-aggregate(to~from,data=gsexclarcs,paste, collapse=",")
write.table(gsexclarcs, file=paste('ressource/dag_bnlearn.tab'), row.names=F, col.names=F, quote=F)










