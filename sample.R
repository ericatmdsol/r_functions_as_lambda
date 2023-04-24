library(h2o)

h2o.init()
df = read.csv('test.csv')
saved_model = h2o.import_mojo('./GLM_model_R_1682363743951_1.zip')
saved_model.predict(as.h2o(df))