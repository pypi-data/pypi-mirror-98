# CDK SSM Document

[![Source](https://img.shields.io/badge/Source-GitHub-blue?logo=github)](https://github.com/udondan/cdk-ssm-document)
[![Test](https://github.com/udondan/cdk-ssm-document/workflows/Test/badge.svg)](https://github.com/udondan/cdk-ssm-document/actions?query=workflow%3ATest)
[![GitHub](https://img.shields.io/github/license/udondan/cdk-ssm-document)](https://github.com/udondan/cdk-ssm-document/blob/master/LICENSE)
[![Docs](https://img.shields.io/badge/awscdk.io-cdk--ssm--document-orange)](https://awscdk.io/packages/cdk-ssm-document@2.1.1)

[![npm package](https://img.shields.io/npm/v/cdk-ssm-document?color=brightgreen)](https://www.npmjs.com/package/cdk-ssm-document)
[![PyPI package](https://img.shields.io/pypi/v/cdk-ssm-document?color=brightgreen)](https://pypi.org/project/cdk-ssm-document/)
[![NuGet package](https://img.shields.io/nuget/v/CDK.SSM.Document?color=brightgreen)](https://www.nuget.org/packages/CDK.SSM.Document/)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
[![npm](https://img.shields.io/npm/dt/cdk-ssm-document?label=npm&color=blueviolet)](https://www.npmjs.com/package/cdk-ssm-document)
[![PyPI](https://img.shields.io/pypi/dm/cdk-ssm-document?label=pypi&color=blueviolet)](https://pypi.org/project/cdk-ssm-document/)
[![NuGet](https://img.shields.io/nuget/dt/CDK.SSM.Document?label=nuget&color=blueviolet)](https://www.nuget.org/packages/CDK.SSM.Document/)

[AWS CDK](https://aws.amazon.com/cdk/) L3 construct for managing SSM Documents.

CloudFormation's support for SSM Documents [currently is lacking updating functionality](https://github.com/aws-cloudformation/aws-cloudformation-coverage-roadmap/issues/339). Instead of updating a document, CFN will replace it. The old document is destroyed and a new one is created with a different name. This is problematic because:

* When names potentially change, you cannot directly reference a document
* Old versions are permanently lost

This construct provides document support in a way you'd expect it:

* Changes on documents will cerate new versions
* Versions cannot be deleted

## Installation

This package has peer dependencies, which need to be installed along in the expected version.

For TypeScript/NodeJS, add these to your `dependencies` in `package.json`:

* cdk-ssm-document
* @aws-cdk/aws-cloudformation
* @aws-cdk/aws-iam
* @aws-cdk/aws-lambda

For Python, add these to your `requirements.txt`:

* cdk-ssm-document
* aws-cdk.aws-cloudformation
* aws-cdk.aws-iam
* aws-cdk.aws-lambda

## Usage

### Creating a document from a YAML or JSON file

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from cdk_ssm_document import Document
import fs as fs
import path as path

class TestStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        file = path.join(__dirname, "../documents/hello-world.yml")
        Document(self, "SSM-Document-HelloWorld",
            name="HelloWorld",
            content=fs.read_file_sync(file).to_string()
        )
```

### Creating a document via inline definition

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from cdk_ssm_document import Document
import fs as fs
import path as path

class TestStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        Document(self, "SSM-Document-HelloWorld",
            name="HelloWorld",
            content={
                "schema_version": "2.2",
                "description": "Echo Hello World!",
                "parameters": {
                    "text": {
                        "default": "Hello World!",
                        "description": "Text to echo",
                        "type": "String"
                    }
                },
                "main_steps": [{
                    "name": "echo",
                    "action": "aws:runShellScript",
                    "inputs": {
                        "run_command": ["echo \"{{text}}\""]
                    },
                    "precondition": {
                        "StringEquals": ["platformType", "Linux"]
                    }
                }
                ]
            }
        )
```

### Deploy all YAML/JSON files from a directory

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from cdk_ssm_document import Document
import fs as fs
import path as path

class TestStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        dir = path.join(__dirname, "../documents")
        files = fs.readdir_sync(dir)for (const i in files) {
              const name = files[i];
              const shortName = name.split('.').slice(0, -1).join('.'); // removes file extension
              const file = `${dir}/${name}`;

              new Document(this, `SSM-Document-${shortName}`, {
                name: shortName,
                content: fs.readFileSync(file).toString(),
              });
            }
```

## Deploying many documents in a single stack

When you want to create multiple documents in the same stack, you will quickly exceed the SSM API rate limit. One ugly but working solution for this is to ensure that only a single document is created/updated at a time by adding resource dependencies. When document C depends on document B and B depends on document A, the documents will be created/updated in that order.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
doc_a = Document(self, "doc-A", ...)
doc_b = Document(self, "doc-B", ...)
doc_c = Document(self, "doc-C", ...)

doc_c.node.add_dependency(doc_b)
doc_b.node.add_dependency(doc_a)
```

When looping through a directory of documents it could look like this:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
last = undefinedfor (const i in files) {
  const doc = new Document(this, `SSM-Document-${shortName}`, {...});
  if (typeof last !== 'undefined') {
    last.node.addDependency(doc);
  }
  last = doc;
}
```

## Using the Lambda as a custom resource in CloudFormation - without CDK

If you're still not convinced to use the [AWS CDK](https://aws.amazon.com/cdk/), you can still use the Lambda as a [custom resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) in your CFN template. Here is how:

1. **Create a zip file for the Lambda:**

   To create a zip from the Lambda source run:

   ```bash
   lambda/build
   ```

   This will generate the file `lambda/code.zip`.
2. **Upload the Lambda function:**

   Upload this zip file to an S3 bucket via cli, Console or however you like.

   Example via cli:

   ```bash
   aws s3 cp lambda/code.zip s3://example-bucket/code.zip
   ```
3. **Deploy a CloudFormation stack utilizing the zip as a custom resource provider:**

   Example CloudFormation template:

   ```yaml
   ---
   AWSTemplateFormatVersion: "2010-09-09"
   Resources:
     SSMDocExecutionRole:
       Type: AWS::IAM::Role
       Properties:
         RoleName: CFN-Resource-Custom-SSM-Document
         AssumeRolePolicyDocument:
           Version: "2012-10-17"
           Statement:
             - Effect: Allow
               Principal:
                 Service: lambda.amazonaws.com
               Action: sts:AssumeRole
         ManagedPolicyArns:
           - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
           - Ref: SSMDocExecutionPolicy

     SSMDocExecutionPolicy:
       Type: AWS::IAM::ManagedPolicy
       Properties:
         ManagedPolicyName: CFN-Resource-Custom-SSM-Document
         PolicyDocument:
           Version: "2012-10-17"
           Statement:
             - Effect: Allow
               Action:
                 - ssm:ListDocuments
                 - ssm:ListTagsForResource
               Resource: "*"
             - Effect: Allow
               Action:
                 - ssm:CreateDocument
                 - ssm:AddTagsToResource
               Resource: "*"
               Condition:
                 StringEquals:
                   aws:RequestTag/CreatedByCfnCustomResource: CFN::Resource::Custom::SSM-Document
             - Effect: Allow
               Action:
                 - ssm:DeleteDocument
                 - ssm:DescribeDocument
                 - ssm:GetDocument
                 - ssm:ListDocumentVersions
                 - ssm:ModifyDocumentPermission
                 - ssm:UpdateDocument
                 - ssm:UpdateDocumentDefaultVersion
                 - ssm:AddTagsToResource
                 - ssm:RemoveTagsFromResource
               Resource: "*"
               Condition:
                 StringEquals:
                   aws:ResourceTag/CreatedByCfnCustomResource: CFN::Resource::Custom::SSM-Document

     SSMDocFunction:
       Type: AWS::Lambda::Function
       Properties:
         FunctionName: CFN-Resource-Custom-SSM-Document-Manager
         Code:
           S3Bucket: example-bucket
           S3Key: code.zip
         Handler: index.handler
         Runtime: nodejs10.x
         Timeout: 3
         Role: !GetAtt SSMDocExecutionRole.Arn

     MyDocument:
       Type: Custom::SSM-Document
       Properties:
         Name: MyDocument
         ServiceToken: !GetAtt SSMDocFunction.Arn
         StackName: !Ref AWS::StackName
         UpdateDefaultVersion: true # default: true
         Content:
           schemaVersion: "2.2"
           description: Echo Hello World!
           parameters:
             text:
               type: String
               description: Text to echo
               default: Hello World!
           mainSteps:
             - name: echo
               action: aws:runShellScript
               inputs:
                 runCommand:
                   - echo "{{text}}"
               precondition:
                 StringEquals:
                   - platformType
                   - Linux
         DocumentType: Command # default: Command
         TargetType: / # default: /
         Tags:
           CreatedByCfnCustomResource: CFN::Resource::Custom::SSM-Document # required, see above policy conditions
   ```
