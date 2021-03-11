print_horses = function(horses){
  for (i in 1:dim(horses)[1]) {
    s = sprintf("%d-%d", horses$raceIdx[i], horses$horseNumber[i]+1)
    print(s)
  }
}