#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
library(copynumber)
#### The first argument is the input 
#### The second argument is the output 
#### The third argument is the gamma 
print(args[1])
print(args[2])
print(args[3])
# Load the simulated data
#setwd("/Users/edrisi/Documents/CNV_project/scripts")
df<-read.csv(file = args[1])

# winsorize data to handle the outliers 
wins.mydata <- winsorize(df)

# Run multipcf 
multipcf.segments <- multipcf(data=wins.mydata, gamma = strtoi(args[3],0L), Y=df)
write.csv(multipcf.segments, file =paste(args[2],".csv",sep=""), row.names = FALSE)
