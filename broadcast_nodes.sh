sudo pip3 install awscli
private_ips=`aws ec2 describe-instances --filter Name="tag:Name",Values="$1-*" | jq --raw-output '.Reservations[].Instances[].NetworkInterfaces[].PrivateIpAddresses[].PrivateIpAddress' | grep "." | grep -v "null"`
rm nodefile
for ip in $private_ips
do
    echo "$ip" >> nodefile
done

public_ips=`aws ec2 describe-instances --filter Name="tag:Name",Values="$1-*" | jq --raw-output '.Reservations[].Instances[].NetworkInterfaces[].PrivateIpAddresses[].Association.PublicIp' | grep "." | grep -v "null"`
for ip in $public_ips
do
    scp -i karl.pem nodefile ec2-user@$ip:/home/ec2-user/nodefile
done
