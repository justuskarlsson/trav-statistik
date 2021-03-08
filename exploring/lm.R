
data = read.csv("../data/2021-02-20_200.csv", sep=";")


val = data$vOdds * data$won
mean(val[val > 0.0])
data$val = val


favorites = data[data$vOdds < 2.0,]


data = subset(data, select=c(-Plats., -plats, -result, -won))
n = dim(data)[1]
set.seed(12345)
id = sample(1:n, floor(0.8* n))
train_set = data[id,] 
test_set = data[-id,]


model = lm(val~., train_set)


# Always pick yes on a horse with really low odds (a lot of people have betted on it)
choose_favorite = function(data, rate) {
  n = dim(data)[1]
  ans = rep(0, n)
  for (i in 1:n) {
    if (data$vOdds[i] <= rate) {
      ans[i] = 1
    }
  }
  return (ans)
}

# Evaluates how good a model is at deciding whether a horse is going to
# win or not. More than 1.0 means that it's better than always choosing
# that it will lose.
eval = function (pred) {
  n = dim(test_set)[1]
  correct = sum(pred == test_set$won) / n
  lose_rate = sum(1 - test_set$won) / n
  return (correct - lose_rate + 1)
  
}

eval_favorite = function(rate) {
  acc = eval(choose_favorite(test_set, rate))
  s = sprintf("Only choose horse which every %.1f gambler thinks is going to win (all others horses lose). Eval: %.4f", rate, acc)
  print(s)
}



s = sprintf("Our model. Eval: %.2f", eval(predict(model, newdata=test_set)))
print(s)


preds = predict(model, newdata=test_set)
sort(preds, decreasing=TRUE)[1:20]

bets = which(preds > 1.0 && preds < 1.2)
mean(test_set$val[bets])
