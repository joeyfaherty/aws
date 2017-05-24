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
* Stop guessing your capacity needs
* 
* Lower risk of architectural change (duplicate envirnoments, cloud formation, low cost envs, automating)
* Automate to make experimentation easier (Cloudformation)
* 
* 

