from localstack.utils.aws import aws_models
rTOvL=super
rTOvy=None
rTOvJ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  rTOvL(LambdaLayer,self).__init__(arn)
  self.cwd=rTOvy
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.rTOvJ.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,rTOvJ,env=rTOvy):
  rTOvL(RDSDatabase,self).__init__(rTOvJ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,rTOvJ,env=rTOvy):
  rTOvL(RDSCluster,self).__init__(rTOvJ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,rTOvJ,env=rTOvy):
  rTOvL(AppSyncAPI,self).__init__(rTOvJ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,rTOvJ,env=rTOvy):
  rTOvL(AmplifyApp,self).__init__(rTOvJ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,rTOvJ,env=rTOvy):
  rTOvL(ElastiCacheCluster,self).__init__(rTOvJ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,rTOvJ,env=rTOvy):
  rTOvL(TransferServer,self).__init__(rTOvJ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,rTOvJ,env=rTOvy):
  rTOvL(CloudFrontDistribution,self).__init__(rTOvJ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,rTOvJ,env=rTOvy):
  rTOvL(CodeCommitRepository,self).__init__(rTOvJ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
