The framework has two distinctive parts.

- A **core** that is developed by the Fetch.ai team as well as external contributors.
- **Extensions** (also known as **packages**) developed by any developer.

Currently, the framework supports four types of packages which can be added to the core as modules:

- <a href="../skill">Skills</a> are the core focus of the framework's extensibility as they implement business logic to deliver economic value for the AEA.
- <a href="../protocol">Protocols</a> define agent-to-agent as well as component-to-component interactions (messages and dialogues) within agents.
- <a href="../connection">Connections</a> wrap SDKs or APIs and provide an interface to network, ledgers and other services.
- <a href="../contract">Contracts</a> wrap smart contracts for Fetch.ai and third-party decentralized ledgers.

The following figure illustrates the framework's architecture:

<img src="../assets/simplified-aea.jpg" alt="Simplified illustration of an AEA" class="center" style="display: block; margin-left: auto; margin-right: auto;width:100%;">


The execution is broken down in more detail below:

<img src="../assets/execution.jpg" alt="Execution of an AEA" class="center" style="display: block; margin-left: auto; margin-right: auto;width:100%;">

The agent operation breaks down into three parts:

* Setup: calls the `setup()` method of all registered resources
* Operation:
    * Main loop (Thread 1 - Synchronous):
        * `react()`: this function grabs all Envelopes waiting in the `InBox` queue and calls the `handle()` function on the Handler(s) responsible for them. As such it consumes and potentially produces `Messages`.
        * `act()`: this function calls the `act()` function of all registered Behaviours. As such it potentially produces `Messages`.
        * `update()`: this function enqueues scheduled tasks for execution with the `TaskManager` and executes the decision maker.
    * Task loop (Thread 2- Synchronous): executes available tasks
    * Decision maker loop (Thread 3- Synchronous): processes internal messages
    * Multiplexer (Thread 4 - Asynchronous event loop): the multiplexer has an event loop which processes incoming and outgoing messages across several connections asynchronously.
* Teardown: calls the `teardown()` method of all registered resources


To prevent a developer from blocking the main loop with custom skill code, an execution time limit is  applied to every `Behaviour.act` and `Handler.handle` call.

By default, the execution limit is set to `0` seconds, which disables the feature. You can set the limit to a strictly positive value (e.g. `0.1` seconds) to test your AEA for production readiness. If the `act` or `handle` time exceed this limit, the call will be terminated.

An appropriate message is added to the logs in the case of some code execution being terminated.


<br />
