# test-scheduler
#### An enhanced greedy approach to the Test Scheduling Problem
This Python script uses an enhanced greedy heuristic to solve the Test Scheduling Problem as defined [here](http://csplib.org/Problems/prob073/) and [here](http://csplib.org/Problems/prob073/assets/description.pdf). The problem was also presented as the Industrial Modelling Challenge at CP2015.

#### The problem
The problem arises in the context of a testing facility. A number of tests have to be performed in minimal time. Each test has a given duration and needs to run on one machine. While the test is running on a machine, no other test can use that machine. Some tests can only be assigned to a subset of the machines, for others you can use any available machine. For some tests, additional, possibly more than one, global resources are needed. While those resources are used for a test, no other test can use the resource. The objective is to finish the set of all tests as quickly as possible, i.e. all start times should be non-negative, and makespan should be minimized. The makespan is the difference between the start of the earliest test, and the end of the latest finishing test. The objective of the original industrial problem is to minimize the time required to find a schedule plus the time required to run that schedule, i.e. to minimize the time between the release of the dataset and the conclusion of all tests required. As this objective depends on the speed of the machine(s) on which the schedule is generated, it is hard to compare results in an objective fashion.

#### The algorithm
The algorithm represents an improved, multi-start greedy approach to solving the problem. Greedy algorithms belong to the constructive class of heuristics. They start with an empty solution. In each subsequent step, they make optimal locally optimal choices. That is, they assign to a decision variable the value that contributes the most toward the final goal of the problem. Multi-start heuristics make multiple "passes" over the problem instance, each time with a different starting solution. In the context of the algorithm applied for this particular problem, "multi-start" means that each pass over the problem instance applies a different iteration logic.

The algorithm makes three passes over the input problem instance:
1. Run the algorithm on sorted instance starting with the **shortest** test
2. Run the algorithm on sorted instance starting with the **longest** test
3. Run the algorithm on sorted instance starting with the test **with no global resource requirements**

The pseudocode of the algorithm is as follows:

```
While there are unscheduled tests:
    For each test t in the sorted list of tests:
        For each machine m that test t can be executed on:
            If machine m is free AND (t does not require a global resource OR
                                      all required global resources are free):
                Add test t to the list of scheduled tests
                If current_time + duration_of_test_t > max_time:
                    max_time = current_time + duration_of_test_t
                Lock the machine while test t is being executed on it
                If t uses a global resource:
                    Lock the global resource
    current_time += 1
    For each test x in list of scheduled tests:
    Remove x from the sorted list of tests
```
#### Additional information
For an example of a problem instance and further information, please see [this document](http://csplib.org/Problems/prob073/assets/description.pdf).
