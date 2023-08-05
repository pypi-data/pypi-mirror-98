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
from aliyunsdkfacebody.endpoint import endpoint_data

class SwapFacialFeaturesRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'facebody', '2019-12-30', 'SwapFacialFeatures','facebody')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_TargetImageURL(self):
		return self.get_body_params().get('TargetImageURL')

	def set_TargetImageURL(self,TargetImageURL):
		self.add_body_params('TargetImageURL', TargetImageURL)

	def get_SourceImageData(self):
		return self.get_body_params().get('SourceImageData')

	def set_SourceImageData(self,SourceImageData):
		self.add_body_params('SourceImageData', SourceImageData)

	def get_SourceImageURL(self):
		return self.get_body_params().get('SourceImageURL')

	def set_SourceImageURL(self,SourceImageURL):
		self.add_body_params('SourceImageURL', SourceImageURL)

	def get_TargetImageData(self):
		return self.get_body_params().get('TargetImageData')

	def set_TargetImageData(self,TargetImageData):
		self.add_body_params('TargetImageData', TargetImageData)

	def get_EditPart(self):
		return self.get_body_params().get('EditPart')

	def set_EditPart(self,EditPart):
		self.add_body_params('EditPart', EditPart)