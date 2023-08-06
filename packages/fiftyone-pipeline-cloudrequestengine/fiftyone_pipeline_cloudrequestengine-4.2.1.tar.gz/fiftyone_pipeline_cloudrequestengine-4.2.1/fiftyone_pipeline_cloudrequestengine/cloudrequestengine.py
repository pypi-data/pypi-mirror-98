 # *********************************************************************
 # This Original Work is copyright of 51 Degrees Mobile Experts Limited.
 # Copyright 2019 51 Degrees Mobile Experts Limited, 5 Charlotte Close,
 # Caversham, Reading, Berkshire, United Kingdom RG4 7BY.
 #
 # This Original Work is licensed under the European Union Public Licence (EUPL) 
 # v.1.2 and is subject to its terms as set out below.
 #
 # If a copy of the EUPL was not distributed with this file, You can obtain
 # one at https://opensource.org/licenses/EUPL-1.2.
 #
 # The 'Compatible Licences' set out in the Appendix to the EUPL (as may be
 # amended by the European Commission) shall be deemed incompatible for
 # the purposes of the Work and the provisions of the compatibility
 # clause in Article 5 of the EUPL shall not apply.
 # 
 # If using the Work as, or as part of, a network application, by 
 # including the attribution notice(s) required under Article 5 of the EUPL
 # in the end user terms of the application under an appropriate heading, 
 # such notice(s) shall fulfill the requirements of that article.
 # ********************************************************************

from __future__ import absolute_import
from fiftyone_pipeline_core.basiclist_evidence_keyfilter import BasicListEvidenceKeyFilter
from fiftyone_pipeline_engines.engine import Engine
from fiftyone_pipeline_engines.aspectdata_dictionary import AspectDataDictionary
from .requestclient import RequestClient
from .constants import Constants

import json
import requests
import os

try:
    #python2
    from urllib import urlencode
except ImportError:
    #python3
    from urllib.parse import urlencode

# Engine that makes a call to the 51Degrees cloud service
# Returns raw JSON as a "cloud" property under "cloud" datakey

class CloudRequestEngine(Engine):

    def __init__(self, settings = {}):

        """!
        Constructor for CloudRequestEngine
        
        @type settings: dict
        @param settings: Settings should contain a resource_key and optionally a cloud_endpoint to overwrite the default baseurl

        """

        super(CloudRequestEngine, self).__init__()

        self.datakey = "cloud"

        self.properties = {
            "cloud" : {
                "type": "string",
                "description": "raw JSON from the cloud service"
            }
        }

        if not "resource_key" in settings:
            raise Exception("CloudRequestEngine needs a resource key")
        else: 
            self.resource_key = settings["resource_key"]
        
        
        if "cloud_endpoint" in settings:
            self.baseURL = settings["cloud_endpoint"]
        else:
            self.baseURL = os.environ.get(Constants.FOD_CLOUD_API_URL)
            if self.baseURL is None or (self.baseURL is not None and self.baseURL == ""):
                self.baseURL = Constants.BASE_URL_DEFAULT

        # Make sure if baseURL does not end with '/', one will be appended
        if not self.baseURL.endswith("/"):
            self.baseURL = self.baseURL + "/"
  
        if "http_client" in settings:
            self.http_client = settings["http_client"]
        else:
            self.http_client = RequestClient()

        # Initialise evidencekeys and properties from the cloud service
     
        self.flow_element_properties = self.get_engine_properties()

        self.evidence_keys = self.get_evidence_keys()

        self.exclude_from_messages = True

    def get_evidence_keys(self):

        """!
        Internal function for getting evidence keys used by cloud engines
        @rtype: dict
        @return: Returns list of keys
        """
    
        evidenceKeyRequest = self.make_cloud_request(self.baseURL + "evidencekeys")

        evidenceKeys = json.loads(evidenceKeyRequest)

        return evidenceKeys


    def get_evidence_key_filter(self):

        """!
        Instance of EvidenceKeyFilter based on the evidence keys fetched
        from the cloud service by the private getEvidenceKeys() method
        
        @type: BasicListEvidenceKeyFilter
        @return: Returns BasicListEvidenceKeyFilter

        """

        return BasicListEvidenceKeyFilter(self.evidence_keys)


    def get_engine_properties(self):

        """!
        Internal method to get properties for cloud engines from the cloud service
    
        @rtype: dict
        @return: Returns properties for all engines
        """

        # Get properties for all engines

        propertiesURL = self.baseURL +"accessibleProperties?" + "resource=" + self.resource_key

        properties = self.make_cloud_request(propertiesURL)

        properties = json.loads(properties)

        flowElementProperties = {}

        # Change indexes to be by name
        for datakey, elementProperties in properties["Products"].items():

            flowElementProperties[datakey] = {}

            engine_properties = elementProperties["Properties"]

            for engineProperty in engine_properties:

                # Lowercase keys

                engineProperty =  {k.lower(): v for k, v in engineProperty.items()}

                flowElementProperties[datakey][engineProperty["name"]] = engineProperty
               
        return flowElementProperties
    
    def make_cloud_request(self, url):

        """!    
        @type url: string
        @param url
        
        @rtype: dict
        @return Returns dict with data and error properties error contains any errors from the request, data contains the response
        """

        cloudResponse = self.http_client.request('GET', url)

        if cloudResponse.status_code < 400:
            return cloudResponse.text
        else:
            try:
                jsonResponse = json.loads(cloudResponse.content)
                if("errors" in jsonResponse and len(jsonResponse["errors"])):
                    raise Exception("Cloud request returned an error " + json.dumps(jsonResponse["errors"]))
            except:
                raise Exception("Cloud request engine properties list request returned " + str(cloudResponse.status_code))
            

    def process_internal(self, flowdata):

        """!
        Processing function for the CloudRequestEngine
        Makes a request to the cloud service with the supplied resource key
        and evidence and returns a JSON object that is then parsed by cloud engines
        placed later in the pipeline
        
        @type FlowData: FlowData
        @param FlowData: Returns a JSON object that is then parsed by cloud engines

        """
   
        url = self.baseURL + self.resource_key + ".json?"

        evidence = flowdata.evidence.get_all()

        # Remove prefix from evidence

        evidenceWithoutPrefix = {}

        for key, value in evidence.items():
        
            keySplit =  key.split('.')

            try:
                keySplit[1]
            except:
                continue
            else:
                evidenceWithoutPrefix[keySplit[1]] = value


        url += urlencode(evidenceWithoutPrefix)

        result = self.make_cloud_request(url)

        data = AspectDataDictionary(self, {"cloud" : result})

        flowdata.set_element_data(data)

        return
