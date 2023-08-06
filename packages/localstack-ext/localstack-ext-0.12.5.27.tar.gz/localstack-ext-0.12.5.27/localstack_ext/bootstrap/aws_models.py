from localstack.utils.aws import aws_models
iXEYV=super
iXEYD=None
iXEYH=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  iXEYV(LambdaLayer,self).__init__(arn)
  self.cwd=iXEYD
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.iXEYH.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,iXEYH,env=iXEYD):
  iXEYV(RDSDatabase,self).__init__(iXEYH,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,iXEYH,env=iXEYD):
  iXEYV(RDSCluster,self).__init__(iXEYH,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,iXEYH,env=iXEYD):
  iXEYV(AppSyncAPI,self).__init__(iXEYH,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,iXEYH,env=iXEYD):
  iXEYV(AmplifyApp,self).__init__(iXEYH,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,iXEYH,env=iXEYD):
  iXEYV(ElastiCacheCluster,self).__init__(iXEYH,env=env)
class TransferServer(BaseComponent):
 def __init__(self,iXEYH,env=iXEYD):
  iXEYV(TransferServer,self).__init__(iXEYH,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,iXEYH,env=iXEYD):
  iXEYV(CloudFrontDistribution,self).__init__(iXEYH,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,iXEYH,env=iXEYD):
  iXEYV(CodeCommitRepository,self).__init__(iXEYH,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
