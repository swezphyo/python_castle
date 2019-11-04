"""
Azure Automation documentation : https://aka.ms/azure-automation-python-documentation
Azure Python SDK documentation : https://aka.ms/azure-python-sdk
"""
import automationassets
import requests
import smtplib
import base64

URL = 'https://www.meemee.online/api/external-validation'

def send_mail():
    '''this function is called when the URL is availble
    - send mail to the related users.
    '''
    cred = automationassets.get_automation_credential("RunBookEmailCred")
    username = cred["username"]
    sender = username
    receiver = ['zzzz@outlook.com']
    password = cred["password"]
    smtpsrv = "smtp.office365.com"
    smtpserver = smtplib.SMTP(smtpsrv,587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(sender, password)
    msg = """Subject : Mother Finance Alert

    ALERT: Mother Finance website is unavaible.
    """
    smtpserver.sendmail(sender, receiver, msg)
    print 'Successfully sent mail'
    smtpserver.close()

def main():
    cred = automationassets.get_automation_credential("app_id_mother_finance")
    _id_app = cred["password"]
    cred = automationassets.get_automation_credential("secret_key_mother_finance")
    key_value = cred["password"]
    header = { 
       "app-id" : _id_app,
       "secret-key" : key_value,
       "Accept" : "application/json",
       "Content-Type" : "application/json"
    }
    payload = {"nrc": "12/YaKaNa(N)123344", "phone_number" : "097934333323"}
    #Post method to check the api
    response = requests.post(URL, params=payload, headers=header)
    response_data = response.json()

    if (response.status_code == 200):
        print "Mother finance website is up and running"
    elif(response.status_code == 422) or (response.status_code == 400):
        #ref : https://www.keycdn.com/support/422-unprocessable-entity 
        errors = response_data.get('errors')
        print errors
    else:
        send_mail()


if __name__ == '__main__':
    main()





