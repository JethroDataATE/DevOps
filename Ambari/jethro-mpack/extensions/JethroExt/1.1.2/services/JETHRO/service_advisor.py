import os
import imp
import traceback
import re
from resource_management.core.logger import Logger

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STACKS_DIR = os.path.join(SCRIPT_DIR, '../../../../../stacks')
PARENT_FILE = os.path.abspath(os.path.join(STACKS_DIR, 'service_advisor.py'))

try:
    with open(PARENT_FILE, 'rb') as fp:
        service_advisor = imp.load_module(
            'service_advisor', fp, PARENT_FILE, ('.py', 'rb', imp.PY_SOURCE))
except Exception as e:
    traceback.print_exc()
    print("Failed to load parent")


class JethroExt112JETHROServiceAdvisor(service_advisor.ServiceAdvisor):

    def colocateService(self, hostsComponentsMap, serviceComponents):
        try:
            # colocate JM with NAMENODE , if no hosts have been allocated for JM
            jm = [component for component in serviceComponents if component["StackServiceComponents"]
                ["component_name"] == "JETHRO_MNG"][0]
            jethroMngAdded = False
            if not self.isComponentHostsPopulated(jm):
                for hostName in hostsComponentsMap.keys():
                    hostComponents = hostsComponentsMap[hostName]
                    if {"name": "NAMENODE"} in hostComponents: 
                        if {"name": "JETHRO_MNG"} not in hostComponents & not jethroMngAdded:
                            hostsComponentsMap[hostName].append({"name": "JETHRO_MNG"})
                            jethroMngAdded = True
                        else:
                             hostsComponentsMap[hostName].remove({"name": "JETHRO_MNG"})
                    if ({"name": "NAMENODE"} not in hostComponents) \
                            and {"name": "JETHRO_MNG"} in hostComponents:
                        hostsComponentsMap[hostName].remove({"name": "JETHRO_MNG"})

            # # colocate JC with NAMENODE , if hosts have been allocated for Jethro maint
            # jc = [component for component in serviceComponents if component["StackServiceComponents"]
            #     ["component_name"] == "JETHRO_MAINT"][0]
            # if not self.isComponentHostsPopulated(jc):
            #     for hostName in hostsComponentsMap.keys():
            #         hostComponents = hostsComponentsMap[hostName]
            #         if ({"name": "NAMENODE"} in hostComponents) \
            #                 and {"name": "JETHRO_MAINT"} in hostComponents:
            #             Logger.info(
            #                 'Removing JETHRO_MAINT from host: ' + hostName)
            #             hostsComponentsMap[hostName].remove(
            #                 {"name": "JETHRO_MAINT"})


            # # colocate JC with NAMENODE , if hosts have been allocated for Jethro server
            # jc = [component for component in serviceComponents if component["StackServiceComponents"]
            #     ["component_name"] == "JETHRO_SERVER"][0]
            # if not self.isComponentHostsPopulated(jc):
            #     for hostName in hostsComponentsMap.keys():
            #         hostComponents = hostsComponentsMap[hostName]
            #         if ({"name": "NAMENODE"} in hostComponents) \
            #                 and {"name": "JETHRO_SERVER"} in hostComponents:
            #             Logger.info(
            #                 'Removing JETHRO_SERVER from host: ' + hostName)
            #             hostsComponentsMap[hostName].remove(
            #                 {"name": "JETHRO_SERVER"})

            # # colocate JC with NAMENODE , if hosts have been allocated for Jethro load schedular
            # jc = [component for component in serviceComponents if component["StackServiceComponents"]
            #     ["component_name"] == "JETHRO_LOAD_SCHEDULER"][0]
            # if not self.isComponentHostsPopulated(jc):
            #     for hostName in hostsComponentsMap.keys():
            #         hostComponents = hostsComponentsMap[hostName]
            #         if ({"name": "NAMENODE"} in hostComponents) \
            #                 and {"name": "JETHRO_LOAD_SCHEDULER"} in hostComponents:
            #             Logger.info(
            #                 'Removing JETHRO_LOAD_SCHEDULER from host: ' + hostName)
            #             hostsComponentsMap[hostName].remove(
            #                 {"name": "JETHRO_LOAD_SCHEDULER"})

            # # colocate JC with NAMENODE , if hosts have been allocated for Jethro Monitor
            # jc = [component for component in serviceComponents if component["StackServiceComponents"]
            #     ["component_name"] == "JETHRO_MONITOR"][0]
            # if not self.isComponentHostsPopulated(jc):
            #     for hostName in hostsComponentsMap.keys():
            #         hostComponents = hostsComponentsMap[hostName]
            #         if ({"name": "NAMENODE"} in hostComponents) \
            #                 and {"name": "JETHRO_MONITOR"} in hostComponents:
            #             Logger.info(
            #                 'Removing JETHRO_MONITOR from host: ' + hostName)
            #             hostsComponentsMap[hostName].remove(
            #                 {"name": "JETHRO_MONITOR"})
        except Exception as e:
            Logger.error("Failed to set Jethro recommended deployment: {0}".format(str(e)))

    def getServiceConfigurationRecommendations(self, configurations, clusterSummary, services, hosts):
        pass

    def getServiceComponentLayoutValidations(self, services, hosts):
        componentsListList = [service["components"]
                              for service in services["services"]]
        componentsList = [item["StackServiceComponents"]
                          for sublist in componentsListList for item in sublist]

        jmHosts = self.getHosts(componentsList, "JETHRO_MNG")
        expectedJmHosts = set(self.getHosts(componentsList, "NAMENODE"))
        items = []

        # Generate WARNING if any JM is not colocated with NAMENODE
        mismatchHosts = sorted(
            expectedJmHosts.symmetric_difference(set(jmHosts)))
        if len(mismatchHosts) > 0:
            hostsString = ', '.join(mismatchHosts)
            message = "Jethro Manager must be installed on the NameNode. " \
                      "The following {0} host(s) do not satisfy the colocation recommendation: {1}".format(
                          len(mismatchHosts), hostsString)
            items.append({"type": 'host-component', "level": 'ERR',
                          "message": message, "component-name": 'JETHRO_MNG'})

        return items

    def getServiceConfigurationsValidationItems(self, configurations, recommendedDefaults, services, hosts):
        return []
