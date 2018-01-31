sudo pip3 install awscli
private_ips=`aws ec2 describe-instances | jq --raw-output '.Reservations[].Instances[].NetworkInterfaces[].PrivateIpAddresses[].PrivateIpAddress' | grep "." | grep -v "null"`
rm nodefile
rm ipfile
for ip in $private_ips
do
    echo "$ip slots=48" >> nodefile
    echo "$ip" >> ipfile
done

public_ips=`aws ec2 describe-instances | jq --raw-output '.Reservations[].Instances[].NetworkInterfaces[].PrivateIpAddresses[].Association.PublicIp' | grep "." | grep -v "null"`
for ip in $public_ips
do
    scp -i karl.pem nodefile ec2-user@$ip:/home/ec2-user/nodefile
    scp -i karl.pem ipfile ec2-user@$ip:/home/ec2-user/ipfile
done
