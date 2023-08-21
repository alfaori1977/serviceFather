service=$1
action=$2
host=$3
port=$SERVICE_FATHER_PORT
token=$SERVICE_FATHER_TOKEN_ID

cat << EOF > action.json
{"serviceName":"$service",
 "action":"$action",
 "token": "$token"
}
EOF

echo curl -k -X POST -H "Content-Type: application/json" \
	-d @action.json \
	 https://$host:$port/api 
curl  -k -X POST -H "Content-Type: application/json" \
	-d @action.json \
	 https://$host:$port/api 
