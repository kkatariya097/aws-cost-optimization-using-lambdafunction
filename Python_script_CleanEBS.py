# boto3 library- AWS SDK for Python, allows you to interact with various AWS services
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # retrieve a list of EBS snapshots owned by the account
    response = ec2.describe_snapshots(OwnerIds=['self'])

    # Iterating through each snapshot & deleting the snapshot if not attached to any volume
    for snapshot in response['Snapshots']:

        # Extracting snapshot ID and volume ID
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')

        if not volume_id:
            # Delete the snapshot if it's not attached to any volume
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted EBS snapshot {snapshot_id} as it was not attached to any volume.")
        else:
            # Check if the volume still exists
            try:
                volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
                if not volume_response['Volumes'][0]['Attachments']:
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Deleted EBS snapshot - {snapshot_id} as it was taken from a volume not attached to any running instance.")
            except ec2.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                    # The volume associated with the snapshot is not found (it might have been deleted)
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Deleted EBS snapshot - {snapshot_id} as its associated volume was not found.")

# The code is designed to clean up unused EBS snapshots by checking whether they are attached to active volumes. 
# If a snapshot is not attached to any volume or if its associated volume is not attached to a running instance, 
# It gets deleted automatically.
