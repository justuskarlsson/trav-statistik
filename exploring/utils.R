print_horses = function(horses){
  for (i in 1:dim(horses)[1]) {
    s = sprintf("%d-%d", horses$raceIdx[i], horses$horseNumber[i]+1)
    print(s)
  }
}

factorize_data = function(data) {
  data$horseNumber = factor(data$horseNumber)
  #data$horseName = factor(data$horseName)
  data$cartInfo = factor(data$cartInfo)
  data$horseSex = factor(data$horseSex)
  data$shoeInfo = factor(data$shoeInfo)
  #data$driver = factor(data$driver)
  #data$Tränare = factor(data$Tränare)
  #data$Hemmabana = factor(data$Hemmabana)
  #data$recordSuffix = factor(data$recordSuffix)
  #data$recordDecimal = factor(data$recordDecimal)
  return (data)
}

trim_v75_data = function(data) {
  subset(data, c(-vOdds, -pOdds))
}
