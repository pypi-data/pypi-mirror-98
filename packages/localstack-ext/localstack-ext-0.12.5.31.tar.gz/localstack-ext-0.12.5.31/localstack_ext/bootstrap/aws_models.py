from localstack.utils.aws import aws_models
cNwhR=super
cNwhq=None
cNwhB=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  cNwhR(LambdaLayer,self).__init__(arn)
  self.cwd=cNwhq
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.cNwhB.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,cNwhB,env=cNwhq):
  cNwhR(RDSDatabase,self).__init__(cNwhB,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,cNwhB,env=cNwhq):
  cNwhR(RDSCluster,self).__init__(cNwhB,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,cNwhB,env=cNwhq):
  cNwhR(AppSyncAPI,self).__init__(cNwhB,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,cNwhB,env=cNwhq):
  cNwhR(AmplifyApp,self).__init__(cNwhB,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,cNwhB,env=cNwhq):
  cNwhR(ElastiCacheCluster,self).__init__(cNwhB,env=env)
class TransferServer(BaseComponent):
 def __init__(self,cNwhB,env=cNwhq):
  cNwhR(TransferServer,self).__init__(cNwhB,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,cNwhB,env=cNwhq):
  cNwhR(CloudFrontDistribution,self).__init__(cNwhB,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,cNwhB,env=cNwhq):
  cNwhR(CodeCommitRepository,self).__init__(cNwhB,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
