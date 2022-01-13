#region "Imports"
# import pytest
from flask import Flask, Blueprint, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
from flask_restplus.apidoc import apidoc
import traceback
from functools import wraps
import logging, logging.handlers
from math import ceil
#endregion

#region "Local imports"
from monitor import logger, exceptions_monitored
#endregion


##############################################################################################
#region "Orders_API worker class"

@exceptions_monitored(logger)
class Orders_API:
    #------------------------------------------------------
    def __init__(self, **kwargs):
        self.throwErrors = True
        self.validateOrder = True
        self.orderMakeTimeSeconds = 0
        self.allowEmployeeOverTime = False
        self.preSortOrders = True
        self.defaultTimeZone = 0
        self.orderSchema = ""
        self.orderSchemaFilename = ""

        # override default values with any kwargs passed in
        for k, v in kwargs.items():
            try:
                setattr(self, k, v)
            except:
                pass

        super().__init__()

    #------------------------------------------------------
    def DateString_To_Epoch(self, dateString):
        """
        Converts a date string in the format supplied by the request to the Unix epoch format

        Parameters:
        -----------
        dateString : string
            A string containing the ISO 8601 formatted datetime string

        Returns:
        --------

        float
            The floating point number representing a UNIX epoch timestamp
        """
        from datetime import datetime
        return datetime.fromisoformat(dateString).timestamp()

    #------------------------------------------------------
    def Epoch_To_DateString(self, timeStamp):
        """
        Converts a unix-epoch timestamp to an ISO 8601 date string.  note: time is truncated to the nearest millisecond

        Parameters:
        -----------
        timeStamp : float
            The floating point number representing a UNIX epoch timestamp

        Returns:
        --------

        string
            Returns a string containing the ISO 8601 formatted datetime string for the given timestamp

        """
        from datetime import datetime
        result = datetime.fromtimestamp(timeStamp).isoformat(timespec='milliseconds')
        return result

    #------------------------------------------------------
    def Validate_OrderSchema(self, orders):
        """
        Validates the structure of a json object using a predefined schema

        This function checks the structure of the given orders object using jsonschema validation.  The schema is loaded from a file
        that's specified at the class level, and once it's been loaded, that schema is cached against further calls within the current
        class instance.
        REF: https://json-schema.org/

        Parameters:
        -----------
        orders : object
            The json object containing orders submitted by the requester

        Returns:
        --------

        boolean
            Returns a boolean with the validation success status

        """
        import json
        import jsonschema
        from jsonschema import validate

        if self.orderSchema=="":
            with open(self.orderSchemaFilename, 'r') as file:
                self.orderSchema = json.load(file)

        result = True
        try:
            validate(instance=orders, schema=self.orderSchema)
        except jsonschema.exceptions.ValidationError as err:
            result = False

        return result

    #------------------------------------------------------
    def Validate_Orders(self, orders):
        """
        Validate the structure & content of the order.

        This function checks the structure of the request using jsonschema validation, and runs a sanity check against a few key properties

        Parameters:
        -----------
        orders : object
            The json object containing orders submitted by the requester

        Returns:
        --------

        boolean
            Returns a boolean with the validation success status

        """
        from datetime import datetime

        #TODO: log results of this Validation

        # confirm that the order is valid, conforming to the spec
        if not self.Validate_OrderSchema(orders):
            return False

        #cycle through employees to ensure valid start/end times
        validStartEndPair = lambda employee: self.DateString_To_Epoch(employee["startTime"]) < self.DateString_To_Epoch(employee["endTime"])
        for employee in orders["storeEmployees"]:
            if not validStartEndPair(employee): return False

        return True

    #------------------------------------------------------
    def Get_Order_Processing_Times(self, orders):
        """
        Determine the completion stats for a batch of submitted orders, given a set of available employees.

        This function takes a json string containting a batch of orders and a set of employees available to process them.
        These orders are then validate, and distributed among the available employees, calculating the absolute completion times
        and total make times for each pizza.

        Parameters:
        -----------
        orders : string
            Contains the raw json string of orders submitted by the requester

        Returns:
        --------

        object
            Returns an object containing the orders, with absolute completion times and total make times for each pizza

        """

        from queue import PriorityQueue
        import json

        # load it up. CYA with try/except
        try:
            ordersObject = json.loads(orders)
        except:
            return None, False, "Posted order is not valid JSON"

        #validate if necessary
        if self.validateOrder and not self.Validate_Orders(ordersObject):
            return None, False, "Posted order does not pass schema validation"

        #grab the oven time for this order, calculate the minimum cycle time for a pie
        ovenTimeSeconds = ordersObject["storeState"]["ovenTimeSeconds"]
        minCycleTimeSeconds = ovenTimeSeconds + self.orderMakeTimeSeconds

        #precompute timestamps for all orders, sort if necessary
        ordersList = ordersObject["storeOrders"]
        for order in ordersList: order["orderPlaced"] = self.DateString_To_Epoch(order["orderPlaced"])
        if self.preSortOrders: ordersList.sort(key=lambda i: i["orderPlaced"])

        #precompute timestamps for all employees, and add to priority queue
        employeesList = ordersObject["storeEmployees"]
        employeeQueue = PriorityQueue()
        employeeCount = len(employeesList)
        for idx,employee in enumerate(employeesList):
            employee["startTime"] = self.DateString_To_Epoch(employee["startTime"])
            employee["endTime"] = self.DateString_To_Epoch(employee["endTime"])
            startTime = float(employee["startTime"])
            employeeQueue.put((startTime,idx,employee),False)

        #quick lambda to ease readability - returns boolean indicating whether the given employee could complete the
        #   given order before the end of their shift
        employeeHasTime = lambda e,p: max(e["startTime"],p["orderPlaced"]) + minCycleTimeSeconds <= e["endTime"]

        #iterate through items, find an employee to make it, update records as appropriate
        for idx,pizza in enumerate(ordersList):
            itemComplete = False

            while not itemComplete:
                #sanity check that we haven't run out of staff resources
                if not employeeQueue.qsize() > 0:
                    #quit processing and return results
                    return ordersObject, False, "Insufficient staff specified for the current order."

                #pop first available employee based on earliest start time, and confirm that they have time to make the pie
                employee = employeeQueue.get()[2]

                #note: at this point, all times are expressed in seconds, so we can just add values up

                #check to see if this employee will be onsite long enough to make the pie
                hasTime = employeeHasTime(employee,pizza)
                if hasTime or self.allowEmployeeOverTime:
                    #calculate pizza absolute completion time and time to make in seconds
                    completionTime = max(employee["startTime"],pizza["orderPlaced"])+minCycleTimeSeconds
                    orderMakeSeconds = completionTime-pizza["orderPlaced"]
                    #write values back to orders object
                    employee["startTime"]=completionTime
                    pizza["orderPlaced"]=self.Epoch_To_DateString(pizza["orderPlaced"])
                    pizza["orderReady"]=self.Epoch_To_DateString(completionTime)
                    pizza["orderMakeSeconds"]=ceil(orderMakeSeconds)

                    #requeue the employee if appropriate, with updated startTime.  if we allowed overtime, then this is their last pie,
                    #  and we will not be requeueing them.  this will limit the overtime for any employee to the time to complete the pizza they
                    #  started while they were still on normal time
                    if hasTime: employeeQueue.put((completionTime,idx+employeeCount,employee))

                    #item is complete
                    itemComplete=True

                else:
                    #this is a redundant line, just making it clear that if the current employee doesn't have time, it's because
                    #  they're leaving too soon to make another pie.  cycle to the next employee.
                    continue

        #we've stepped through each order, clean up the order object and return results
        del ordersObject["storeState"]
        del ordersObject["storeEmployees"]

        return ordersObject, True, ""

#endregion

##############################################################################################
# #region "Flask run"
# if __name__ == "__main__":
#     from rest_wrapper.wrapper import Run
#     Run()
# #endregion
