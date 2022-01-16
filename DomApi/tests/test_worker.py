#region "Imports"
import pytest
from datetime import datetime,timedelta
import json
from random import randint

# with open('output.json', 'w') as f:
#     json.dump(sampleOrder(100,5), f, indent=4)

class TestWorker:
     
     # utility functions for mocking order data
     orderList = lambda orderCount, orderRangeHours=24 : [{'orderId':i, 'orderPlaced': (datetime.now() + timedelta(hours=randint(-orderRangeHours,orderRangeHours))).isoformat(timespec='milliseconds')} for i in range(orderCount) ]
     employeeList = lambda employeeCount, employeeHours=8: [
                         {'employeeId':f"{i:04}", 
                         'startTime': (datetime.now() + timedelta(hours=randint(-employeeHours,0))).isoformat(timespec='milliseconds'),
                         'endTime': (datetime.now() + timedelta(hours=randint(1,employeeHours))).isoformat(timespec='milliseconds')
                         } 
                         for i in range(employeeCount) 
                    ]
     storeState = lambda ovenTimeSeconds = 120 : {
               "storeId": 1,
               "ovenTimeSeconds": ovenTimeSeconds
          }
     sampleOrder = lambda orderCount, employeeCount, employeeHours=8 : { 
          'eventAt' : datetime.now().isoformat(timespec='milliseconds'),
          'storeState': storeState(),
          'storeOrders' : orderList(orderCount),
          'storeEmployees' : employeeList(employeeCount,employeeHours)
          }

     def test_empty_post(self):
          raise NotImplementedError()
     
     def test_zero_employees(self):
          raise NotImplementedError()
     
     def test_zero_orders(self):
          raise NotImplementedError()
     
     def test_invalid_date_format(self):
          raise NotImplementedError()
     
     def test_invalid_employee_start_end(self):
          raise NotImplementedError()
     
     def test_missing_key(self):
          raise NotImplementedError()
     
     def test_extra_key(self):
          raise NotImplementedError()
     
     def test_insufficient_employees(self):
          raise NotImplementedError()
     
     def test_simple_order_known_response(self):
          # test exact response
          # consider output validator
          raise NotImplementedError()
     
     def test_very_long_order(self):
          raise NotImplementedError()
     
     def test_max_content_length_overflow(self):
          raise NotImplementedError()
     

