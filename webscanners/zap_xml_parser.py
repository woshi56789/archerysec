import xml.etree.ElementTree as ET
from webscanners.models import zap_scan_results_db, zap_scans_db
import uuid

spider_status = "0"
scans_status = "0"
spider_alert = ""
target_url = []
driver = []
new_uri = []
cookies = []
excluded_url = []
vul_col = []
note = []
rtt = []
tags = []
timestamp = []
responseHeader = []
requestBody = []
responseBody = []
requestHeader = []
cookieParams = []
res_type = []
res_id = []
url = []
name = []
solution = []
instance = []
sourceid = []
pluginid = []
alert = []
desc = []
riskcode = []
confidence = []
wascid = []
risk = []
reference = []



def xml_parser(root, project_id, scan_id):
    global vul_col, confidence, wascid, risk, reference, url, name, solution, instance, sourceid, pluginid \
        , alert, desc

    for zap in root:
        host = zap.attrib
        for key, items in host.iteritems():
            if key == "host":
                url = items
        for site in zap:
            for alerts in site:
                for alertsitem in alerts:
                    vuln_id = uuid.uuid4()
                    if alertsitem.tag == "pluginid":
                        pluginid = alertsitem.text
                    if alertsitem.tag == "alert":
                        alert = alertsitem.text
                    if alertsitem.tag == "name":
                        name = alertsitem.text
                    if alertsitem.tag == "riskcode":
                        riskcode = alertsitem.text
                    if alertsitem.tag == "confidence":
                        confidence = alertsitem.text
                    if alertsitem.tag == "desc":
                        desc = alertsitem.text
                    if alertsitem.tag == "solution":
                        solution = alertsitem.text
                    if alertsitem.tag == "reference":
                        reference = alertsitem.text
                    if alertsitem.tag == "wascid":
                        wascid = alertsitem.text
                    if alertsitem.tag == "sourceid":
                        sourceid = alertsitem.text
                    for instances in alertsitem:
                        for instance in instances:
                            instance = instance.text

                    global riskcode

                    if riskcode == "3":
                        vul_col = "important"
                        risk = "High"
                    elif riskcode == '2':
                        vul_col = "warning"
                        risk = "Medium"
                    elif riskcode == '1':
                        vul_col = "info"
                        risk = "Low"
                    elif riskcode == '0':
                        vul_col = "info"
                        risk = "Informational"

                    dump_data = zap_scan_results_db(vuln_id=vuln_id, vuln_color=vul_col, scan_id=scan_id,
                                                    project_id=project_id,
                                                    confidence=confidence, wascid=wascid,
                                                    risk=risk, reference=reference, url=url, name=name,
                                                    solution=solution,
                                                    param=instance, sourceid=sourceid,
                                                    pluginId=pluginid,
                                                    alert=alert, description=desc, false_positive='No')
                    dump_data.save()

    zap_all_vul = zap_scan_results_db.objects.filter(scan_id=scan_id).values('name', 'risk', 'vuln_color').distinct()

    total_vul = len(zap_all_vul)
    total_high = len(zap_all_vul.filter(risk="High"))
    total_medium = len(zap_all_vul.filter(risk="Medium"))
    total_low = len(zap_all_vul.filter(risk="Low"))

    zap_scans_db.objects.filter(scan_scanid=scan_id).update(total_vul=total_vul, high_vul=total_high,
                                                            medium_vul=total_medium, low_vul=total_low)
