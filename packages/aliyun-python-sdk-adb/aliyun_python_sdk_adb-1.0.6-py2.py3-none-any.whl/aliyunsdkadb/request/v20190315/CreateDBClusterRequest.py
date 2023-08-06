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

class CreateDBClusterRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'adb', '2019-03-15', 'CreateDBCluster','ads')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_ResourceOwnerId(self):
		return self.get_query_params().get('ResourceOwnerId')

	def set_ResourceOwnerId(self,ResourceOwnerId):
		self.add_query_param('ResourceOwnerId',ResourceOwnerId)

	def get_DBClusterDescription(self):
		return self.get_query_params().get('DBClusterDescription')

	def set_DBClusterDescription(self,DBClusterDescription):
		self.add_query_param('DBClusterDescription',DBClusterDescription)

	def get_StorageType(self):
		return self.get_query_params().get('StorageType')

	def set_StorageType(self,StorageType):
		self.add_query_param('StorageType',StorageType)

	def get_Mode(self):
		return self.get_query_params().get('Mode')

	def set_Mode(self,Mode):
		self.add_query_param('Mode',Mode)

	def get_ResourceGroupId(self):
		return self.get_query_params().get('ResourceGroupId')

	def set_ResourceGroupId(self,ResourceGroupId):
		self.add_query_param('ResourceGroupId',ResourceGroupId)

	def get_Period(self):
		return self.get_query_params().get('Period')

	def set_Period(self,Period):
		self.add_query_param('Period',Period)

	def get_BackupSetID(self):
		return self.get_query_params().get('BackupSetID')

	def set_BackupSetID(self,BackupSetID):
		self.add_query_param('BackupSetID',BackupSetID)

	def get_OwnerId(self):
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)

	def get_DBNodeGroupCount(self):
		return self.get_query_params().get('DBNodeGroupCount')

	def set_DBNodeGroupCount(self,DBNodeGroupCount):
		self.add_query_param('DBNodeGroupCount',DBNodeGroupCount)

	def get_VSwitchId(self):
		return self.get_query_params().get('VSwitchId')

	def set_VSwitchId(self,VSwitchId):
		self.add_query_param('VSwitchId',VSwitchId)

	def get_ZoneId(self):
		return self.get_query_params().get('ZoneId')

	def set_ZoneId(self,ZoneId):
		self.add_query_param('ZoneId',ZoneId)

	def get_ComputeResource(self):
		return self.get_query_params().get('ComputeResource')

	def set_ComputeResource(self,ComputeResource):
		self.add_query_param('ComputeResource',ComputeResource)

	def get_SourceDBInstanceName(self):
		return self.get_query_params().get('SourceDBInstanceName')

	def set_SourceDBInstanceName(self,SourceDBInstanceName):
		self.add_query_param('SourceDBInstanceName',SourceDBInstanceName)

	def get_ClientToken(self):
		return self.get_query_params().get('ClientToken')

	def set_ClientToken(self,ClientToken):
		self.add_query_param('ClientToken',ClientToken)

	def get_StorageResource(self):
		return self.get_query_params().get('StorageResource')

	def set_StorageResource(self,StorageResource):
		self.add_query_param('StorageResource',StorageResource)

	def get_DBClusterCategory(self):
		return self.get_query_params().get('DBClusterCategory')

	def set_DBClusterCategory(self,DBClusterCategory):
		self.add_query_param('DBClusterCategory',DBClusterCategory)

	def get_DBClusterNetworkType(self):
		return self.get_query_params().get('DBClusterNetworkType')

	def set_DBClusterNetworkType(self,DBClusterNetworkType):
		self.add_query_param('DBClusterNetworkType',DBClusterNetworkType)

	def get_RestoreTime(self):
		return self.get_query_params().get('RestoreTime')

	def set_RestoreTime(self,RestoreTime):
		self.add_query_param('RestoreTime',RestoreTime)

	def get_ResourceOwnerAccount(self):
		return self.get_query_params().get('ResourceOwnerAccount')

	def set_ResourceOwnerAccount(self,ResourceOwnerAccount):
		self.add_query_param('ResourceOwnerAccount',ResourceOwnerAccount)

	def get_OwnerAccount(self):
		return self.get_query_params().get('OwnerAccount')

	def set_OwnerAccount(self,OwnerAccount):
		self.add_query_param('OwnerAccount',OwnerAccount)

	def get_DBClusterVersion(self):
		return self.get_query_params().get('DBClusterVersion')

	def set_DBClusterVersion(self,DBClusterVersion):
		self.add_query_param('DBClusterVersion',DBClusterVersion)

	def get_DBClusterClass(self):
		return self.get_query_params().get('DBClusterClass')

	def set_DBClusterClass(self,DBClusterClass):
		self.add_query_param('DBClusterClass',DBClusterClass)

	def get_UsedTime(self):
		return self.get_query_params().get('UsedTime')

	def set_UsedTime(self,UsedTime):
		self.add_query_param('UsedTime',UsedTime)

	def get_RestoreType(self):
		return self.get_query_params().get('RestoreType')

	def set_RestoreType(self,RestoreType):
		self.add_query_param('RestoreType',RestoreType)

	def get_DBNodeStorage(self):
		return self.get_query_params().get('DBNodeStorage')

	def set_DBNodeStorage(self,DBNodeStorage):
		self.add_query_param('DBNodeStorage',DBNodeStorage)

	def get_ExecutorCount(self):
		return self.get_query_params().get('ExecutorCount')

	def set_ExecutorCount(self,ExecutorCount):
		self.add_query_param('ExecutorCount',ExecutorCount)

	def get_VPCId(self):
		return self.get_query_params().get('VPCId')

	def set_VPCId(self,VPCId):
		self.add_query_param('VPCId',VPCId)

	def get_PayType(self):
		return self.get_query_params().get('PayType')

	def set_PayType(self,PayType):
		self.add_query_param('PayType',PayType)