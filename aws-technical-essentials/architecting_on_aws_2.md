## Day 2
---
[aws certification](https://d0.awsstatic.com/training-and-certification/docs-sa-assoc/AWS_certified_solutions_architect_associate_blueprint.pdf) 

### Network Access Control List (NACL)
* Stateless firewall
* Works on subnet level
* Automatically allows outgoing traffic
* Add rule priority in increments of 50 or 100

### Security group
* Stateful firewall
* Works on instance level
* Ability to define security groups as a source (this is useful for multi-tier applications, where you want the app server only in communication with the db server on a specific port and nothing else)
* When creating rds instances, you are asked if you would like a security group for this, as it usually will only allow traffic to your app servers

### Connecting to an on premise network
* Side to side VPN - CGW-VPN
* AWS Direct Connect - doesnt use internet, uses private network connections. You need to work with telecommunications provider to get this.




Making Your Environment Highly Available
Forklifting an Existing Application onto AWS

Event-Driven Scaling
Automating and Decoupling Your Infrastructure
Designing Storage at Scale
Hosting a New Web Application on AWS
