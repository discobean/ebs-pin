# ebs-pin
Pin EBS volumes to EC2 hosts.
```
pip install ebs-pin
```

## Features

* If EBS volume exists in same AZ as EC2 instance
  * Attaches it
* If a snapshot exists
  * Creates a volume from snapshot and attahces it
* Otherwise, it creates a new volume and attaches it

Also has a method to create snapshots you can place in cron, and is able to tag volumes

## Usage
Attach a new or existing volume
```
ebs-pin attach -h # Help!
ebs-pin attach -u some-arbitrary-static-id --tags Team=DevOps Application=UnDevOpsLikeHost -s 10 -t gp2
```

Snapshot the current attached volume
```
ebs-pin snapshot -h # Help!
ebs-pin snapshot -u some-arbitrary-static-id --tags SnappedTag=ChooseSomething
```

## Thanks to

* This is almost line for line copy of stapler code in Ruby: https://github.com/mikelorant/stapler.git
* A shout out goes to Gonz who thought of it originally: https://github.com/gservat

## Build notes
````
python setup.py sdist
twine upload dist/*
````
