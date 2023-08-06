#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from aodhclient.tests.functional import base


class CapabilitiesClientTest(base.ClientTestBase):
    def test_capabilities_scenario(self):
        # GET
        result = self.aodh('capabilities', params="list")
        caps = self.parser.listing(result)[0]
        self.assertIsNotNone(caps)
        self.assertEqual('alarm_storage', caps['Field'])
