[ebooks and lab guides](https://evantage.gilmoreglobal.com/#/)

# Day 1
## Module 1: Core AWS Knowledge/Services
---
### Cloud Advantages
* one
* two
* eliminate guessing on your capacity needs(new app, popular?)
* speed and agility (beanstalk)
* no more data centre costs
* go global in minutes (web app CDN to make your app available globally)

#### BP:
rds.. will always be running, so do not over spec machine in the beginning, always spec for the present and change in future as needed to keep costs in check.

AWS data centres are always hot (always on) so resources are always available immediately to customers

### Availability Zones:
made up of one or more data centres
designed for fault isolation
interconnected with other AZs using high speed private links.

#### BP:
always design your app with more than one AZ for fault tolerence.

### Regions:
each region is made up of 2 or more AZs
AWS has 12 regions worldwide
You control data replication across regions.
communication between regions uses public internet infrastructure.

### Edge locations
Locations used for caching
Route 53 routing is used 

### Unmanaged vs managed services
Fault tolerence, Scaling, Availability managed by cloud provider. Otherwise you manage this!

### Shared responsibility model
#### your responsibilities: 
aws account
user access, role-based access
aws services used by customer

instance os: patching, maintanence
app: passwords, role-based access
security groups
network config / firewall

#### aws responsibilities:
hardware, software, network (updates, patching, instance isolation)
aws data centres

### Use case 1:
* The weather company, 4GB of data sent per second
* handles 150,000 API calls per second

#### BP1
* Enable Scalability - ensure that your architecture can handle changes in demand. (scala up/down, monitoring,)
#### BP2
* Automate your env - remove manual processes to improve your systems staability and consistency (cloud formation, config etc)
#### BP3
* Use disposable resources - think of servers and other components as ephemeral (backup, external staores etc)
#### BP4
* Loosly couple your components - reduce interdependencies so that the change or failure of one component does not affect other components
#### BP5
* Design services, not servers
* Managed services and serverless architecures can provide greater reliability and efficientcy in your env
#### BP6
* Choose the right database solutions - match the technology to the workload (RDS, NoSql, Kinesis, DWH, Elastic search AWS)
#### BP7
* Avoid single points of failure (HA) - Implement redundency where possible..
#### BP8
* Optimize for cost - resources are sized appropriately, scaling in and out based on need, and that you take advanatge of different price ranges (spot price, glacier)
#### BP9
* Use caching - Use caching to minimize redundant data retrieval operations (caching with cloudfront)
* person -> cloudfront -> ?

#### BP10
* Secure your infrastructure at every layer - 

## Module 2 - AWS Services
* VPC - By default each VPC is isolated  from other virtaul networks
* EC2s are launched into a VPC, since 2013
* VPC key features are configuarbale;
* IP range
* subnets
* routing
* network gateways
* security settings (security groups [firewalls] etc)

Each VPC lives in only one region.
You can have multiple VPCs in same account (dev, test, prodVpc) or (salesVpc, ItVpc)
You need to pick AZ it will be in (should be multiple for HA)

### EC2
elastic compute cloud
most os supported
create, save, resue your own sever images (AMI's)
launch one at a time, or launch a whole fleet
add more instances as you need, terminate when no longer required

### Instance Specs
spec templates can be selected (general purpose, graphics, memory, storage etc)
Site to check different specs: http://selec2or.info/ 
Monthly calculator AWS: http://calculator.s3.amazonaws.com/index.html
scale-up vs scale-out
less higher spec machines vs many lower spec machines
Burstable
t2 (only this instance type is burstable): uses only 10% or 20% cpu, you will save credits built up per hour, then can be used to "burst" to 100% for a specific time, after this time it will automatically reduce to the 10% cpu threshold.

### Pricing:
On demand instances - pay as you go,
use case: short term, spikey, app dev or testing

#### reserved instances - 
one year or 3 years, lower cost, subscription based you pay even if you dont use (same as gym!)
use case: steady predictable workloads, disaster recovery

#### spot instances - 
bid on instance type, instance lost if you are outbid
use case: apps with flexible start and end times, apps only feasible as very low compute prices, users with urgent computing need for large amounts of additional capacity.
If the day price goes above your bid price, your instance will be terminated with a 2 min warning.

#### BP: 
2 min warning, react on this 2 minute warning to store tmp data etc
#### BP: 
big below demand price but more than usual spot price, you will mostly have your instance paying bid price but will lose it only on spikes :)

### Block Storage vs object storage
#### EBS
Only available from within the machine (unlike publicly available s3)
volumes are auto replicated with its AZ
can be auto backed up in s3
can now resize an EBS volume (previously has to create new and copy data across)
uses:
boot volumes and storage for ec2 instances
data storage with a file system
database hosts
enterprise apps

Instance store in inside host of ec2, so when shut down data is lost.
EBS is outside host of ec2, so this data volume will not be lost on shutdown.
EBS can only be linked to one ec2 instance, cannot be shared to more than one ec2 instance.

### EBS Volume Types
GP SSD: 3 IOPS/GB , MAX 10,000 IOPS
Provisioned IOPS SSD: MAX 20,000 IOPS


### S3 
Available publicly by URL
durability: 9s
availability: 4 9s
availabilty: data is still there (durability sla passed) but its not available (by URL etc)
SLA: if sla is not met, credits are issued depending on percentage to user
Virtually unlimited in size (max size is 5tb for one object upload)
s3://region-code.amazonaws.com/<bucket-name>/<key>
There are no folder structures in s3, its just park of the key!
Can have an event triggered on any upload, edit of object into s3. (send email notification etc)

### Cost:
Uploads - free
Pay for - transfer out to other regions, PUT, GET, COPY etc
General Purpose: s3 standards
Infrequent access - can be automated based on rules
Glacier - extremely low cost, takes up to 5hrs to access. (Extremely low cost hardware is used where speed is not essential) (keeping invoices for 10 year period for audit (NL Law))

s3 -> infreq -> glacier -> delete (configurable per bucket)


## Databases

### RDS
Managed service, scalable, automated redundancy and backup available
db engines Aurora, mysql, oracle, prostgres, mariadb, sql server
use cases:
complex transactions or complex queries
a medium-to-high query/write up to 30K IOPS
lots of cols per table

not use cases:
massive read/read orates ie 150K per sec
storing simple table with few columns, massive amounts of rows/records

### Dynamo DB
Read capacity unit:
one **strongly consistent** read per second for items as large as 4kb (twice as much as eventually consistent read)
two **eventually consistent** reads per second for items as large as 4kb

one write per second
one write per second for items as large as 1kb.

Configure tables based on which tables are accessed and written to more frequently.

RDS is always on. But if you only use RDS for processing for 8hrs/day, then you can enable snapshots. Essentially this terminates the instance and restores before your 8 hour window commences, and then after the job is done, we can terminate the instance again to reduce cost. (instance is running 8hr/day instead of 24hrs/day).

### AWS IAM
Your responsibility
Create users, roles, groups for access 

Link policy to a user or group.

Example; App is running on ec2 instance and needs access to s3, instead of having credentials hardcoded in app, combine all permissions into a role, and link it to the instance. Then anything running within the instance will have access to this role.

Role: combination of different policies:
Link a role to a machine.** do it

Link a role to a user

#### Cross account access:
Permission set up in titan account
multi-screen account go to switch role, fill in titan account number, you will then switch to this role.

### Security crentials
email address + paswword - associated with your AWS account (root)
IAM user name and password - AWS managenment console
Access Keys - CLIs , APIs
Multi-factor authentication - extra security layer
Key pairs - only available of specific service like ec2

Root account should only be used once to create a admin account
admin account then used for day to day admin 


All permissions are denied by default
If something is explicity denied, it cannot be allowed.

#### BP1
Follow the least priviledge principle

#### IAM Policies
formal statement of one or more permissions
attached to any user, group, role
Policies - set of permissions - access to s3, write to a table - stored as json file, resource, allow/deny, start/stop




#### IAM Users
you create users
no default 

#### IAM groups
cannot be nested
no default groups
collection of iam users

#### IAM Roles

#### Use cases
provide aws resources with access to aws services
only one role per user at a time (admin, CFO_Billing)
Switch roles to access resources
- in your account
- another account (cross account access)

AWS Cloudtrail - leaves a trail of all API request by each user, SDK, CLI everything logged. (security monitoring)
AWS Config (Combined with Cloudtrail) - Service that allows you to record a resource (cost) and monitor all changes done to your configuration. On management console you can filter by resources and see config changes.

AWS Cost and Usage Report - 

#### EC2 Best Practices
1 seperate roles
devs -> dev access
admin -> admin access

2 minimum privlidges needed

3 

EC2 storage
deleted when instance terminated
more..

Resource Management
Instance metadata - instance id, instance type
Tags...




## Designing Your Environment
1
2 Latency.. How close is the region to your users. When you pick a region, you pick one close to you (Ireland, Franfurt)
3 Not all services (or a feature of a service) are available in all regions (new regions take time to expand DS) (lamba)
4 How many AZs? (If a requirement is to have 3 AZs, then you need to pick a region with 3 AZs [default is 2 AZs per region])

How many AZs should you use? BP*
Start with 2 AZs per region.
Using more than 2 AZs for HA is not usually cost effective.le applications managed by one person or very small team

- Spot prices not available for +2 AZs
- DB servers usually use active/passive architecture

How many VPCs?

One VPC
limited use cases for one VPC:
high performance computing
identity management
small, single apps managed by one person or small team

#### Multiple VPCs (each account will always be in in its own vpc)
dev account, test account, prod account

#### Multi-VPC Pattern
uses one aws account
uses 2 or more VPCs

#### Multi-account pattern




VPC CIDR Block
Range of IPs, always make it big enough to cope with future growth, as you cannot modify once created

How should you divide your VPCs into subnets?

Subnet -> aka SubVPC. Will have a smaller range cidr block. This is also not changeable
Each subnet will have its own IP.
Subnets are private by default.
To create a public subnet => in route table add 10.0.0.0/16 => local and 0.0.0.0/0 => internet gateway
Note:
S3, Dynamo are not part of your VPC, publically available (public internet)
RDS etc are within your VPC

#### Routing table: 
Create a VPC endpoint so that you can internally call s3 without going through public internet. How?
Create a VPCEP by adding an entry into your routing table with the public IP of your s3 machine.

DNS
.0 network address
.1 default gateway
.2 internal dns/dhcp
.3 reserved
.255 broadcast

#### bastion host / jump box:
how can a private subnet access public internet?  Access a bastion host (which is in a public subnet) 
bastion host should be set to a limited range of IPs or just your own IP.

#### BP
Start with one public and one private subnet.

Private
db, batch processing instances, back-end instances
Web app
public or private

#### How do you control VPC traffic








Snapshots BP: Should be taken from a shutdown machine. (But this is not always possible)
If its taken from a running machine, you have no guarantee that it is in a consistent state.




## Making Your Environment Highly Available
## Forklifting an Existing Application onto AWS

# Day 2

## Event-Driven Scaling
## Automating and Decoupling Your Infrastructure
## Designing Storage at Scale
## Hosting a New Web Application on AWS

# Day 3

## The Four Pillars of the Well-Architected Framework
## Disaster Recovery and Failover Strategies
## Troubleshooting Your Environment
## Large-Scale Design Patterns and Case Studies
