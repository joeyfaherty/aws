## Day 2
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
* Scale up very quickly (automate process). Scale down very slowly, so users are not impacted.

How does AS work?
1. Launch Configuration - What
* name, ami, instance type etc
2. Auto scaling group - Where
* Name, Launch Config Name, min and max, load balancer, desired capacity (between min and max)
3. When
* Alarms - Increase or decrease EC2 instances based on cloudwatch alarms
* Scheduled Acion - tells AS to perform a scaling action at a certain time in the future.

Forklifting an Existing Application onto AWS

Event-Driven Scaling
Automating and Decoupling Your Infrastructure
Designing Storage at Scale
Hosting a New Web Application on AWS
