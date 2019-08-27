plot_rc_cn <- function(file_for_plot, pdf_output, legend1, legend2) {
    # The 3rd, 4th and 5th column in file_for_plot are read count, the absolute copy number whose legend is legend1, the absolute copy number whole legend is legend2. 
    a<-read.table(file_for_plot)
    rc=a$V3
    hc_correct=a$V4
    hc_wrong=a$V5
    #mad_=mad(rc/mean(rc))
    #print(mad_)
    pdf(pdf_output)
    #par(mfrow=c(1,2))
    plot(rc, cex=0.1, ylim=c(0, 900), xlab="Bin Index on Whole Genome", ylab="Raw Read Count")
    par(new = T)
    plot(hc_correct, cex=0.4, ylim=c(0, 8.8), col="red", axes=F, ylab=NA, xlab=NA)
    axis(side=4)
    mtext(side = 4, line = 2, 'Absolute Copy Number')
    points(hc_wrong, cex=0.1, col="blue")
    legend("topright",
           legend=c("legend1", "legend2"),
           lty=c(1,1), col=c("red", "blue"), pt.cex=0.5, bty="n")
    # get the difference between the method and the ground truth
    #x=integer(length(gt))
    #x[gt==hc]=1
    #plot(x, cex=0.1, ylim=c(-0.5, 4), ylab="consistency of inferred", main="difference btw hmmcopy and gt")
    dev.off()
}
