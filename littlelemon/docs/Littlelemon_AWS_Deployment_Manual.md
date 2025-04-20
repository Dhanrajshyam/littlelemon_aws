Little Lemon Restaurant AWS Deployment Setup - Manual:

AWS Architecture:
AWS Cloud
├── VPC
│   ├── Internet Gateway
│   ├── Public Subnet
│   │   └── EC2 (Caddy Reverse Proxy + HTTPS)
│   └── Private Subnet
│       └── ECS Task (Django container pulled from ECR)
├── RDS (PostgreSQL, Free Tier)
├── S3 + CloudFront (Static files CDN)


S3 + CloudFront (Static files CDN) Setup:

S3 Storage:
Bucket Name: littlelemon-static-file-storage-s3
	Settings:
		ACLs disabled - All objects in this bucket are owned by this account. Access to this bucket and its objects is specified using only policies.
		Block all public access - set - only private from current AWS account instances or users.
		Bucket Versioning - Disable
		Tags - optional - None
		Default encryption - Encryption type : Server-side encryption with Amazon S3 managed keys (SSE-S3) | Bucket Key : Enable
		Advanced settings - Object Lock : Disable
		Bucket Policy:
			{
				"Version": "2008-10-17",
				"Id": "PolicyForCloudFrontPrivateContent",
				"Statement": [
					{
						"Sid": "AllowCloudFrontServicePrincipal",
						"Effect": "Allow",
						"Principal": {
							"Service": "cloudfront.amazonaws.com"
						},
						"Action": "s3:GetObject",
						"Resource": "arn:aws:s3:::littlelemon-static-file-storage-s3/*",
						"Condition": {
							"StringEquals": {
								"AWS:SourceArn": "arn:aws:cloudfront::593005978575:distribution/E1MVJS8GXW8L9N"
							}
						}
					}
				]
			}

CloudFront: Content Delivery Network
Domain Name: d3j5vedw5h2qdm.cloudfront.net
Name: littlelemon-static-file-storage-s3.s3.ap-south-1.amazonaws.com
	Settings:
		Origin domain: littlelemon-static-file-storage-s3.s3.ap-south-1.amaz: 10 | The number of seconds that CloudFront waits when trying to establish a connection to the origin, from 1 to 10. The default is 10.onaws.com
		Origin access: Origin access control settings (recommended) | Bucket can restrict access to only CloudFront.
		Origin access control: 
			Name: S3-OAC-for-StaticFiles
			Signing behavior: Always
			Origin type: S3
		Add custom header - optional:
		Enable Origin Shield: No
		Connection attempts: 3 | The number of times that CloudFront attempts to connect to the origin, from 1 to 3. The default is 3.
		Connection timeout: 10 | The number of seconds that CloudFront waits when trying to establish a connection to the origin, from 1 to 10. The default is 10.:
		
		Default cache behavior:
			Path pattern: Default (*)
			Compress objects automatically: Yes
			Viewer protocol policy: HTTP and HTTPS
			Allowed HTTP methods: GET, HEAD
			Restrict viewer access: No | If you restrict viewer access, viewers must use CloudFront signed URLs or signed cookies to access your content.
			Cache key and origin requests: Cache policy and origin request policy (recommended)
		
		Web Application Firewall (WAF): Do not enable security protections
		
		Settings:
			Price class: Use North America, Europe, Asia, Middle East, and Africa
			Supported HTTP versions: HTTP/2
			IPv6: On
		
		Standard logging :
			Log delivery: Off | Additional charges may apply. See Info for more details.

# CDN (Cloudfront + S3) Setup Verification:

http://d3j5vedw5h2qdm.cloudfront.net/littlelemon/static/img/photos/restaurant_inside.jpg - HTTP request verified and working
https://d3j5vedw5h2qdm.cloudfront.net/littlelemon/static/img/photos/restaurant_inside.jpg - HTTPS request verified and working

 
RDS (PostgreSQL, Free Tier) Setup:

Amazon Relational Database Service (RDS):
Endpoint: littlelemon-postgres-db.crwcskgw0tvi.ap-south-1.rds.amazonaws.com
Create database 
	Choose a database creation method: Standard create
	Engine options: Engine type: PostgreSQL
	Engine version: PostgreSQL 17.2-R2
	Templates: Free Tier
	
	Availability and durability
		Deployment options: Single-AZ DB instance deployment (1 instance
	
	Settings
		DB instance identifier: littlelemon-postgres-db
	
	Credentials Settings
		Master username: postgres
		Credentials management: Self managed
		Auto generate password: Enabled | You can view your credentials after you create your database. Click the 'View credential details' in the database creation banner to view the password.
		Password: e9K0wPDWJ9mPllCsX5nV
	
	Instance configuration
		Burstable classes (includes t classes): db.t4g.micro (2 vCPUs | 1 GiB RAM | Network: Upto 2,085 Mbps)
	
	Storage
		Storage type: General Purpose SSD (gp2)
		Allocated Storage: 20 GiB
		
	Connectivity
		Compute resource: Don’t connect to an EC2 compute resource | Don’t set up a connection to a compute resource for this database. You can manually set up a connection to a compute resource later.
		Network type: IPv4
		Virtual private cloud (VPC): Default VPC (vpc-08cda0d54129b3978) | 3 Subnets and 3 Availability Zones. | After a database is created, you can't change its VPC.
		DB subnet group: default
		Public access: No
		
	VPC security group (firewall)
		New VPC security group name: littlelemon-vpc
		Availability Zone: ap-south-1a
		Certificate authority - optional: rds-ca-rsa2048-g1 (default) | Expiry: May 20, 2061
		Database Port: 5432
			
	Database authentication
		Database authentication options: Password and IAM database authentication
			
	Monitoring 
		Database Insights - Standard | Retains 7 days of performance history, with the option to pay for the retention of up to 24 months of performance history
	
	DB parameter group: default.postgres17
	
	Backup
		Enable automated backups: Enabled | Creates a point-in-time snapshot of your database
		Backup retention period: 1 Day
		Backup window: No Preference | The daily time range (in UTC) during which RDS takes automated backups.
		Copy tags to snapshots: Enabled
		Backup replication: Disabled
	
	Encryption: Enabled | Choose to encrypt the given instance. Master key IDs and aliases appear in the list after they have been created using the AWS Key Management Service console
		AWS KMS Key: (default) aws/rds
		Account: 593005978575
		KMS key ID: alias/aws/rds
	
	Maintenance
		Enable auto minor version upgrade: Disabled | Enabling auto minor version upgrade will automatically upgrade your database minor version. For limitations and more details, see Automatically upgrading the minor engine version
	
	Maintenance window:
		No Preference | Select the period you want pending modifications or maintenance applied to the database by Amazon RDS.
		
	Deletion protection
		Enable deletion protection: Enabled | Protects the database from being deleted accidentally. While this option is enabled, you can’t delete the database.
		
		
Virtual Private Cloud Setup:
	VPC ID: vpc-08cda0d54129b3978acl-09d8f995d7d37c574
	Default VPC: Yes
	State: Available
	Block Public Access: Off
	DNS hostnames: Enabled
	DNS resolution: Enabled
	Tenancy: Default
	DHCP option set: dopt-0eccffbfaa397b0f2
	Main route table: rtb-0777726db0657d7d5
	Main network ACL: acl-09d8f995d7d37c574
	Default VPC: Yes
	IPv4 CIDR: 172.31.0.0/16
	Network Address Usage metrics: Disabled
	Owner ID: 593005978575
	
	Subnets(3):
		ap-south-1a: subnet-09b7af2c646c62dff | 172.31.32.0/20
		ap-south-1b: subnet-0b6188f1fe7fc417a | 172.31.0.0/20
		ap-south-1c: subnet-03f46829daad8cd62 | 172.31.16.0/20
		
		Route Tables:
			rtb-0777726db0657d7d5
			
			Network Connections
				igw-082e9b75ba21ecddd


Security Groups:
	Reverse Proxy: Caddy
	Security group name: littlelemon-sg-caddy
	Security group ID: sg-0029e6c7e1bf0ed56
	Description: Allow External or Public users to Access the reverse proxy server on EC2
	VPC ID: vpc-08cda0d54129b3978
	Owner: 593005978575
		
		Inbound rules:
			Name	| Security group rule ID	| IP version	| Type	| Protocol	| Port range	| Source			| Description

			–		| sgr-0345cea5da4956926		| IPv4			| SSH	| TCP		| 22			| 49.37.215.132/32	| –
			–		| sgr-092aa4b22cbdd270c		| IPv4			| SSH	| TCP		| 80			| 0.0.0.0/0			| Allow public access
			–		| sgr-0b25078763c43ac82		| IPv4			| SSH	| TCP		| 443			| 0.0.0.0/0			| Allow public access


		

