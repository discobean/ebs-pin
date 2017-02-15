import requests, json, logging

class Configuration:
    def metadata(self):
        try:
            r = requests.get('http://169.254.169.254/latest/dynamic/instance-identity/document', timeout=1)
            return r.json()
        except requests.exceptions.ConnectionError:
            logging.error("Simulation mode enabled.")
            return {
                  "privateIp" : "10.123.26.236",
                  "devpayProductCodes" : None,
                  "availabilityZone" : "ap-southeast-2a",
                  "version" : "2010-08-31",
                  "region" : "ap-southeast-2",
                  "instanceId" : "i-04ec586a0e91b640c",
                  "instanceType" : "t2.medium",
                  "pendingTime" : "2017-02-13T05:57:33Z",
                  "imageId" : "ami-1aefee79",
                  "architecture" : "x86_64",
                  "kernelId" : None,
                  "ramdiskId" : None
                }
