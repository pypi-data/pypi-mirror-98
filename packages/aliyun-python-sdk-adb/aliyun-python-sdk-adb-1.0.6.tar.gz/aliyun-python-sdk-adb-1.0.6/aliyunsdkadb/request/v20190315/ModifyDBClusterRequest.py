# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkadb.endpoint import endpoint_data

class ModifyDBClusterRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'adb', '2019-03-15', 'ModifyDBCluster','ads')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_ResourceOwnerId(self):
		return self.get_query_params().get('ResourceOwnerId')

	def set_ResourceOwnerId(self,ResourceOwnerId):
		self.add_query_param('ResourceOwnerId',ResourceOwnerId)

	def get_Mode(self):
		return self.get_query_params().get('Mode')

	def set_Mode(self,Mode):
		self.add_query_param('Mode',Mode)

	def get_StorageResource(self):
		return self.get_query_params().get('StorageResource')

	def set_StorageResource(self,StorageResource):
		self.add_query_param('StorageResource',StorageResource)

	def get_DBNodeClass(self):
		return self.get_query_params().get('DBNodeClass')

	def set_DBNodeClass(self,DBNodeClass):
		self.add_query_param('DBNodeClass',DBNodeClass)

	def get_DBClusterCategory(self):
		return self.get_query_params().get('DBClusterCategory')

	def set_DBClusterCategory(self,DBClusterCategory):
		self.add_query_param('DBClusterCategory',DBClusterCategory)

	def get_ResourceOwnerAccount(self):
		return self.get_query_params().get('ResourceOwnerAccount')

	def set_ResourceOwnerAccount(self,ResourceOwnerAccount):
		self.add_query_param('ResourceOwnerAccount',ResourceOwnerAccount)

	def get_DBClusterId(self):
		return self.get_query_params().get('DBClusterId')

	def set_DBClusterId(self,DBClusterId):
		self.add_query_param('DBClusterId',DBClusterId)

	def get_OwnerAccount(self):
		return self.get_query_params().get('OwnerAccount')

	def set_OwnerAccount(self,OwnerAccount):
		self.add_query_param('OwnerAccount',OwnerAccount)

	def get_OwnerId(self):
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)

	def get_DBNodeGroupCount(self):
		return self.get_query_params().get('DBNodeGroupCount')

	def set_DBNodeGroupCount(self,DBNodeGroupCount):
		self.add_query_param('DBNodeGroupCount',DBNodeGroupCount)

	def get_DBNodeStorage(self):
		return self.get_query_params().get('DBNodeStorage')

	def set_DBNodeStorage(self,DBNodeStorage):
		self.add_query_param('DBNodeStorage',DBNodeStorage)

	def get_ExecutorCount(self):
		return self.get_query_params().get('ExecutorCount')

	def set_ExecutorCount(self,ExecutorCount):
		self.add_query_param('ExecutorCount',ExecutorCount)

	def get_ModifyType(self):
		return self.get_query_params().get('ModifyType')

	def set_ModifyType(self,ModifyType):
		self.add_query_param('ModifyType',ModifyType)

	def get_ComputeResource(self):
		return self.get_query_params().get('ComputeResource')

	def set_ComputeResource(self,ComputeResource):
		self.add_query_param('ComputeResource',ComputeResource)

	def get_ElasticIOResource(self):
		return self.get_query_params().get('ElasticIOResource')

	def set_ElasticIOResource(self,ElasticIOResource):
		self.add_query_param('ElasticIOResource',ElasticIOResource)