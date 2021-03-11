source("utils.r")

#data = read.csv("../data/2021-03-06_4/data.csv", sep=";")

data = read.csv("../data/2021-03-06_250/data.csv", sep=";")

data[data$betDistribution == 0.0,] = 0.0001


data$v75val = (1/data$betDistribution) * data$won


# PREDICTION
data = subset(data, select=c(-Plats., -plats, -result, -won, -pValue))
pred_data = read.csv("../data/2021-03-13-prediction/data.csv", sep=";")
model = lm(v75val~., data)
preds = predict(model, newdata=pred_data)
preds[is.na(preds)] = -2.0

pred_data$v75Pred = preds

print_set = subset(pred_data, select = c(raceIdx, horseNumber, vOdds, pOdds, Poäng, v75Pred))
print_set$horseNumber = print_set$horseNumber + 1


# TESTING

n = dim(data)[1]
set.seed(123456)
id = sample(1:n, floor(0.9* n))

train_set = data[id,] 
test_set = data[-id,]





model = lm(v75val~., train_set)

preds = predict(model, newdata=test_set)
preds[is.na(preds)] = -2.0

test_set$v75Pred = preds

print_set = subset(test_set, select = c(raceIdx, horseNumber, vOdds, pOdds, Poï..ng, v75val, v75Pred))

best = test_set[test_set$v75Pred > 2.0,]
mean(best$v75val)
mean(test_set$v75val)
