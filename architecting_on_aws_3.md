# Day 3

## Designing a Web Scaled Storage

Reality of Web based Apps "1 sec delay in page load results in big revenue loss"

# How should web-accessible content be stored?
## 1. Store static assets in s3

s3 consistency model:
Provides ___read-after-write___ consistency for PUTS of new objects
Provides ___eventual consistency___ for overwrite PUTS and DELETES 

    File name can effect performance. s3 hashes first 5/6 characters of key string (<bucket-name>/<key-string>). If your route   folder (s3-logs/May/log.log) where all traffic is going to s3-logs only.  If you create your own hash and prefix it to your key, you will distribute the data of s3-logs accross many machines.
    
    Before:
    s3-logs/May/log.log
    archive/2012

    Result:
    AG43J2/s3-logs/May/log.log
    J67fS2/s3-logs/May/log.log


## 2. Use Caching
* Implement caching on multiple layers. Possible to cache with Cloudfront (CDN Caching)
* **Caching Example:** _The first request checks for the file in the cache (maybe CloudFront). Upon not finding it there, it pulls the file from Amazon S3, stores a copy of the file in the cache at an edge location closest to the user, and then sends another copy to the user who made the request.  Now, when any other users request that file, it's retrieved from the closer edge location in CloudFront, rather than going all the way to Amazon S3 to get it._

### CloudFront CDN Caching
* Your content is cached all over the world at edge locations.  => Lower latencty and good UX
* Less stress on your core infrastructure
* TCP/IP otimizations for the network path
* Keep-alive connections to reduce round trip time (If user is downloading images, it will keep the connection open while the user downloads each image one by one)

Caching BP
* Cache static content / infrequently changing data
* Use cache control headers


## 3. Store non-relational data in a NoSql database.
### DynamoDb BPs
* Keep item size small
* Store metadata in Dynamo and large blobs in S3
* Create sperate tables for day, month, year. Because frequently access tables can be configured differently, hourly table can have 5,000 reads/sec and monthly table with 500 reads/sec
* 

## Well Architected Design Principles
* Stop guessing your capacity needs (Start and then scale up or down as needed)
* Test systems at production scale. (_create a duplicate environments on demand, complete your testing, and then decommission the resources. Because you only pay for the test environment when it is running, you can simulate your live environment for a fraction of the cost of testing on premises._)
* Lower risk of architectural change (duplicate envirnoments, cloud formation, low cost envs, automating)
* Automate to make experimentation easier (Cloudformation) - _Automation allows you to create and replicate your systems at low cost (no manual effort). You can track changes to your automation, audit the impact, and revert to previous parameters when necessary._

# 1. Security
### "Secure your infrastructure Everywhere:" - BPs of Cloud Security
Note: _Tranitional security models focus on securing the perimetre but in cloud you should secure perimetre and between all resources._
* Apply security at all layers - _Instead of just running security appliances (e.g., firewalls) at the edge of your infrastructure, use firewalls and other security controls on all of your resources (e.g., every virtual server, load balancer, and network subnet)._
* Isolate each componenent of your infra
* Encrypt data in transit and in rest
* Enforce access control granularly, using the princincilpe of least privilige
* Use multi-factor authentication
* Log and audit all action and changes of your resources
* Automate your deployments to keep security consistent
* Monitor and automatically trigger responses to event-driven or condition-driven alerts.
* Create and save a custom baseline images (AMI) and use that image automatically on each new (ec2) server you launch.
* Create an entire infrastructure that is defined and managed in a template (CLoud Formation)

## Four areas of security:
#### Data protection: 
Services such as Elastic Load Balancing, Amazon Elastic Block Store (EBS), Amazon Simple Storage Service (S3), and Amazon Relational Database Service (RDS) include encryption capabilities to protect your data in transit and at rest. AWS Key Management Service (KMS) makes it easier for customers to create and control keys used for encryption.
#### Privilege management: 
IAM enables you to securely control access to AWS services and resources. Multi-factor authentication (MFA), adds an extra layer of protection on top of your user name and password.
#### Infrastructure protection: 
Amazon Virtual Private Cloud (VPC) lets you provision a private, isolated section of the AWS cloud where you can launch AWS resources in a virtual network.
#### Detective controls: 
AWS CloudTrail records AWS API calls, AWS Config provides a detailed inventory of your AWS resources and configuration, and Amazon CloudWatch is a monitoring service for AWS resources.

![alt text](https://github.com/joeyfaherty/aws/img/pic.png "Key Services for Security")

## DDoS Attack Mitigation
Prevention strategies
* reduce # of necessary Internet entry point. Eliminate non-critial Internet entry points.
* seperate end user traffic from management traffic
* configure AS and ELBs to automatically scale. __Because ELB only supports valid TCP requests, DDoS aatacks such as UDP and SYN floods are not able to reach your instances.__
* You can set a condition to incrementally add new instances to your AS groups when network traffic is high.
* Cloudfront also has capabilities to filter requests so that only valid TCP and HTTP requests are allowed.
* WAF (Web App Firewall) is a tool which can be used to apply a set of rules to your HTTP traffic, that will filter requests based on data such as IP addresses, HTTP headers, HTTP body, URI strings.

### OAI to only access to your S3 buckets from CloudFront CDN/Cache
        Typically, if you use an Amazon S3 bucket as the origin for a CloudFront distribution, you grant everyone permission to read the objects in your bucket. This allows anyone to access your objects using either the CloudFront URL or the Amazon S3 URL. CloudFront application servers access objects directly from Amazon S3 or if anyone gives out direct links to specific objects in Amazon S3.
        If you want to use CloudFront-signed URLs to provide access to objects in your Amazon S3 bucket, you probably also want to prevent users from accessing your Amazon S3 objects by using Amazon S3 URLs. If users access your objects directly in Amazon S3, they bypass the controls provided by CloudFront-signed URLs, including control over when a URL expires and control over which IP addresses can be used to access the objects. In addition, if users access objects using both CloudFront URLs and Amazon S3 URLs, CloudFront access logs are less useful because they are incomplete.
        You restrict access to Amazon S3 content by creating an origin access identity, which is a special CloudFront user. You change Amazon S3 permissions to give the origin access identity permission to access your objects, and to remove permissions from everyone else. When your users access your Amazon S3 objects using CloudFront URLs, the access objects using Amazon S3 URLs, they are denied access. The origin access identity has permission to access objects in your S3 bucket, but users dont.
        You can create origin access identity using the CloudFront console or the CloudFront API.

#### Encryption
**Public**:
* same key used for encryption and decryption
* performant
* insecure

**Private**:
* 2 keys, diff keys for encrytion and decryption
* no so performant as public
* more secure than public


# 2. Reliability
* **Recovery procedures** - Before a failure occurs, you want to test your recovery procedures. It is important to try to automate recovery as much as possible to reduce the possibility of human error.
* Chaos monkey to similate fail-over and automated recovery process.
* **Monitoring**: By monitoring a system for key performance indicators (KPIs), you can trigger automation when a threshold is breached. This allows for automatic notification and tracking of failures and for automated recovery processes that work around or repair the failure. 
* With more sophisticated automation, it is possible to anticipate and remediate failures before they occur.
* **Auto-Scale** Distribute requests accross multiple small resources to ensure that they dont share a common point of failure.

## Backups:
1. Take backups of all current systems
2. Store backups in s3
3. describe the procedure to restore from backup on AWS
  * know which AMI to use; build your own as needed
  * know how to restore system from backups
  * know how to switch to the new system
  * know how to configure and automate the deployment
### In case of disaster:
1. Retrieve backups from S3
2. Bring up required infra
  * ec2 instance with prepared AMIs, ELBs etc
  * Cloud Formation to automate deployment of core networking
3. Restore system from backup
4. Switch over to the new system.
  * Adjust DNS to point to AWS
  
### Reliability BPs
* Start simple and work upwards
  * backups
  * incrementally improve RTO and RPO as a continuous effort ()
* Excercise your DR solution
  * practice disaster day excercises
  * ensure backups, snapshots, AMIs etc are all properly functionally
  * monitor your monitoring!
  
  
# 3. Performace Effeciency
Cloud
* democratize advanced technologies - _push the complexity of managing services into the cloud vendors domain so that your team can consume the service and focus on product development._
* go gloabl in minutes - lower latency and better UX by maximising features like _multiple regions, edge locations, elbs, autoscaling_
* serverless architecture - 
  * _Deploy an infrastructure without creating or having to patch EC2 instances by using a "serverless" architecture.  A big driver of this is the availability of managed services on AWS such as AWS Lambda and Amazon API Gateway, and regional services like Amazon S3 and Amazon DynamoDB._
  * For example, storage services can act as static websites, thus removing the need for web servers; event services can host your code for you. This not only removes the operational burden of managing these servers, but also can lower transactional costs because these managed services operate at cloud scale.
* experiment more often - quickly carry out comparative testing using different types of instances, storage, or configurations.

## 3.1 Infra Performace
1. evaluate most appropriate instance family and instance type
2. avoid over-provising and under-provisioning
3. change instance types and sizes as your needs change
4. auto-scale by design.  scale horizontally instead of vertically where possible.  Analyze if your application can scale out across multiple ec2 instances by design.
5. Caching. Elasticache - Database layer caching. Works on top of database. (Unline Cloudfront which caches on App Layer for content etc)

How do you select the appropriate instance types, staorage solutions, database solutions, proximity and caching for your system?

Select solutions based on:
1. Predicted resource needs.
2. Required internal governance standards
3. cost/budget
4. benchmarking results
5. load test results

        Amazon EC2 offers a wide selection of instance types optimized to fit different use cases. Instance types are composed of varying combinations of CPU, memory, storage, and networking capacity and give you the flexibility to choose the appropriate mix of resources for your applications. Each instance type includes one or more instance sizes, which allows you to scale your resources to the requirements of your target workload. AWS supports server-less architectures, such as AWS Lambda, that can radically change the performance efficiency of a workload.
        AWS is designed to provide low-cost data storage with high durability and availability. AWS offers storage choices for backup, archiving, and disaster recovery and block, file, and object storage.
        The optimal database solution for a particular system can vary based on requirements for consistency, availability, partition tolerance, and latency. Many systems use different database solutions for different sub-systems and enable different features within them to improve performance. Selecting the wrong database solution and features for a systems workload can lead to lower performance efficiency.
        Physical distance, network distance, or long-running requests can introduce system delays. Unaddressed latency can tie up system resources for longer than required and introduce both internal and external performance degradation. To reduce latency, consider the end- to-end performance of your entire system from the end-users perspective, and look for opportunities to adjust the physical proximity of your resources or cache solutions.

# 4. Cost Optimization
* Region specfic costs
* Spot prices: no more than 10 spot requests at one time. Also have more reties on jobs running on spots.
* burstable instance types.
* Switch off machines 8pm -> 8am 
* AWS "Trusted" Advisor - Tool for suggesting cost improves to make in your aws env
* Snapshots - snapshot -> shutdown -> restore (before report is needed) -> run 
* Caching - lower calls, IOPS etc
* Tools 
  1. Simple Monthly calculator
  2. Billing tab


# 5. 




Certification:
Udemy - Cloud Guru Cert Prep
5 locations in NL for certification

