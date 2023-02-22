import boto3

# create a SageMaker client
sagemaker = boto3.client('sagemaker')

# create an IAM role to access your S3 bucket
iam = boto3.client('iam')
role_name = 'SageMaker-Execution-Role'
policy_document = {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::your-bucket-name",
        "arn:aws:s3:::your-bucket-name/*"
      ]
    }
  ]
}
iam.create_role(
  RoleName=role_name,
  AssumeRolePolicyDocument='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"sagemaker.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
)
iam.put_role_policy(
  RoleName=role_name,
  PolicyName='sagemaker-access-policy',
  PolicyDocument=json.dumps(policy_document)
)

# create a SageMaker notebook instance
notebook_name = 'My-Notebook-Instance'
instance_type = 'ml.t2.medium'
role_arn = iam.get_role(RoleName=role_name)['Role']['Arn']
response = sagemaker.create_notebook_instance(
  NotebookInstanceName=notebook_name,
  InstanceType=instance_type,
  RoleArn=role_arn,
  VolumeSizeInGB=5,
  DefaultCodeRepository='https://github.com/aws/amazon-sagemaker-examples',
  LifecycleConfigName='lifecycle-configuration-name'
)
