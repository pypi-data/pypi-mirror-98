import os
import json
import logging
import sys
from . import az_cis_utils as az_cis_utils

def check62(subid):
    logging.info("Processing 61 and 62...")
    acl61=""
    acl62=""
    failvalue61 = 0
    passvalue61 = 0
    totalvalue61 = 0
    nsgfailvalue61 = 0
    score61=""
    passed61='<font color="green">Passed </font>'
    failvalue62 = 0
    passvalue62 = 0
    totalvalue62 = 0
    nsgfailvalue62 = 0
    score62=""
    passed62='<font color="green">Passed </font>'
    rangestart=1
    rangeend=65535
    rangestarts=1
    rangeends=65535
    try:
        query62='az network nsg list --query [*].[name,securityRules,id,resourceGroup]'
        #query62=('az network nsg list --query "[?contains(id,\'%s\')].[name,securityRules]"' % subid)
        json_cis=az_cis_utils.query_az(query62)
        #i iteration number of NSG
        if (len(json_cis)>0):
            for i in range(len(json_cis)):
                nsgid=str(json_cis[i][2])
                nsgrd=str(json_cis[i][3])
                # Find NSG with public IP @
                query621=('az network nic list -g %s --query "[?networkSecurityGroup.id==\'%s\'].ipConfigurations[0].publicIpAddress"'  % (nsgrd,nsgid))
                json_cis2=az_cis_utils.query_az(query621)
                #Check if public IP address is not empty
                if (len(json_cis2)>0):
                    #j iteration of ACL per NSG
                    if (len(json_cis[i][1])>0):
                        for j in range(len(json_cis[i][1])):
                            protocol=str(json_cis[i][1][j]['protocol'])
                            dport=str(json_cis[i][1][j]['destinationPortRange'])
                            dports=json_cis[i][1][j]['destinationPortRanges']
                            action=str(json_cis[i][1][j]['access'])
                            src=str(json_cis[i][1][j]['sourceAddressPrefix'])
                            direction=str(json_cis[i][1][j]['direction'])
                            # Combination of ranges or single port
                            # Split in case a single range is used
                            if (dport!="None" and dport!="*"):
                                rangedport=dport.split('-')
                                rangestart=int(rangedport[0])
                                # Check if single range configured
                                if (len(rangedport)>1):
                                    rangeend=int(rangedport[1])
                                    ## Check For Inbound RDP Access
                                    ## Available Protocol TCP, UDP or * or Internet (Service Tag)
                                    if (protocol!="UDP" and (rangestart<=3389<=rangeend) and action=="Allow" and (src=="*" or src=="Internet") and direction=="Inbound"):
                                        acl61=acl61+('Inbound RDP Allowed on nsg <b>%s</b><br>\n' % (str(json_cis[i][0])))
                                        passed61='<font color="red">Failed </font>'
                                        failvalue61=1
                                    ## Check For Inbound SSH Access.
                                    if (protocol !="UDP" and (rangestart<=22<=rangeend) and action=="Allow" and (src=="*" or src=="Internet") and direction=="Inbound"):
                                        acl62=acl62+('Inbound SSH Allowed on nsg <b>%s</b><br>\n' % (str(json_cis[i][0])))
                                        passed62='<font color="red">Failed </font>'
                                        failvalue62=1
                                else:
                                    if (protocol!="UDP" and (rangestart==3389) and action=="Allow" and (src=="*" or src=="Internet") and direction=="Inbound"):
                                        acl61=acl61+('Inbound RDP Allowed on nsg <b>%s</b><br>\n' % (str(json_cis[i][0])))
                                        passed61='<font color="red">Failed </font>'
                                        failvalue61=1
                                    ## Check For Inbound SSH Access.
                                    if (protocol !="UDP" and (rangestart==22) and action=="Allow" and (src=="*" or src=="Internet") and direction=="Inbound"):
                                        acl62=acl62+('Inbound SSH Allowed on nsg <b>%s</b><br>\n' % (str(json_cis[i][0])))
                                        passed62='<font color="red">Failed </font>'
                                        failvalue62=1

                            # Combination of ranges and single port
                            if (len(dports)>0):    
                                for k in range(len(dports)):
                                    rangedports=dports[k].split('-')
                                    rangestarts=int(rangedports[0])             
                                    if (len(rangedports)>1):
                                        rangeends=int(rangedports[1])
                                        ## Check For Inbound RDP Access
                                        ## Available Protocol TCP, UDP or * or Internet (Service Tag)
                                        if (protocol!="UDP" and (rangestarts<=3389<=rangeends) and action=="Allow" and (src=="*" or src=="Internet") and direction=="Inbound"):
                                            acl61=acl61+('Inbound RDP Allowed on nsg <b>%s</b><br>\n' % (str(json_cis[i][0])))
                                            passed61='<font color="red">Failed </font>'
                                            failvalue61=1
                                        ## Check For Inbound SSH Access.
                                        if (protocol !="UDP" and (rangestarts<=22<=rangeends) and action=="Allow" and (src=="*" or src=="Internet") and direction=="Inbound"):
                                            acl62=acl62+('Inbound SSH Allowed on nsg <b>%s</b><br>\n' % (str(json_cis[i][0])))
                                            passed62='<font color="red">Failed </font>'
                                            failvalue62=1
                                    else:
                                        if (protocol!="UDP" and (rangestarts==3389) and action=="Allow" and (src=="*" or src=="Internet") and direction=="Inbound"):
                                            acl61=acl61+('Inbound RDP Allowed on nsg <b>%s</b><br>\n' % (str(json_cis[i][0])))
                                            passed61='<font color="red">Failed </font>'
                                            failvalue61=1
                                        ## Check For Inbound SSH Access.
                                        if (protocol !="UDP" and (rangestarts==22) and action=="Allow" and (src=="*" or src=="Internet") and direction=="Inbound"):
                                            acl62=acl62+('Inbound SSH Allowed on nsg <b>%s</b><br>\n' % (str(json_cis[i][0])))
                                            passed62='<font color="red">Failed </font>'
                                            failvalue62=1

                            ## Check if all port are opened
                            if ((dport=="*") and action=="Allow" and (src=="*" or src=="Internet") and direction=="Inbound"):
                                acl61=acl61+('<font color="red">All Inbound ports are opened on nsg <b>%s</b></font><br>\n' % (str(json_cis[i][0])))
                                acl62=acl62+('<font color="red">All Inbound ports are opened on nsg <b>%s</b></font><br>\n' % (str(json_cis[i][0])))
                                passed61='<font color="red">Failed </font>'
                                passed62='<font color="red">Failed </font>'
                                failvalue61=1
                                failvalue62=1
                        if (failvalue61==1):
                            # Incread counter for NSG which is not compliant
                            nsgfailvalue61=nsgfailvalue61+1
                            #Reset counter for Next NSG
                            failvalue61=0 
                        else:
                            acl61=acl61+('No Inbound RDP Allowed on nsg <b>%s</b><br>\n' % (str(json_cis[i][0])))
                        if(failvalue62==1):
                            # Incread counter for NSG which is not compliant
                            nsgfailvalue62=nsgfailvalue62+1
                            #Reset counter for Next NSG
                            failvalue62=0
                        else:
                            acl62=acl62+('No Inbound SSH Allowed on nsg <b>%s</b><br>\n' % (str(json_cis[i][0])))
                    # If No ACL defined for NSG, assumed RDP/SSH not allowed
                    else:
                        acl61=acl61+('No ACL defined on nsg <b>%s</b><br>\n' % (str(json_cis[i][0])))
                        acl62=acl62+('No ACL defined on nsg <b>%s</b><br>\n' % (str(json_cis[i][0])))
                else:
                    acl61=acl61+('No public interface defined on nsg <b>%s</b><br>\n' % (str(json_cis[i][0])))
                    acl62=acl62+('No public interface defined on nsg <b>%s</b><br>\n' % (str(json_cis[i][0])))
                #Increasing counter of NSG
                totalvalue61 = totalvalue61+1
                totalvalue62 = totalvalue62+1                
                passvalue61=totalvalue61-nsgfailvalue61
                passvalue62=totalvalue62-nsgfailvalue62
        else:
            acl61="No NSG Configured"
            acl62="No NSG Configured"
            totalvalue61 = 1
            totalvalue62 = 1
            passvalue61 = 1
            passvalue62 = 1
        score61=[acl61,passvalue61,totalvalue61,passed61]
        score62=[acl62,passvalue62,totalvalue62,passed62]
        return [score61,score62]
    except Exception as e:
        logging.error("Exception in check62: %s %s" %(type(e), str(e.args)))
        acl61="Failed to query for NSG or SSH/RDP not allowed"
        acl62="Failed to query for NSG or SSH/RDP not allowed"
        passed61='<font color="orange">UNKNOWN </font>'
        passed62='<font color="orange">UNKNOWN </font>'
        totalvalue61 = 1
        totalvalue62 = 1
        score61=[acl61,passvalue61,totalvalue61,passed61]
        score62=[acl62,passvalue62,totalvalue62,passed62]
        return [score61,score62]

def check63():
    logging.info("Processing 63...")
    st63=""
    passvalue63 = 0
    totalvalue63 = 0
    score63=""
    passed63='<font color="green">Passed </font>'
    try:
        query63='az sql server list --query [*][resourceGroup,name]'
        #query63=('az network nsg list --query "[?contains(id,\'%s\')].[resourceGroup,name]"' % subid)
        json_cis=az_cis_utils.query_az(query63)
        #iteration through SQL Servers
        if (len(json_cis)>0):
            for i in range(len(json_cis)):
                RG = json_cis[i][0]
                SRV = json_cis[i][1]
                queryrp=("az sql server firewall-rule list --resource-group %s --server %s --query [*].[startIpAddress,endIpAddress]" % (RG,SRV))
                try:
                    json_cis2=az_cis_utils.query_az(queryrp)
                    startip=str(json_cis2[0][0])
                    endip=str(json_cis2[0][1])
                    if (startip=="0.0.0.0" and endip=="0.0.0.0"):
                        passed63='<font color="red">Failed </font>'
                        st63=st63+('SQL Server: <b>%s</b> access is not restricted<br></li>\n' % SRV)  
                    else:
                        passvalue63=passvalue63+1
                        st63=st63+('SQL Server: <b>%s</b> access is restricted<br></li>\n' % SRV) 
                    totalvalue63 = totalvalue63+1
                except Exception as e:
                    logging.error('Failed to query SQL Server ' + str(e))
                    st63="Failed to query SQL Server"
                    passed63='<font color="orange">UNKNOWN </font>'
                    totalvalue63 = 1
                    score63=[st63,passvalue63,totalvalue63,passed63]
                    return score63
        else:
            st63="No SQL Server Configured"
            passvalue63 = 1
            totalvalue63 = 1
        score63=[st63,passvalue63,totalvalue63,passed63]
        return score63
    except Exception as e:
        logging.error("Exception in check63: %s %s" %(type(e), str(e.args)))
        st63="Failed to query SQL Server"
        totalvalue63 = 1
        passed63='<font color="orange">UNKNOWN </font>'
        score63=[st63,passvalue63,totalvalue63,passed63]
        return score63


def check64(subid):
    logging.info("Processing 64...")
    st64=""
    passvalue64 = 0
    totalvalue64 = 0
    score64=""
    passed64='<font color="green">Passed </font>'
    try:
        query64='az network nsg list --query [*][resourceGroup,name]'
        #query64=('az network nsg list --query "[?contains(id,\'%s\')].[resourceGroup,name]"' % subid)
        json_cis=az_cis_utils.query_az(query64)
        #iteration through NSG
        if (len(json_cis)>0):
            for i in range(len(json_cis)):
                RG = json_cis[i][0]
                NSG = json_cis[i][1]
                queryrp=("az network watcher flow-log show --resource-group %s --nsg %s" % (RG,NSG))
                try:
                    json_cis2=az_cis_utils.query_az(queryrp)
                    status=str(json_cis2['retentionPolicy']['enabled'])
                    days=json_cis2['retentionPolicy']['days']
                    if (days<90 or status is False):
                        passed64='<font color="red">Failed </font>'   
                    else:
                        passvalue64=passvalue64+1
                    totalvalue64 = totalvalue64+1
                    st64=st64+('NSG: <b>%s</b> Enabled: <font color="blue"><b>%s</b></font> Days <font color="blue"><b>%d</b></font><br></li>\n' % (NSG,status,days))
                except Exception as e:
                    logging.error('Failed to query for network watcher flow-log ' + str(e))
                    st64="Failed to query for network watcher flow-log"
                    passed64='<font color="orange">UNKNOWN </font>'
                    totalvalue64 = 1
                    score64=[st64,passvalue64,totalvalue64,passed64]
                    return score64
        else:
            st64="No NSG Configured"
            passvalue64 = 1
            totalvalue64 = 1
        score64=[st64,passvalue64,totalvalue64,passed64]
        return score64
    except Exception as e:
        logging.error("Exception in check64: %s %s" %(type(e), str(e.args)))
        st64="Failed to query for NSG"
        totalvalue64 = 1
        passed64='<font color="orange">UNKNOWN </font>'
        score64=[st64,passvalue64,totalvalue64,passed64]
        return score64


def check65(subid):
    logging.info("Processing 65...")
    passed65='<font color="red">Failed </font>'
    numberegions=0
    totalregions = 27
    try:
        query65='az network watcher list'
        #query65=('az network watcher list --query "[?contains(id,\'%s\')]"' % subid)
        json_cis=az_cis_utils.query_az(query65)
        if (len(json_cis)>0):
            #iteration through existing regions
            for i in range(len(json_cis)):
                numberegions = numberegions+1
                region = json_cis[i]['location']
                state = json_cis[i]['provisioningState']
            if (numberegions==27):
                passed65='<font color="green">Passed </font>'
            st65=('Enabled on <font color="blue"><b>%d</b></font>/%dregions</li>' % (numberegions, totalregions,))
        else:
            st65="Network Watcher not found"
        score65=[st65,numberegions,totalregions,passed65]
        return score65
    except Exception as e:
        logging.error("Exception in check65: %s %s" %(type(e), str(e.args)))
        st65="Failed to query for network watcher"
        passed65='<font color="orange">UNKNOWN </font>'
        score65=[st65,numberegions,totalregions,passed65]
        return score65
