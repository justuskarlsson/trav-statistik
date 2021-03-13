#data = read.csv("../data/2021-03-06_4/data.csv", sep=";")

data = read.csv("../data/2021-03-06_500/data.csv", sep=";")

data$pValue = data$plats*data$pOdds
data = subset(data, select=c(-Plats., -plats, -result, -won))
# Factors
#data = factorize_data(data)


# PREDICTION


pred_data = read.csv("../data/2021-03-13-prediction/data.csv", sep=";")
pred_data = factorize_data(pred_data)
model = lm(v75val~., data)
preds = predict(model, newdata=pred_data)
preds[is.na(preds)] = -2.0

pred_data$v75Pred = preds

print_set = subset(pred_data, select = c(raceIdx, horseNumber, vOdds, pOdds, Poäng, v75Pred))
print_set$horseNumber = print_set$horseNumber + 1


# TESTING

n = dim(data)[1]
set.seed(1234)
id = sample(1:n, floor(0.9* n))

train_set = data[id,] 
test_set = data[-id,]





model = lm(pValue~., train_set)

preds = predict(model, newdata=test_set)
preds[is.na(preds)] = -2.0

test_set$pValue = preds

best = test_set[test_set$pValue > 1.0,]
mean(best$pValue)
mean(test_set$pValue)
