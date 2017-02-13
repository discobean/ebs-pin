import time, logging

class Ec2:
    session = None
    client = None

    def __init__(self, session):
        self.session = session
        self.client = self.session.client('ec2')

    def get_latest_volume_id_available(self, uuid):
        filters = [
                { "Name": 'tag-key',   "Values": [ 'UUID' ] },
                { "Name": 'tag-value', "Values": [ uuid ] }
            ]
        try:
            volumes = self.client.describe_volumes(Filters=filters)['Volumes']
            volumes = sorted(volumes, key=lambda ss:ss['CreateTime'])
            volume = [x for x in volumes if x['State'] == 'available'].pop()
            return volume['VolumeId']
        except:
            return None

    def get_latest_snapshot_id(self, uuid):
        filters = [
                { 'Name': 'tag-key',   'Values': ['UUID'] },
                { 'Name': 'tag-value', 'Values': [ uuid ] },
                { 'Name': 'status',    'Values': ['completed'] }
            ]

        try:
            snapshots = self.client.describe_snapshots(Filters=filters)['Snapshots']
            snapshot = sorted(snapshots, key=lambda ss:ss['StartTime']).pop()
            return snapshot['SnapshotId']
        except:
            return None

    def get_instance_name(self, instance_id):
        filters = [
                { "Name": 'resource-id', "Values": [ instance_id ] },
                { "Name": 'key',         "Values": [ 'Name' ] }
            ]

        try:
            result = self.client.describe_tags(Filters=filters)['Tags'][0]['Value']
            return result
        except:
            return None

    def get_volume_id(self, volume_id):
        pass

    def get_volume_name(self, volume_name):
        pass

    def get_volume_region(self, volume_id):
        try:
            return self.client.describe_volumes(VolumeIds=[volume_id])['Volumes'][0]['AvailabilityZone']
        except:
            return None

    def create_volume(self, size, volume_type, availability_zone, snapshot_id=None):
        try:
            if snapshot_id:
                response = self.client.create_volume(
                    Size=size,
                    SnapshotId=snapshot_id,
                    AvailabilityZone=availability_zone,
                    VolumeType=volume_type
                )
            else:
                response = self.client.create_volume(
                    Size=size,
                    AvailabilityZone=availability_zone,
                    VolumeType=volume_type
                )

            max = 12
            num = 0
            while True:
                if num >= max:
                    break

                state = self.client.describe_volumes(VolumeIds=[response['VolumeId']])['Volumes'][0]['State']

                if state != 'available':
                    time.sleep(5)
                    num += 1
                    continue

                return response['VolumeId']
        except:
            logging.exception("Failed to create volume")
            return None


    def create_snapshot(self, volume_id):
        pass

    def tag_volume(self, volume_id, volume_name, options):
        try:
            tags = [
                    { 'Key': 'Name',         'Value': volume_name },
                    { 'Key': 'Application',  'Value': None },
                    { 'Key': 'Environment',  'Value': None },
                    { 'Key': 'Team',         'Value': None },
                    { 'Key': 'UUID',         'Value': options.uuid },
                    { 'Key': 'SnapInterval', 'Value': options.interval },
                    { 'Key': 'Detached',     'Value': str(not options.nopreserve).lower() }
                ]

            tags = [x for x in tags if x['Value'] is not None]

            return self.client.create_tags(
                    Resources=[ volume_id ],
                    Tags=tags
                )
        except:
            logging.exception("Failed to create tags")
            return None


    def tag_snapshot(self, snapshot_id, tags):
        pass

    def attach_volume(self, volume_id, instance_id, device):
        try:
            response = self.client.attach_volume(
                VolumeId=volume_id,
                InstanceId=instance_id,
                Device=device
            )

            max = 12
            num = 0
            while True:
                if num >= max:
                    break

                try:
                    state = self.client.describe_volumes(VolumeIds=[volume_id])['Volumes'][0]['Attachments'][0]['State']
                except:
                    logging.exception("Error getting state")

                if state != 'attached':
                    time.sleep(5)
                    num += 1
                    continue

                return volume_id
        except:
            logging.exception("Failed to mount volume")
            return None
