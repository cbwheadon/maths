library("R2jags")
## Set working directory
setwd("C:/Users/User/BitNami DjangoStack projects/maths/rasch")
##============================================================
##
## Basic IRT Models
##
##============================================================
##------------------------------------------------------------
## Two Parameter Logistic IRT Model
set.seed(31032012)
Y <- matrix(responses,nrow=1)

n <- 1
p <- ncol(Y)
m.delta <- 0.0
s.delta <- 1.0

data <- list("Y", "n", "p", "m.delta", "s.delta","m.theta","s.theta")
monitor <- c("theta")
jags.file <- file.path(getwd(), "rasch.txt")
system.time(jagsout <- jags(data=data, inits=NULL, parameters.to.save=monitor,
                            model.file=jags.file,
                            n.iter=1000, n.thin=1, n.burnin=500))

thm <- jagsout$BUGSoutput$median$theta[1]
ths <- jagsout$BUGSoutput$sd$theta[1]

probs <- pnorm(grades, mean = thm, sd = ths, lower.tail=FALSE)