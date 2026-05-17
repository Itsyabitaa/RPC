# Remote Procedure Call (RPC) Framework with Calculator Service

## Project Overview

This project is a custom-built communication system that allows two different computer programs to communicate with each other over a network as if they were working on the same machine.

The project demonstrates how remote systems can send requests, process operations, and return results automatically through a simple and organized communication process.

To demonstrate the framework, the project includes a calculator service where one computer can request mathematical operations such as addition, subtraction, multiplication, and division from another computer remotely.

The entire system is built from scratch using Python without using existing RPC libraries.

---

## Purpose of the Project

In modern software systems, applications are often distributed across multiple computers or servers. These systems need a reliable way to communicate with each other.

The purpose of this project is to:

* Understand how remote communication between systems works
* Build a communication framework from scratch
* Simulate how large-scale distributed systems operate
* Learn how requests and responses travel across a network
* Demonstrate reliability mechanisms in network communication
* Explore how services can be accessed remotely

This project is educational and focuses on understanding the core concepts behind distributed systems and remote communication technologies.

---

## What Problem Does the Project Solve?

Normally, when a program needs to perform an operation, it runs the operation locally on the same computer.

However, in distributed systems:

* The service may exist on another computer
* The data may be stored remotely
* Different systems may need to communicate continuously

This project solves that challenge by creating a framework where:

1. A client sends a request to another computer
2. The server receives and processes the request
3. The result is returned to the client automatically

To the user, the process feels simple and seamless even though the operation happens remotely.

---

## Simple Real-World Example

Imagine using a banking mobile application:

* You request your account balance
* Your phone sends a request to a remote banking server
* The server processes the request
* The result is sent back to your phone

This project works in a similar way.

The calculator service demonstrates this communication process in a simple and understandable manner.

---

## Main Features

### Remote Communication

Allows two programs to communicate through a network connection.

### Calculator Service

Supports operations such as:

* Addition
* Subtraction
* Multiplication
* Division

### Request and Response System

The client sends requests and receives responses automatically.

### Data Conversion

The framework converts data into a transferable format before sending it through the network.

### Reliability Mechanism

If a message fails to arrive, the system can resend the request to improve reliability.

### Automatic Interface Generation

The project can automatically generate communication interfaces from a simple service description file.

---

## Technologies Used

* **Python Programming Language**
* **TCP Socket Communication**
* **JSON-Based Data Formatting**
* **Multi-threading** for handling multiple users

---

## Expected Outcomes

By completing this project, the team will gain practical experience in:

* Distributed systems
* Network communication
* Client-server architecture
* Protocol design
* Reliability mechanisms
* Software architecture principles

---

## Educational Value

This project helps students understand the foundational ideas behind technologies used in:

* Cloud computing
* Banking systems
* Mobile applications
* Online services
* Microservices architecture
* Distributed platforms

It provides hands-on experience with concepts that are commonly used in real-world software systems.

---

## Conclusion

The Remote Procedure Call (RPC) Framework project is designed to demonstrate how computers and software systems communicate remotely in a structured and reliable way.

Although the calculator service is simple, it represents the same fundamental communication principles used in many modern distributed applications and enterprise systems.

The project focuses on learning, experimentation, and understanding the internal mechanisms of remote communication technologies by building them from the ground up.
