sudo pip3 install awscli

public_ips=`aws ec2 describe-instances --filter Name="tag:Name",Values="$1-*" | jq --raw-output '.Reservations[].Instances[].NetworkInterfaces[].PrivateIpAddresses[].Association.PublicIp' | grep "." | grep -v "null"`
for ip in $public_ips
do
    ssh -i karl.pem ec2-user@$ip 'cd HPL-solve && git pull'
done
