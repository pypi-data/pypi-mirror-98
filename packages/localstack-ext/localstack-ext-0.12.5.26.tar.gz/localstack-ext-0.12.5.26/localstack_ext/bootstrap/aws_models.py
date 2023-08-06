from localstack.utils.aws import aws_models
IYUef=super
IYUeM=None
IYUeA=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  IYUef(LambdaLayer,self).__init__(arn)
  self.cwd=IYUeM
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.IYUeA.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,IYUeA,env=IYUeM):
  IYUef(RDSDatabase,self).__init__(IYUeA,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,IYUeA,env=IYUeM):
  IYUef(RDSCluster,self).__init__(IYUeA,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,IYUeA,env=IYUeM):
  IYUef(AppSyncAPI,self).__init__(IYUeA,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,IYUeA,env=IYUeM):
  IYUef(AmplifyApp,self).__init__(IYUeA,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,IYUeA,env=IYUeM):
  IYUef(ElastiCacheCluster,self).__init__(IYUeA,env=env)
class TransferServer(BaseComponent):
 def __init__(self,IYUeA,env=IYUeM):
  IYUef(TransferServer,self).__init__(IYUeA,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,IYUeA,env=IYUeM):
  IYUef(CloudFrontDistribution,self).__init__(IYUeA,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,IYUeA,env=IYUeM):
  IYUef(CodeCommitRepository,self).__init__(IYUeA,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
