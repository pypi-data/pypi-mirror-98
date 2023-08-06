from localstack.utils.aws import aws_models
COHuo=super
COHuW=None
COHuX=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  COHuo(LambdaLayer,self).__init__(arn)
  self.cwd=COHuW
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.COHuX.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,COHuX,env=COHuW):
  COHuo(RDSDatabase,self).__init__(COHuX,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,COHuX,env=COHuW):
  COHuo(RDSCluster,self).__init__(COHuX,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,COHuX,env=COHuW):
  COHuo(AppSyncAPI,self).__init__(COHuX,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,COHuX,env=COHuW):
  COHuo(AmplifyApp,self).__init__(COHuX,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,COHuX,env=COHuW):
  COHuo(ElastiCacheCluster,self).__init__(COHuX,env=env)
class TransferServer(BaseComponent):
 def __init__(self,COHuX,env=COHuW):
  COHuo(TransferServer,self).__init__(COHuX,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,COHuX,env=COHuW):
  COHuo(CloudFrontDistribution,self).__init__(COHuX,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,COHuX,env=COHuW):
  COHuo(CodeCommitRepository,self).__init__(COHuX,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
