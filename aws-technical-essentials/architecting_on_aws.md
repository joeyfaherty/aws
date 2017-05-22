ebooks and lab guides:
https://evantage.gilmoreglobal.com/#/

Day 1

Module 1; Core AWS Knowledge/Services
Cloud Advantages

one
two
eliminate guessing on your capacity needs(new app, popular?)
speed and agility (beanstalk)
no more data centre costs
go global in minutes (web app CDN to make your app available globally)

note:
rds.. will always be running, so do not over spec machine in the beginning, always spec for the present and change in future as needed to keep costs in check.

AWS data centres are always hot (always on) so resources are always available immediately to customers

Availability Zones:
made up of one or more data centres
designed for fault isolation
interconnected with other AZs using high speed private links.

note: always design your app with more than one AZ for fault tolerence.

Regions:
each region is made up of 2 or more AZs
AWS has 12 regions worldwide
You control data replication across regions.
communication between regions uses public internet infrastructure.

Edge locations
Locations used for caching
Route 53 routing is used 

Unmanaged vs managed services
Fault tolerence, Scaling, Availability managed by cloud provider. Otherwise you manage this!

Shared responsibility model
your responsibilities: 
aws account
user access, role-based access
aws services used by customer

instance os: patching, maintanence
app: passwords, role-based access
security groups
network config / firewall

aws responsibilities:
hardware, software, network (updates, patching, instance isolation)
aws data centres

Use case 1:
The weather company, 4GB of data sent per second
handles 150,000 API calls per second

BP1
Enable Scalability - ensure that your architecture can handle changes in demand. (scala up/down, monitoring,)
BP2
Automate your env - remove manual processes to improve your systems staability and consistency (cloud formation, config etc)
BP3
Use disposable resources - think of servers and other components as ephemeral (backup, external staores etc)
BP4
Loosly couple your components - reduce interdependencies so that the change or failure of one component does not affect other components
BP5
Design services, not servers
Managed services and serverless architecures can provide greater reliability and efficientcy in your env
BP6
Choose the right database solutions - match the technology to the workload (RDS, NoSql, Kinesis, DWH, Elastic search AWS)
BP7
Avoid single points of failure (HA) - Implement redundency where possible..
BP8
Optimize for cost - resources are sized appropriately, scaling in and out based on need, and that you take advanatge of different price ranges (spot price, glacier)
BP9
Use caching - Use caching to minimize redundant data retrieval operations (caching with cloudfront)

person -> cloudfront -> ?

BP10
Secure your infrastructure at every layer - 


Module 2 - AWS Services

VPC - By default each VPC is isolated  from other virtaul networks
EC2s are launched into a VPC, since 2013
VPC key features are configuarbale;
IP range
subnets
routing
network gateways
security settings (security groups [firewalls] etc)

Each VPC lives in only one region.
You can have multiple VPCs in same account (dev, test, prodVpc) or (salesVpc, ItVpc)
You need to pick AZ it will be in (should be multiple for HA)

EC2
elastic compute cloud
most os supported
create, save, resue your own sever images (AMI's)
launch one at a time, or launch a whole fleet
add more instances as you need, terminate when no longer required

Instance Specs
spec templates can be selected (general purpose, graphics, memory, storage etc)
Site to check different specs: http://selec2or.info/ 
Monthly calculator AWS: http://calculator.s3.amazonaws.com/index.html
scale-up vs scale-out
less higher spec machines vs many lower spec machines
Burstable
t2 (only this instance type is burstable): uses only 10% or 20% cpu, you will save credits built up per hour, then can be used to "burst" to 100% for a specific time, after this time it will automatically reduce to the 10% cpu threshold.

Pricing:
On demand instances - pay as you go,
use case: short term, spikey, app dev or testing

reserved instances - one year or 3 years, lower cost, subscription based you pay even if you dont use (same as gym!)
use case: steady predictable workloads, disaster recovery

spot instances - bid on instance type, instance lost if you are outbid
use case: apps with flexible start and end times, apps only feasible as very low compute prices, users with urgent computing need for large amounts of additional capacity.
If the day price goes above your bid price, your instance will be terminated with a 2 min warning.
note: 2 min warning, react on this 2 minute warning to store tmp data etc
Note bp: big below demand price but more than usual spot price, you will mostly have your instance paying bid price but will lose it only on spikes :)

Block Storage vs object storage
EBS
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

EBS Volume Types
GP SSD: 3 IOPS/GB , MAX 10,000 IOPS
Provisioned IOPS SSD: MAX 20,000 IOPS


S3 
Available publicly by URL
durability: 9s
availability: 4 9s
availabilty: data is still there (durability sla passed) but its not available (by URL etc)
SLA: if sla is not met, credits are issued depending on percentage to user
Virtually unlimited in size (max size is 5tb for one object upload)
s3://region-code.amazonaws.com/<bucket-name>/<key>
There are no folder structures in s3, its just park of the key!
Can have an event triggered on any upload, edit of object into s3. (send email notification etc)

Cost:
Uploads - free
Pay for - transfer out to other regions, PUT, GET, COPY etc
General Purpose: s3 standards
Infrequent access - can be automated based on rules
Glacier - extremely low cost, takes up to 5hrs to access. (Extremely low cost hardware is used where speed is not essential) (keeping invoices for 10 year period for audit (NL Law))

s3 -> infreq -> glacier -> delete (configurable per bucket)



















Designing Your Environment
Making Your Environment Highly Available
Forklifting an Existing Application onto AWS
    
    
Hello

Day 2

Event-Driven Scaling
Automating and Decoupling Your Infrastructure
Designing Storage at Scale
Hosting a New Web Application on AWS

Day 3

The Four Pillars of the Well-Architected Framework
Disaster Recovery and Failover Strategies
Troubleshooting Your Environment
Large-Scale Design Patterns and Case Studies
