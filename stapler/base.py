import boto3, logging, sys
import ec2

class Base:
    options = None
    metadata = None
    session = None
    ec2 = None

    def __init__(self, options, metadata):
        self.options = options
        self.metadata = metadata
        self.session = boto3.Session(region_name=metadata['region'])
        self.ec2 = ec2.Ec2(self.session)

    def attach(self):
        #name = ec2.get_instance_name(metadata[:instanceId]) || metadata[:instanceId]
        name = self.ec2.get_instance_name(self.metadata['instanceId']) or self.metadata['instanceId']
        volume_name = "%s-%s" % (name, self.options.device)
        logging.info("Volume name: %s" % volume_name)

        logging.info("Finding volume...")

        volume_id = self.ec2.get_latest_volume_id_available(self.options.uuid)
        if volume_id:
            logging.info("Volume found: %s" % volume_id)
            logging.info("Checking volume is in same availability zone as instance...")
            if self.ec2.get_volume_region(volume_id) != self.metadata['availabilityZone']:
                logging.info("Volume in another availability zone, snapshot required.")
                """
                if (snapshot_id = ec2.create_snapshot(volume_id))
                    puts "Snapshot created: #{snapshot_id}"
                    volume_id = nil
                end
                """
        else:
            snapshot_id = self.ec2.get_latest_snapshot_id(self.options.uuid)
            if snapshot_id:
                logging.info("Snapshot found: %s" % snapshot_id)
            else:
                logging.info("No snapshot found. An empty #%s volume will be created of #%s GB." % (self.options.type, self.options.size))

        if not volume_id:
            logging.info("Creating volume...")
            volume_id = self.ec2.create_volume(self.options.size, self.options.type, self.metadata['availabilityZone'], snapshot_id)
            if volume_id:
                logging.info("Created volume: %s" % volume_id)

                logging.info("Tagging volume...")
                if self.ec2.tag_volume(volume_id, volume_name, self.options):
                    logging.info("Volume tagged.")
                else:
                    logging.warning("Volume failed tagging.")
            else:
                logging.error("Volume failed creation.")
                sys.exit(1)

        if volume_id:
            logging.info("Attaching volume...")
            if self.ec2.attach_volume(volume_id, self.metadata['instanceId'], self.options.device):
                logging.info('Volume attached to instance.')
            else:
                logging.info('Volume attachment failed.')
                sys.exit(1)


    def tag(self):
        """
          ec2 = Stapler::Ec2.new(metadata[:region])

          puts 'Finding volumes...'
          if (volumes = ec2.get_volume_id(metadata[:instanceId]))
            puts "Volumes found: #{volumes}"

            volumes.each do |volume_id|
              if ec2.tag_volume(volume_id, ec2.get_volume_name(volume_id), options)
                puts "Volume #{volume_id} tagged."
              else
                puts 'Volume failed tagging.'
              end
            end
          else
            puts 'No volumes found.'
            exit 1
          end
        """
        pass
