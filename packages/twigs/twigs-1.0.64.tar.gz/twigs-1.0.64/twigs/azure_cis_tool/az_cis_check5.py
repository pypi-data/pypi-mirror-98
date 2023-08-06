import os
import json
import logging
import sys
from . import az_cis_utils as az_cis_utils

def check50(subid):
    logging.info("Processing 50...")
    chk51=""
    chk52=""
    chk53=('No Alert found for policyAssignments</li>\n')
    chk54=('No Alert found for Create or Update NSG</li>\n')
    chk55=('No Alert found for Delete NSG</li>\n')
    chk56=('No Alert found for Create or Update NSG security rule</li>\n')
    chk57=('No Alert found for Delete NSG security rule</li>\n')
    chk58=('No Alert found for Create or Update Security Solution</li>\n')
    chk59=('No Alert found for Delete Security Solution</li>\n')
    chk510=('No Alert found for Create or Update SQL Server FW rules</li>\n')
    chk511=('No Alert found for Delete SQL Server FW rules</li>\n')
    chk512=('No Alert found for Create or Update Security Policy</li>\n')
    chk513=''

    score51=['<font color="red">Failed</font>',0]
    score52=['<font color="red">Failed</font>',0]
    score53=['<font color="red">Failed</font>',0]
    score54=['<font color="red">Failed</font>',0]
    score55=['<font color="red">Failed</font>',0]
    score56=['<font color="red">Failed</font>',0]
    score57=['<font color="red">Failed</font>',0]
    score58=['<font color="red">Failed</font>',0]
    score59=['<font color="red">Failed</font>',0]
    score510=['<font color="red">Failed</font>',0]
    score511=['<font color="red">Failed</font>',0]
    score512=['<font color="red">Failed</font>',0]
    score513=['<font color="red">Failed</font>',0]
    try:
        query51='az monitor log-profiles list --query [*].[id,name,retentionPolicy.days]'
        json_cis51=az_cis_utils.query_az(query51)
        #iteration through log profiles
        if (len(json_cis51)>0):
            for i in range(len(json_cis51)):
                chk51=chk51+('logprofiles: <b><font color="blue">%s</b></font></li></br>\n' % json_cis51[i][1])
                score51=['<font color="green">Passed</font>',1]
                chk52=chk52+('Retendtion Days <b><font color="blue">%d</b></font> for logprofiles: <b><font color="blue">%s</b></font></li></br>\n' % (json_cis51[i][2],json_cis51[i][1]))
                if (json_cis51[i][2]>=365):
                    score52=['<font color="green">Passed</font>',1]
        else:
            chk51="No Log Profile found</li>\n"
            chk52="No Log Profile found</li>\n"
        query53='az monitor activity-log alert list --query [*].[name,condition.allOf]'
        #query53=('az monitor activity-log alert list --query "[?contains(id,\'%s\')].[name,condition.allOf]"' % subid)
        json_cis53=az_cis_utils.query_az(query53)
        # iteration through Alerts
        for j in range(len(json_cis53)):
            if ("Microsoft.Authorization/policyAssignments/write" in json_cis53[j][1][1]['equals']):
                chk53=('Alert Name:<font color="blue"><b>%s</b></font> set up for policyAssignments</li>\n' % (json_cis53[j][0]))
                score53=['<font color="green">Passed</font>',1]
            elif ("Microsoft.Network/networkSecurityGroups/write" in json_cis53[j][1][1]['equals']):
                chk54=('Alert Name:<font color="blue"><b>%s</b></font> set up for Create or Update NSG</li>\n' % (json_cis53[j][0]))
                score54=['<font color="green">Passed</font>',1]
            elif ("Microsoft.Network/networkSecurityGroups/delete" in json_cis53[j][1][1]['equals']):
                chk55=('Alert Name:<font color="blue"><b>%s</b></font> set up for Delete NSG</li>\n' % (json_cis53[j][0]))
                score55=['<font color="green">Passed</font>',1]
            elif ("Microsoft.Network/networkSecurityGroups/securityRules/write" in json_cis53[j][1][1]['equals']):
                chk56=('Alert Name:<font color="blue"><b>%s</b></font> set up for Create or Update NSG rule</li>\n' % (json_cis53[j][0]))
                score56=['<font color="green">Passed</font>',1]
            elif ("Microsoft.Network/networkSecurityGroups/securityRules/delete" in json_cis53[j][1][1]['equals']):
                chk57=('Alert Name:<font color="blue"><b>%s</b></font> set up for Delete NSG rule</li>\n' % (json_cis53[j][0]))
                score57=['<font color="green">Passed</font>',1]
            elif ("Microsoft.Security/securitySolutions/write" in json_cis53[j][1][1]['equals']):
                chk58=('Alert Name:<font color="blue"><b>%s</b></font> set up for Create or Update Security Solution</li>\n' % (json_cis53[j][0]))
                score58=['<font color="green">Passed</font>',1]
            elif ("Microsoft.Security/securitySolutions/delete" in json_cis53[j][1][1]['equals']):
                chk59=('Alert Name:<font color="blue"><b>%s</b></font> set up for Delete Security Solution</li>\n' % (json_cis53[j][0]))
                score59=['<font color="green">Passed</font>',1]
            elif ("Microsoft.Sql/servers/firewallRules/write" in json_cis53[j][1][1]['equals']):
                chk510=('Alert Name:<font color="blue"><b>%s</b></font> set up for Create or Update SQL Server FW rules</li>\n' % (json_cis53[j][0]))
                score510=['<font color="green">Passed</font>',1]   
            elif ("Microsoft.Sql/servers/firewallRules/delete" in json_cis53[j][1][1]['equals']):
                chk511=('Alert Name:<font color="blue"><b>%s</b></font> set up for Delete SQL Server FW rules</li>\n' % (json_cis53[j][0]))
                score511=['<font color="green">Passed</font>',1]
            elif ("Microsoft.Security/policies/write" in json_cis53[j][1][1]['equals']):
                chk512=('Alert Name:<font color="blue"><b>%s</b></font> set up for Create or Update Security Policy</li>\n' % (json_cis53[j][0]))
                score512=['<font color="green">Passed</font>',1]
        try:
            query513=('az keyvault list --query [*].[name,id]')
            #query513=('az keyvault list --query "[?contains(id,\'%s\')].[name,id]"' % subid)
            json_cis513=az_cis_utils.query_az(query513)
            if (len(json_cis513)>0):
                # iteration through keyvault
                for j in range(len(json_cis513)):
                    query5131=('az monitor diagnostic-settings list --resource %s' % (json_cis513[j][1]))
                    json_cis5131=az_cis_utils.query_az(query5131)
                    if (len(json_cis5131['value'])>0):
                        category = json_cis5131['value'][0]['logs'][0]['category']
                        days = json_cis5131['value'][0]['logs'][0]['retentionPolicy']['days']
                        if ("AuditEvent" in category):
                            chk513=chk513+('Keyvault <b>%s</b> Audit event enabled for <b>%s</b> days' % (json_cis513[j][0],days))
                            if (days>=180):
                                score513=['<font color="green">Passed</font>',1]
                            else:
                                score513=['<font color="red">Failed</font>',0]
                        else:
                            score513=['<font color="red">Failed</font>',0]
                            chk513=chk513+('Keyvault <b>%s</b> Audit event disabled' % (json_cis513[j][0]))
                    else:
                        chk513=chk513+('Diagnostics disable for Keyvault <b>%s</b>' % (json_cis513[j][0]))
                        score513=['<font color="red">Failed</font>',0]
            else:
                chk513="No KeyVault Found"
                score513=['<font color="green">Passed</font>',1]
        except Exception as e:
            logging.error("Exception in check50: %s %s" %(type(e), str(e.args)))
            unkScore=['<font color="orange">UNKNOWN </font>',0]
            chk="Failed query KeyVault"
            return [chk,chk,chk,chk,chk,chk,chk,chk,chk,chk,chk,chk,chk,unkScore,unkScore,unkScore,unkScore,unkScore,unkScore,unkScore,unkScore,unkScore,unkScore,unkScore,unkScore,unkScore]
            #chk513="Failed query KeyVault"
        return [chk51,chk52,chk53,chk54,chk55,chk56,chk57,chk58,chk59,chk510,chk511,chk512,chk513,score51,score52,score53,score54,score55,score56,score57,score58,score59,score510,score511,score512,score513]
    except Exception as e:
        logging.error("Exception in check50: %s %s" %(type(e), str(e.args)))
        unkScore=['<font color="orange">UNKNOWN </font>',0]
        chk="Failed to query log profiles"
        return [chk,chk,chk,chk,chk,chk,chk,chk,chk,chk,chk,chk,chk,unkScore,unkScore,unkScore,unkScore,unkScore,unkScore,unkScore,unkScore,unkScore,unkScore,unkScore,unkScore,unkScore] 
