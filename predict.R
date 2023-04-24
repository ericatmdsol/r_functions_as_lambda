library(jsonlite)
library(logger)
library(h2o)
# download model file from S3 into /tmp folder

h2o.init()

handler <- function(body) {
  parsed_payload = jsonlite::fromJSON(body)

  
  df = read.csv('test.csv')
  saved_model = h2o.import_mojo('GLM_model_R_1682363743951_1.zip')
  output = predict(saved_model, as.h2o(df))
  output = as.data.frame(output)
  return(
    list(
      statusCode = 200,
      headers = list("Content-Type" = "application/json"),
      body = toJSON(list(echo_data = output))
    )
  )
}