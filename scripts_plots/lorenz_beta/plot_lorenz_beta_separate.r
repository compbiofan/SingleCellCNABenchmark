plot_lorenz_beta_separate <- function(pdf_file){
    pdf(pdf_file)
    x=0:100
    x=x/100
    cex=0.2
    axis_cex=1.5
    lab_cex=1.6
    par(mfrow=c(4,2))
    a=1.23
    plot(pbeta(x, a, a), pbeta(x, a+1, a), main="MALBAC Lorenz (x=0.5, y=0.27)", pch=16, cex=cex, xlab="bin (%)", ylab="read count (%)", cex.axis=axis_cex, cex.lab=lab_cex)
    lines(pbeta(x, a, a), pbeta(x, a+1, a), type="l", col="red")
    plot(x, dbeta(x, a, a), main="MALBAC Beta (a=b=1.23)", pch=16, cex=cex, xlab="normalized read count", ylab="probability", cex.axis=axis_cex, cex.lab=lab_cex)
    lines(x, dbeta(x, a, a), type="l", col="red")
    
    a=1.38
    plot(pbeta(x, a, a), pbeta(x, a+1, a), main="DOP-PCR Lorenz (x=0.5, y=0.28)", pch=16, cex=cex, xlab="bin (%)", ylab="read count (%)", cex.axis=axis_cex, cex.lab=lab_cex)
    lines(pbeta(x, a, a), pbeta(x, a+1, a), type="l", col="red")
    plot(x, dbeta(x, a, a), main="DOP-PCR Beta (a=b=1.38)", pch=16, cex=cex, xlab="normalized read count", ylab="probability", cex.axis=axis_cex, cex.lab=lab_cex)
    lines(x, dbeta(x, a, a), type="l", col="red")
    
    a=2.49
    plot(pbeta(x, a, a), pbeta(x, a+1, a), main="TnBC Lorenz (x=0.5, y=0.33)", pch=16, cex=cex, xlab="bin (%)", ylab="read count (%)", cex.axis=axis_cex, cex.lab=lab_cex)
    lines(pbeta(x, a, a), pbeta(x, a+1, a), type="l", col="red")
    plot(x, dbeta(x, a, a), main="TnBC Beta (a=b=2.49)", pch=16, cex=cex, xlab="normalized read count", ylab="probability", cex.axis=axis_cex, cex.lab=lab_cex)
    lines(x, dbeta(x, a, a), type="l", col="red")
    
    a=5.27
    plot(pbeta(x, a, a), pbeta(x, a+1, a), main="Bulk Lorenz (x=0.5, y=0.38)", pch=16, cex=cex, xlab="bin (%)", ylab="read count (%)", cex.axis=axis_cex, cex.lab=lab_cex)
    lines(pbeta(x, a, a), pbeta(x, a+1, a), type="l", col="red")
    plot(x, dbeta(x, a, a), main="Bulk Beta (a=b=5.27)", pch=16, cex=cex, xlab="normalized read count", ylab="probability", cex.axis=axis_cex, cex.lab=lab_cex)
    lines(x, dbeta(x, a, a), type="l", col="red")
    
    dev.off()
}
