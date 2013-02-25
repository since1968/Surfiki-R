qplot(as.POSIXlt(dTItemDateTime/1000, origin="1970-01-01", tz="America/New_York"), data = obama, geom = "density")


qplot(as.POSIXlt(dTItemDateTime/1000, origin="1970-01-01 00:00:00", tz="America/New_York"), data = obama, geom = "density", colour = strOpinon)


