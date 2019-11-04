import automationassets
cred = automationassets.get_automation_credential("app_id_mother_finance")
_id_name = cred["username"]
_id_pwd = cred["password"]

print(_id_name)
print(_id_pwd)

cred = automationassets.get_automation_credential("secret_key_mother_finance")
_key_name = cred["username"]
_key_pwd = cred["password"]
print(_key_name)
print(_key_pwd)