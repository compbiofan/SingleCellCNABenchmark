plot_lorenz_beta_summary <- function(pdf_file)
    pdf(pdf_file)
    par(mfrow=c(1,2))
    a=1.23
    plot(pbeta(x, a, a), pbeta(x, a+1, a), main="Lorenz", pch=16, cex=0.5, xlab="bin (%)", ylab="read count (%)")
    lines(pbeta(x, a, a), pbeta(x, a+1, a), type="l", col="red")
    a=1.38
    points(pbeta(x, a, a), pbeta(x, a+1, a), pch=16, cex=0.5)
    lines(pbeta(x, a, a), pbeta(x, a+1, a), type="l", col="blue")
    a=5.27
    points(pbeta(x, a, a), pbeta(x, a+1, a), pch=16, cex=0.5)
    lines(pbeta(x, a, a), pbeta(x, a+1, a), type="l", col="green")
    a=1.23
    plot(x, dbeta(x, a, a), main="Distribution of Read Count", pch=16, cex=0.5, xlab="read count (mean @ 0.5)", ylab="probability", ylim=c(0, 3))
    lines(x, dbeta(x, a, a), type="l", col="red")
    a=1.38
    points(x, dbeta(x, a, a), pch=16, cex=0.5)
    lines(x, dbeta(x, a, a), type="l", col="blue")
    a=5.27
    points(x, dbeta(x, a, a), pch=16, cex=0.5)
    lines(x, dbeta(x, a, a), type="l", col="green")
    
    dev.off()
    
    #a=1.38
    #plot(pbeta(x, a, a), pbeta(x, a+1, a), main="DOP-PCR Lorenz (a=b=1.38)", pch=16, cex=0.5, xlab="bin (%)", ylab="read count (%)")
    #lines(pbeta(x, a, a), pbeta(x, a+1, a), type="l", col="red")
    #plot(x, dbeta(x, a, a), main="Beta Distribution (a=b=1.38)", pch=16, cex=0.5, xlab="read count (%)", ylab="probability")
    #lines(x, dbeta(x, a, a), type="l", col="red")
    
    #a=2.49
    #plot(pbeta(x, a, a), pbeta(x, a+1, a), main="TNBC Lorenz (a=b=2.49)", pch=16, cex=0.5, xlab="bin (%)", ylab="read count (%)")
    #lines(pbeta(x, a, a), pbeta(x, a+1, a), type="l", col="red")
    #plot(x, dbeta(x, a, a), main="Beta Distribution (a=b=2.49)", pch=16, cex=0.5, xlab="read count (%)", ylab="probability")
    #lines(x, dbeta(x, a, a), type="l", col="red")
    
    #a=5.27
    #plot(pbeta(x, a, a), pbeta(x, a+1, a), main="Bulk Lorenz (a=b=5.27)", pch=16, cex=0.5, xlab="bin (%)", ylab="read count (%)")
    #lines(pbeta(x, a, a), pbeta(x, a+1, a), type="l", col="red")
    #plot(x, dbeta(x, a, a), main="Beta Distribution (a=b=5.27)", pch=16, cex=0.5, xlab="read count (%)", ylab="probability")
    #lines(x, dbeta(x, a, a), type="l", col="red")
}
