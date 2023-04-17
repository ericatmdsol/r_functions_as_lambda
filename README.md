# Basic code to deploy an R Image to a lambda function

We might in the future want to deploy our R code as a lambda function. This might allow us to skip the use of sagemaker for deployments which should be cheaper and easier. This repo also uses hydra to maintain configurations

# Pre-requistes

1. You must install aws-okta-keyman in order to get the credentials to do anything on our system
2. Update your conda env: ```conda env create -f env.yml```

# Primary components:

runtime.R this is the basic file that allows us to call a handler that's written in predict.R. Note the predict.R file name isn't important, and that is specified in the Dockerfile as the following line, ```CMD [ "predict.handler" ]``` where the .R extension is changed to ```.handler```. If you want to write your own just steal every file but the predict.R file and alter it to your needs

To deploy the container, update the config.yaml file to what is appropriate for your setting. Most of it should be self-explanatory

```
docker_img: test_r_lambda:latest                                 # local name of your docker container (this should change)
lambda_name: test_r_lambda                                       # name of your lambda function        (as should this)
ecr_address: 833923177614.dkr.ecr.us-east-1.amazonaws.com        # the ECR that DSE has access to. Shouldn't change for you. Deployment by engineering might change this
role: arn:aws:iam::833923177614:role/acorn-dse-lambda            # The role that the lambda function has. Shouldn't change for you
memory: 1536
```

# Deployment

Once you're ready to deploy, update your config.yaml file, login through okta-keyman and you should be able to run deploy.py to get your lambda function onto AWS

If you want to test it. run the test.py function (i didn't change the parameters so it's left as an exercise to the reader how to adjust for this)