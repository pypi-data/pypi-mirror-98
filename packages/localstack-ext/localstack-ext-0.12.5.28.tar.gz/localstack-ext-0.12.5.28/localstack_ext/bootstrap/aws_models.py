from localstack.utils.aws import aws_models
VCIQW=super
VCIQe=None
VCIQX=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  VCIQW(LambdaLayer,self).__init__(arn)
  self.cwd=VCIQe
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.VCIQX.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,VCIQX,env=VCIQe):
  VCIQW(RDSDatabase,self).__init__(VCIQX,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,VCIQX,env=VCIQe):
  VCIQW(RDSCluster,self).__init__(VCIQX,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,VCIQX,env=VCIQe):
  VCIQW(AppSyncAPI,self).__init__(VCIQX,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,VCIQX,env=VCIQe):
  VCIQW(AmplifyApp,self).__init__(VCIQX,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,VCIQX,env=VCIQe):
  VCIQW(ElastiCacheCluster,self).__init__(VCIQX,env=env)
class TransferServer(BaseComponent):
 def __init__(self,VCIQX,env=VCIQe):
  VCIQW(TransferServer,self).__init__(VCIQX,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,VCIQX,env=VCIQe):
  VCIQW(CloudFrontDistribution,self).__init__(VCIQX,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,VCIQX,env=VCIQe):
  VCIQW(CodeCommitRepository,self).__init__(VCIQX,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
