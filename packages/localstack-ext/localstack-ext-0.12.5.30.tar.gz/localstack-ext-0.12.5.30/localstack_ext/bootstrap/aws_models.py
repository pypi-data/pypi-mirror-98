from localstack.utils.aws import aws_models
RJLfM=super
RJLfV=None
RJLfQ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  RJLfM(LambdaLayer,self).__init__(arn)
  self.cwd=RJLfV
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.RJLfQ.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,RJLfQ,env=RJLfV):
  RJLfM(RDSDatabase,self).__init__(RJLfQ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,RJLfQ,env=RJLfV):
  RJLfM(RDSCluster,self).__init__(RJLfQ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,RJLfQ,env=RJLfV):
  RJLfM(AppSyncAPI,self).__init__(RJLfQ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,RJLfQ,env=RJLfV):
  RJLfM(AmplifyApp,self).__init__(RJLfQ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,RJLfQ,env=RJLfV):
  RJLfM(ElastiCacheCluster,self).__init__(RJLfQ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,RJLfQ,env=RJLfV):
  RJLfM(TransferServer,self).__init__(RJLfQ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,RJLfQ,env=RJLfV):
  RJLfM(CloudFrontDistribution,self).__init__(RJLfQ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,RJLfQ,env=RJLfV):
  RJLfM(CodeCommitRepository,self).__init__(RJLfQ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
