#region "Imports"
import pytest
from datetime import datetime,timedelta
import json
from random import randint

orderList = lambda orderCount, orderRangeHours=10 : [{'orderId':i, 'orderPlaced': (datetime.now() + timedelta(hours=randint(-orderRangeHours,orderRangeHours))).isoformat(timespec='milliseconds')} for i in range(orderCount) ]

employeeList = lambda employeeCount, employeeHours=8: [
                    {'employeeId':f"{i:04}", 
                    'startTime': (datetime.now() + timedelta(hours=randint(-employeeHours,0))).isoformat(timespec='milliseconds'),
                    'endTime': (datetime.now() + timedelta(hours=randint(1,employeeHours))).isoformat(timespec='milliseconds')
                    } 
                    for i in range(employeeCount) 
                ]

sampleOrder = lambda orderCount, employeeCount, employeeHours=16 : { 
     'eventAt' : datetime.now().isoformat(timespec='milliseconds'),
     'storeState': {
		"storeId": 1,
		"ovenTimeSeconds": 10
    	},
     'storeOrders' : orderList(orderCount),
     'storeEmployees' : employeeList(employeeCount,employeeHours)
     }

with open('output.json', 'w') as f:
    json.dump(sampleOrder(100,5), f, indent=4)
