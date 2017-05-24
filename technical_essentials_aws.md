**_TODO: tidy up file and add more details from notes........... 7/12/16_**

**EC2** - virtual machine

**AWS Lambda** - Run your small script on aws.
Doesn't care about os or layers underneath. Used for talking to other aws services, api calls.

**IAM** - Identity and Access Management - Security groups and roles.

**Regions**:
Ireland, London, Frankfurt. All data centres in secret locations.  

.......There is no cloud actually!!
Choose a site close to your customers fo lower latency, if you have German customers, use the frankfurt region.

At least 2 availability zones per region.
Always triple replicate to 3 AZ's.

DNS - Route 53 - 

Management console

Never get access to the amazon machines themsleves.
Only access to the bastian hosts.

public IP ... one bastian host with a public IP, where you can then reach the rest of your aws services via their internal IP's.

CLI possible to get instances info. You need to install CLI and keys for it to work.
Access Key 
Secret Key

# Module 2: Layout

**EC2** (virtual machine) - Elastic compute cloud
* Resizeable compute capacity
* Control over your resources
* Choose linux or windows (if you choose windows, then you need to pay for licences, same for redhat, centos is free)
* pay only for capacity you use

1 - Pick region
2 - Launch
3 - Choose instance type
4 - 

### **Instances and ami**

* ami is based on: region, os, archictecture (32/64 bit), launch permissions, storage for the root device
* Always deploy to multi AZ's.. usually handled by autoscaling groups.
* EC2 instance types (many different families).
* Start with M4 (General purpose), if this doesnt fit your needs, upgrade.
* X1 instance: -> 2TB memory! This is the highest spec.
* T family, affordable. But its burstable, good for spikey stuff, not for constant high load.
* selec2or.info -> site for camparing ec2 memory and cpu
* ami + user data script = machine with everything configured installed.
* script can then be in version control for automated deployments.
* instances should be throw awayable.. redeploy with updated script if any issue.
 
### Payments

On demand; 
Pay for instances by the hour.
Reserved instances:
1 -3 years. always on.

#### Spot instances; 
**difference between spot market price and on demand price is HUGE**
If your app is not a web service, (can be occasionally terminated), then you will save huge cash 
by going on a highest bidder using the spot price where you will be 90% running (but possibly terminated)

## VPC - Virtual Private Cloud

private network in frankfurt, safely in their own network.
vpn only subnet - db server 
not accessible from internet - private subnet - back-ends, app server etc
accessible from public internet - public subnet - web server
Youtube video: a day in the life of 1M packets

#### VPC security groups:

webserver talks to app server that talks to sb server, web server cant talk directly to db server -> this is security froups
vpc with single public subnet
Your instances run in a private, isolated section of the AWS cloud with direct access to the Internet. Network access control lists and security groups can be used to provide strict control over inbound and outbound network traffic to your instances.

Creates:
A /16 network with a /24 subnet. Public subnet instances use Elastic IPs or Public IPs to access the Internet.
vpc with public & private subnets:
In addition to containing a public subnet, this configuration adds a private subnet whose instances are not addressable from the Internet. Instances in the private subnet can establish outbound connections to the Internet via the public subnet using Network Address Translation (NAT).

Creates:

A /16 network with two /24 subnets. Public subnet instances use Elastic IPs to access the Internet. Private subnet instances access the Internet via Network Address Translation (NAT). (Hourly charges for NAT devices apply.)
SSL endpoints
Security groups can refer to each other, this minimises the need to refer to other hosts by IP.

Dynamo DB -> No sql key value DB.
EC2 -> VPC -> Dynameo
VM  -> Network -> DB service
Roles -> add signed keys

Roles (instance profiles) are always created when the ec2 is created. Cannot add roles at a later stage.

IAM Authentication & Authorization

Deny policies override other admin policies that allow access to everything

Module 4:

Databases:

DynamoDB

Amazon RDS (postgres, oracle, mariadb) -> relational -> it is actually a aws machine with an os and the actual postgres installed.  

RDS:

simple and fast to deploy

manages most db admin tasks

fast to scale

cost effective

Snapshots stored in S3.

  ELB

App  App

   DB

S3 backups

DynamoDb:

store any amount of data with no limits

fast, predictable performance using SSD's

Triad of services:

          ELB

Autoscaling CLoudwatch

ELB distributes traffic across ec2 machines across multiple AZ's

Autoscaling:

- fault tolerant

- better availability

- cost effective

minimum, desired, maximum.

Uses cloud watch metrics to determine if an autoscaling group should start new/terminate old instances.

terminates instances (doesnt stop them), then it starts NEW containers, not starts existing ones.

launch configuration -> roles, subnet, sec groups etc
