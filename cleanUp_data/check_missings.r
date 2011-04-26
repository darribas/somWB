# Print some statistics about the quality of the data
propmiss <- function(dataframe){
    # Function taken from
    # http://gettinggeneticsdone.blogspot.com/2011/02/summarize-missing-data-for-all.html
    lapply(dataframe,function(x) data.frame(nmiss=sum(is.na(x)),
            n=length(x), propmiss=sum(is.na(x))/length(x)))
}

data.link <- '/home/dani/AAA/LargeData/WDIandGDF_csv/WDI_GDF_Data.csv'
data <- read.csv(data.link, header=TRUE)
misstats <- propmiss(data)
