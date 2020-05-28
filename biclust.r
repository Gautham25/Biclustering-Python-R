install.packages("biclust")
library(biclust)

#Read data from csv file
data <- read.csv("../Data/CleanData/BCData.csv", header=TRUE)

#Initialize fields to be dropped from data
drops <- c("SubId","Q4.2.2.","Q4.3.")
#Remove ColorBlindness Questions
drops <- c(drops,"Q6.2.","Q6.3.","Q6.4.","Q6.5.","Q6.6.","Q6.7.","Q6.8.")

rnames <- c()
cnames <- c()

for (i in data[,1:1]) {
  x <- toString(i)
  rnames <- c(rnames,x)
}

#Drop fields from data
data <- data[ ,!(names(data) %in% drops)]

cnames <- c(colnames(data))


rows <- nrow(data)
cols <- ncol(data)

#Create matrix from dataframe
bmat <- matrix(unlist(data),nrow=rows,ncol=cols)

i=0.1
j=1
mdf <- data.frame("Delta"=double(), "NoC"=integer())

li <- list()
while (i<=0.2){
  z <- biclust(bmat,BCCC,i,1,100)
  l1 <- c(i,z@Number)
  mdf <- rbind(mdf, data.frame("Delta"=i,"NoC"=z@Number))
  fname = paste("result_",j,".txt",sep = "")
  cfname = "text/variance.txt"
  write(paste("Delta = ",i),cfname,append = TRUE)
  write(paste("Number of Clusters = ",z@Number,sep = ""),cfname,append = TRUE)
  write("Cluster,ConstantVariance,AdditiveVariance,MultiplicativeVariance,SignVariance",cfname,append = TRUE)
  k <- 1
  while(k <= z@Number){
    x <- ""
    cluster <- k
    cv <- constantVariance(bmat,z,k,dimension = "row")
    av <- additiveVariance(bmat,z,k,dimension = "row")
    mv <- multiplicativeVariance(bmat,z,k,dimension = "row")
    sv <- signVariance(bmat,z,k,dimension = "row")
    x <- paste(cluster,",",cv,",",av,",",mv,",",sv,sep = "")
    write(x,cfname,append = TRUE)
    k <- k+1
  }
  write("\n",cfname,append = TRUE)
  print(paste0("DELTA=",i),sep="")
  writeBiclusterResults(fileName = fname,z,paste("BCCC Delta = ",i),rnames,cnames, delimiter = ",")
  i=i+0.01
  j=j+1

}
write.csv(mdf, "Delta-Clusters.csv",row.names=FALSE)
