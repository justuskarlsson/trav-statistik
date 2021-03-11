
data = read.csv("../data/2021-03-06_4/data.csv", sep=";")
#data = read.csv("../data/2021-02-20_200.csv", sep=";")


val = data$vOdds * data$won
data$val = val
mean(data$val)
mean(data$vOdds)


favorites = data[data$vOdds < 2.0,]
mean(favorites$val)


print_horses = function(horses){
  for (i in 1:dim(horses)[1]) {
    s = sprintf("%d-%d", horses$raceIdx[i], horses$horseNumber[i]+1)
    print(s)
  }
}

v_val = function(){
  data = subset(data, select=c(-Plats., -plats, -result, -won))
  n = dim(data)[1]
  set.seed(12345)
  id = sample(1:n, floor(0.8* n))
  train_set = data[id,] 
  test_set = data[-id,]
  
  model = lm(val~., train_set)
  
  preds = predict(model, newdata=test_set)
  print(sort(preds, decreasing=TRUE)[1:200])
  
  # This really seems like the sweet stop, tested 3 times
  bets = intersect(which(preds > 1.04), which(preds < 1.2))
  horses = test_set[bets,]
  length(horses)
  print(mean(horses$val))
  print(mean(horses$vOdds))
  

  
  return (horses)
}




