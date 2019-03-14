# ebs-pin
Pin EBS volumes to EC2 hosts.
```
pip install ebs-pin3
```

Previous versions for 2.7 are available as
```
pip install ebs-pin
```

## Features

* If EBS volume exists in same AZ as EC2 instance
  * Attaches it
* If volume exists in another AZ, then
  * Creates a volume from snapshot and attaches it
* Otherwise, it creates a new volume and attaches it

Also has a method to create snapshots you can place in cron, and is able to tag volumes

## Usage
Attach a new or existing volume
```
ebs-pin attach -h # Help!
ebs-pin attach -u some-arbitrary-static-id -d /dev/xvdf -s 10 -t gp2 --tags Team=DevOps Application=UnDevOpsLikeHost
```

Snapshot the current attached volume
```
ebs-pin snapshot -h # Help!
ebs-pin snapshot -u some-arbitrary-static-id --tags SnappedTag=ChooseSomething
```

## Thanks to

* This is almost line for line copy of [stapler](https://github.com/mikelorant/stapler.git) code in Ruby
* A shout out goes to [Gonz](https://github.com/gservat) who thought of it originally

## Build notes
To build and upload
````
make upload
````

## TODO

* Check if already mounted before attempting to run again
* Delete old snapshot once snapshot succeeds, keep X snapshots
