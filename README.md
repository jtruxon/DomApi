# Order completion times

We would like you to design a simple API using Python.

The goal is to create an endpoint that does the following:

- Accepts a set of current customer orders
- Determines the following:
	- When each order will be ready
	- How long it took to prepare each order

Please complete your work as a branch from `main`, making as many commits as you like, and submit a pull request when you are finished.

## Requirements

- The API should be built and run in a Docker container
- Please include instructions (an `INSTRUCTIONS.md` file is fine) for building and running the application
- Use the provided `request_example.json` payload to test your code
- Your output should match the format of `response_example.json` (but should contain all orders from the request)

## Data

The `request_example.json` has the following structure:

- Order data: order ID, order placed timestamp
- Employee data: employee ID, shift start time, shift end time
- Store data: store ID, oven time in seconds

## Assumptions

- The life cycle of an order after it is placed is:
	1. Order being made (assume 2 minutes for every order)
	2. Order in the oven
	3. Order ready
- All orders are submitted to the queue at the same time
- The oven time varies by store but is constant for every order
- Each employee can only make one order at a time
