import json
from .BaseObject import BaseObject
from .VendorList import VendorList
from .Vendor import Vendor
from .VulnerabilityList import VulnerabilityList
from .Vulnerability import Vulnerability
class Account(BaseObject):
    
  def monitor_vendor(self, hostname):
    url = "https://cyber-risk.upguard.com/api/public/vendor?hostname=" + str(hostname) + ""
    obj = self.http_get(url)
    elem = Vendor(self.api_key)
    if "categoryScores" in obj:
      if "networkSecurity" in obj["categoryScores"]:
        elem.network_security_score = obj["categoryScores"]["networkSecurity"]
    if "categoryScores" in obj:
      if "phishing" in obj["categoryScores"]:
        elem.phishing_score = obj["categoryScores"]["phishing"]
    if "categoryScores" in obj:
      if "websiteSecurity" in obj["categoryScores"]:
        elem.website_security_score = obj["categoryScores"]["websiteSecurity"]
    if "id" in obj:
      elem.id = obj["id"]
    if "questionnaireScore" in obj:
      elem.questionnaire_score = obj["questionnaireScore"]
    if "automatedScore" in obj:
      elem.automated_score = obj["automatedScore"]
    if "categoryScores" in obj:
      if "brandProtection" in obj["categoryScores"]:
        elem.brand_protection_score = obj["categoryScores"]["brandProtection"]
    if "categoryScores" in obj:
      if "emailSecurity" in obj["categoryScores"]:
        elem.email_security_score = obj["categoryScores"]["emailSecurity"]
    if "industry_group" in obj:
      elem.industry_group = obj["industry_group"]
    if "industry_sector" in obj:
      elem.industry_sector = obj["industry_sector"]
    if "name" in obj:
      elem.name = obj["name"]
    if "overallScore" in obj:
      elem.overall_score = obj["overallScore"]
    if "primary_hostname" in obj:
      elem.primary_domain = obj["primary_hostname"]
    return elem
  

    
  def vendors(self):
    next_page_token = None
    the_list = VendorList(self.api_key)
    while True:
      url = "https://cyber-risk.upguard.com/api/public/vendors"
      if next_page_token != None:
        url += "&page_token=" + next_page_token
      obj = self.http_get(url)
      if len(obj["vendors"]) == 0:
        break
      for x in obj["vendors"]:
        elem = Vendor(self.api_key)
        if "categoryScores" in x:
          if "networkSecurity" in x["categoryScores"]:
            elem.network_security_score = x["categoryScores"]["networkSecurity"]
        if "labels" in x:
          elem.labels = x["labels"]
        if "monitored" in x:
          elem.monitored = x["monitored"]
        if "overallScore" in x:
          elem.overall_score = x["overallScore"]
        if "questionnaireScore" in x:
          elem.questionnaire_score = x["questionnaireScore"]
        if "automatedScore" in x:
          elem.automated_score = x["automatedScore"]
        if "categoryScores" in x:
          if "brandProtection" in x["categoryScores"]:
            elem.brand_protection_score = x["categoryScores"]["brandProtection"]
        if "categoryScores" in x:
          if "emailSecurity" in x["categoryScores"]:
            elem.email_security_score = x["categoryScores"]["emailSecurity"]
        if "name" in x:
          elem.name = x["name"]
        if "primary_hostname" in x:
          elem.primary_domain = x["primary_hostname"]
        if "categoryScores" in x:
          if "phishing" in x["categoryScores"]:
            elem.phishing_score = x["categoryScores"]["phishing"]
        if "categoryScores" in x:
          if "websiteSecurity" in x["categoryScores"]:
            elem.website_security_score = x["categoryScores"]["websiteSecurity"]
        if "id" in x:
          elem.id = x["id"]
        the_list.append(elem)
      next_page_token = obj["next_page_token"]
    return the_list
  

    
  def vendor_by_domain(self, hostname):
    url = "https://cyber-risk.upguard.com/api/public/vendor?hostname=" + str(hostname) + ""
    obj = self.http_get(url)
    elem = Vendor(self.api_key)
    if "automatedScore" in obj:
      elem.automated_score = obj["automatedScore"]
    if "categoryScores" in obj:
      if "emailSecurity" in obj["categoryScores"]:
        elem.email_security_score = obj["categoryScores"]["emailSecurity"]
    if "categoryScores" in obj:
      if "networkSecurity" in obj["categoryScores"]:
        elem.network_security_score = obj["categoryScores"]["networkSecurity"]
    if "id" in obj:
      elem.id = obj["id"]
    if "overallScore" in obj:
      elem.overall_score = obj["overallScore"]
    if "questionnaireScore" in obj:
      elem.questionnaire_score = obj["questionnaireScore"]
    if "categoryScores" in obj:
      if "brandProtection" in obj["categoryScores"]:
        elem.brand_protection_score = obj["categoryScores"]["brandProtection"]
    if "categoryScores" in obj:
      if "phishing" in obj["categoryScores"]:
        elem.phishing_score = obj["categoryScores"]["phishing"]
    if "categoryScores" in obj:
      if "websiteSecurity" in obj["categoryScores"]:
        elem.website_security_score = obj["categoryScores"]["websiteSecurity"]
    if "industry_group" in obj:
      elem.industry_group = obj["industry_group"]
    if "industry_sector" in obj:
      elem.industry_sector = obj["industry_sector"]
    if "name" in obj:
      elem.name = obj["name"]
    if "primary_hostname" in obj:
      elem.primary_domain = obj["primary_hostname"]
    return elem
  

