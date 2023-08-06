# cdk-lambda-bash

Deploy Lambda container image with Bash script support in AWS CDK

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app = cdk.App()

stack = cdk.Stack(app, "my-stack")

# bundle your Lambda function to execute the local demo.sh in container
fn = BashExecFunction(stack, "Demo",
    script=path.join(__dirname, "../demo.sh")
)

# run it as custom resource on deployment
fn.run()
```
