import requests
import sys
import re
import os
from dotenv import load_dotenv

load_dotenv()

mail = os.getenv('EMAIL')

if len(sys.argv) > 1:
    mail = sys.argv[1]

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
if not re.search(regex,mail):
    print('INVALID MAIL')
    sys.exit(0)

request_token = requests.get('https://rooftop-career-switch.herokuapp.com/token?email='+mail)
TOKEN=request_token.json()['token']

request_block = requests.get('https://rooftop-career-switch.herokuapp.com/blocks?token='+TOKEN)
array_job = request_block.json()['data']
original_size = len(array_job)

#INCIALIZO
array_order = []
array_order.append(array_job.pop(0))
copyA = array_job[::-1]

def checkValue(v2):
    last = array_order[-1]
    block = {'blocks': [last,v2]}
    check = requests.post('https://rooftop-career-switch.herokuapp.com/check?token='+TOKEN, json=block)
    if check.json()['message']:
        array_order.append(v2)
        return True
    return False

while len(array_order) != original_size:
    for i in range(len(copyA)):
        if copyA[i] in array_order:
            continue
        v2 = copyA[i]
        if checkValue(v2):
            break

final={'encoded':''.join(array_order)}
result = requests.post('https://rooftop-career-switch.herokuapp.com/check?token='+TOKEN, json=final)

print('ARRAY INCIAL: ', request_block.json()['data'])
print('ARRAY ORDENADO: ', array_order)
print('RESULTADO FINAL: ', result.json()['message'])
