library(jsonlite)
library(logger)

# download model file from S3 into /tmp folder

handler <- function(body) {
  parsed_payload = jsonlite::fromJSON(body)
  return(
    list(
      statusCode = 200,
      headers = list("Content-Type" = "application/json"),
      body = toJSON(list(echo_data = parsed_payload))
    )
  )
}