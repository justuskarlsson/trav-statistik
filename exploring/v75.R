
data = read.csv("../data/2021-05-15_510/data.csv", sep=";")
data$betDistribution[data$betDistribution == 0.0] = 0.001
data$y = (1/data$betDistribution) * data$won
data = subset(data, select=c(-Plats., -plats, -result, -won, -pValue))


########## PREDICTION ##########


model = lm(y~., data)

pred_data = read.csv("../data/2021-05-22-prediction/data.csv", sep=";")
names = read.csv("../data/2021-05-22-prediction/horseNames.csv", header=F)
preds = predict(model, newdata=pred_data)
preds[is.na(preds)] = -2.0


print_set = data.frame(
  Lopp = pred_data$raceIdx,
  Häst_Nummer = pred_data$horseNumber + 1,
  Namn = names[pred_data$horseName+1,] ,
  Spel_Värde = round(preds, 2),
  Vinnar_Odds = pred_data$vOdds,
  V75_Procent = sapply(pred_data$betDistribution*100, function(x) sprintf("%d%%", round(x)))
)


print_set[,] = print_set[order(preds, decreasing=T) ,]
print_set[,] = print_set[order(print_set$Lopp) ,]


write.csv(print_set, "pred.csv", row.names = F, fileEncoding = "utf-8")


# https://www.convertcsv.com/csv-to-pdf.htm
# font-size

########## TESTING ##########
n = dim(data)[1]
set.seed(123456)
id = sample(1:n, floor(0.9* n))

train_set = data[id,]
test_set = data[-id,]





model = lm(y~., train_set)

preds = predict(model, newdata=test_set)
preds[is.na(preds)] = -2.0

test_set$y_hat = preds


best = test_set[test_set$y_hat > 1.0,]
mean(best$y)
mean(test_set$y)
'