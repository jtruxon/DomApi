# MLOps take-home assignment


## Store Order Status

Design a simple API using python that evaluates all current orders (orders placed by customers) and determines when the orders are ready to be picked up or delivered and how long it took to prepare the order.

### Requirements
- The API should be containerized and include instructions for building and running the application
- The repo contains an example request payload and response payload.  Your output should match the response example. Note that the example contains one order; your output will contain all orders in the request
- Please complete your work as a feature branch from main, making as many commits as you like, and submit a pull request when you are finished.

### Assumptions
- the life cycle of an order is order placed, order on makeline (employee making order), order in oven, order ready
- to keep things simple, all orders are in the queue (order placed), and none are on the makeline yet
- the time it takes to bake an order in the oven varies by store but is constant for every order in the store. this value is part of the payload and is measured in seconds
- the time it takes to make an order is dependent on how many orders are in front of it and how many employees are available to make an order. Each employee can make one order at a time, and it takes an employee 120 seconds to make an order


The request includes the following:
- Order Data: Order ID, order placed timestamp
- Employee Data: Employee ID, shift start time, shift end time
- Store data: store ID, oven time in seconds
