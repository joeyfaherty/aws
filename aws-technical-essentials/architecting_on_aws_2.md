# Day 2
---
[aws certification](https://d0.awsstatic.com/training-and-certification/docs-sa-assoc/AWS_certified_solutions_architect_associate_blueprint.pdf) 

### Network Access Control List (NACL)
* Stateless firewall
* Works on subnet level
* Automatically allows outgoing traffic
* Add rule priority in increments of 50 or 100

### Security groups
* Stateful firewall
* Works on instance level
* Ability to define security groups as a source (this is useful for multi-tier applications, where you want the app server only in communication with the db server on a specific port and nothing else)
* When creating rds instances, you are asked if you would like a security group for this, as it usually will only allow traffic to your app servers

### Connecting to an on premise network
* Side to side VPN - CGW-VPN
* AWS Direct Connect - doesnt use internet, uses private network connections. You need to work with telecommunications provider to get this.

### VPN Best Practices
* Dont use default VPC in production, only used for testing. Create your own.
* Pick CIDR block (IP ranges) wisely by selecting something big enough for future growth (or run multiple VPCs): start with "/16"
* The primary purpose of subnets is to divide resources based on access, so they should be leveraged that way.
*	Use Multi-AZ deployments in VPC for high availability.
*	Use security groups to control traffic between resources. You can specify granular security policy for Amazon EC2 instances using a security group.
*	VPC Flow Logs stores traffic logs for a particular VPC, VPC subnet, or Elastic Network Interface to CloudWatch Logs, where they can be accessed by third-party tools for storage and analysis.

---

# Making Your Environment Highly Available

***"everything fails, all of the time"***

App 
    => DB Main (Anti-pattern)
App

App 
    => DB Main => DB Secondary (Best Practice)
App

It is better to have an active/passive architecture where data is replicated to a secondary node so that there is no ___single point of failure___.

Recovery Time Objective (RTO) - How quickly must the system recover?
Recovery Point Objective (RPO) - How much data can you afford to lose?
So, how much money do you need to spend to meet these requirements?

Fault tolerence
* built in redundancy of components
Recoverability
* Automated processes, policies and proceedures to restore service after a disater event
Scalability
* Automated accomodation of growth of your application.
* ___BP___ App servers scale based on an alarm.  Autoscaling is alreted and scales in/out based on rules.

Scaling types
Vertical | Horizontal
--- | ---
Up and down | in and out
Change of specs (memory, CPU) | change in # of instances


## ELB (Elastic Load Balancer)
* distributes load between instances
* cross AZ load balancing
* recognises unhealthy instances with a health check.
* public or internal-facing (private) ELBs. If ELB is public, then your App servers can now be in a private subnet.
* ELBs can help prevent DoS attacks.
* Sticky sessions (every client will always get directed to the same server, without this if your session data is on one server and your next request is directed to another server, then this new server will not have your session data!)

___BP___ - Use ELBs on every level. Public ELB and internal-facing ELB between App servers.

#### Elastic IP Address:
Linked to the VPC. Used so that URL can be used for a website
If a client goes down, then a user can use same address to reach the replacement server.

#### AWS Route 53
Available at edge locations


#### AWS CloudWatch
* Metrics, Logs, Status checks, create custom metrics
* Memory checks need to be checked by you
* Alarms - Latency, CPU, # of connections, ELB healthy hosts 
* Actions - Executed after an alarm. 
Action examples; 
1. Shutdown instances after 6pm and restart instances at 8am
2. Scale an auto scaling group in or out
3. Send email or SNS

#### AutoScaling
TV operator example: Champions League Final, huge peak of viewer, so you need extra instances on this date so we scale up. After the event we scale back down to or usual traffic.
* launch across AZs
* Scale up very quickly (automate process). Scale down very slowly, so users are not impacted. (Avoiding AS thrashing)
* Ensure your autoscale across AZs
* Take into account how long it is over the threshold for, if it is 1 sec we dont care, but over 80% for more than x minutes, then alarm is triggered.
* Set min and max values carefully

How does AS work?
___Launch Configuration - What___
* name, ami, instance type etc
___Auto scaling group - Where___
* Name, Launch Config Name, min and max, load balancer, desired capacity (between min and max)
___When___
* Alarms - Increase or decrease EC2 instances based on cloudwatch alarms
* Scheduled Acion - tells AS to perform a scaling action at a certain time in the future.



#### EC2 Auto Recovery
* Only available for larger instances types
* Will ahve same IP, same metadata, so config but will lose all data in memory of course
* Unlike autoscaling (create and terminate instances so the IPs will be different)



### Scaling Data Stores
---
#### RDS Scaling
Scale up or down. This will trigger a reboot in the background.
Offload read traffic to Read Replicas. Keep master instance for write operations.
Caching:
Put a cache in front of RDS. Maybe you can cache 80% of operations.

Sharding:
* without shards all data resides in one partition.
* sharding can spilt your data into different chunks (shards)
example: Users by last name A to M in one database. M to Z in another database.


## AWS Lambda and Event-Driven Scaling
* Allows to run code with managing infrastructure like EC2 instances and AS groups
* Multiple language support (Java, Python, Nodejs)
* Lambda functions can call other lambda functions
* Difficult to test/debug as it needs to be run on the environment
* [serverless.org can be used for testing and replicating aws env](https://serverless.com/framework/docs/providers/aws/guide/quick-start/)
* auto scale
* Never use password or access keys within lambda, always use roles for authentication

# LAB 3


## 6. Automating Your Infrastructure
Automation Scripting:
* Reliable - Eliminate human error. 
* Reproducability - dev, test, prod
* ___BP___ Use disposable resources: Automate deployment of new resources with identical configurations.
* Switch to new IP addresses automagically EIP
* ___BP___ Infrastructure as code - Keep scripts and config version controlled.

### Cloud Formation - Build your environemnt - "Infrastructure as code"
* launch, configure and connect AWS resources
* ___template___ - json formatted file that describes each resource to be created, that works as our source code
* ___cloudformation engine___ - interprets json file template into stacks of AWS resources
* ___stack___ - collection of resources created by cloud formation
* [terraform.io](terraform.io)
* depends on - depends on another resource
* Wait conditions - wait until something is up, ready
* conditions - add conditional logic
* ___BP___ Parametrize ec2 key pairs, security group names, subnet IDs, EBS Snapshot IDs
* ___BP___ Similar to coding standards, split your templates into modular templates

### Other infra as code service option on AWS - "AWS elastic Beanstalk"
* Specifically for web apps, you pick a web platform where your app will be deployed
* automatically handles autoscaling, ELBs etc etc
blue/green deployment
* keep both elbs warm
* roll back quickly if anything goes wrong


## 7. Decoupling Your Infrastructure
___BP___ "Change or failure of one component should not affect other components"
#### Strategies:
* use a load balancer for decoupling between web servers and app servers
* serverless architecture
* use queues (kafka, kinesis, etc) allow for asynchronous message processing and decouplign of components
* static web assests stored externally such as s3
* external configuration server


### SOA Service-Oriented Architecture
#### MicroServices
* small independant services within an SOA
* each service is focused on one small task

#### Anti-patterns
* apps communicate directly with one another
* backend servers handling user state storage and user authentication

### Simple Queue Service SQS
* 256 kb message limit
* no guarantee of ordering
* you are reponsible for queue clean up. Messages stay on queue until explicity deleted
