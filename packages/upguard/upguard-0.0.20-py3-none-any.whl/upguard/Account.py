import json
from .BaseObject import BaseObject
from .VendorList import VendorList
from .Vendor import Vendor
class Account(BaseObject):
    
  def vendors(self):
    obj = self.http_get("https://cyber-risk.upguard.com/api/public/vendors")
    the_list = VendorList(self.api_key)
    for x in obj["vendors"]:
      elem = Vendor(self.api_key)
      if "network_security_score" in x:
        elem.network_security_score = x["network_security_score"]
      if "phishing_score" in x:
        elem.phishing_score = x["phishing_score"]
      if "labels" in x:
        elem.labels = x["labels"]
      if "name" in x:
        elem.name = x["name"]
      if "overall_score" in x:
        elem.overall_score = x["overall_score"]
      if "primary_domain" in x:
        elem.primary_domain = x["primary_domain"]
      if "automated_score" in x:
        elem.automated_score = x["automated_score"]
      if "brand_protection_score" in x:
        elem.brand_protection_score = x["brand_protection_score"]
      if "id" in x:
        elem.id = x["id"]
      if "monitored" in x:
        elem.monitored = x["monitored"]
      if "questionnaire_score" in x:
        elem.questionnaire_score = x["questionnaire_score"]
      if "email_security_score" in x:
        elem.email_security_score = x["email_security_score"]
      if "website_security_score" in x:
        elem.website_security_score = x["website_security_score"]
      the_list.append(elem)
    return the_list
  

    
  def vendor_by_domain(self, hostname):
    url = "https://cyber-risk.upguard.com/api/public/vendor?hostname=" + str(hostname) + ""
    obj = self.http_get(url)
    elem = Vendor(self.api_key)
    elem.brand_protection_score = obj["categoryScores"]["brandProtection"]
    elem.network_security_score = obj["categoryScores"]["networkSecurity"]
    elem.website_security_score = obj["categoryScores"]["websiteSecurity"]
    elem.industry_group = obj["industry_group"]
    elem.industry_sector = obj["industry_sector"]
    elem.overall_score = obj["overallScore"]
    elem.automated_score = obj["automatedScore"]
    elem.email_security_score = obj["categoryScores"]["emailSecurity"]
    elem.phishing_score = obj["categoryScores"]["phishing"]
    elem.id = obj["id"]
    elem.name = obj["name"]
    elem.primary_domain = obj["primary_hostname"]
    elem.questionnaire_score = obj["questionnaireScore"]
    return elem
  

