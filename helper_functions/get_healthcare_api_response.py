import requests
import nferx_py.fn as nf
import base64
import json

nferxAuth ={
        "accessKey" : "harish@nference.net",
        "secretKey": "8b711abdab60298e97d8d61e2f998b49"
        }

def get_nferx_auth_details(nferxAuthDetails):
    accessKey = nferxAuthDetails.get("accessKey","")
    secretKey = nferxAuthDetails.get("secretKey","")
    headers = {}
    if accessKey != "" and secretKey != "":
        key = '%s:%s' % (accessKey, secretKey)
        nferxAuth = base64.standard_b64encode(key.encode('utf-8')).decode('utf-8')
        headers = {'Authorization': 'Basic %s' % nferxAuth}
    return headers


headers = get_nferx_auth_details(nferxAuth)
headers["Content-Type"] = 'application/json'
params = {}
params["subsume"] = "unconditional"

url = "https://preview.nferx.com/nfer_doctor/v2/get_entities"


def make_post_call(url, data, headers={}, params={}, timeout=None, retry=5):
    response = {}
    try:
        for i in range(0, retry):
            response = requests.post(url, data=data, headers=headers,
                params=params, timeout=timeout)
            if response.status_code == 200:
                return response.json()
            else:
                import pdb;pdb.set_trace()
    except Exception as e:
        print(e)
        
def get_healthcare_api_response(text_sample):
    data = {"text": [text_sample]}
    chunk_resp = make_post_call(url, data=json.dumps(data), headers=headers, params=params)
    return chunk_resp


 