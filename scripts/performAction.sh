service=$1
action=$2
host=$3

cat << EOF > action.json
{"serviceName":"$service",
 "action":"$action",
  "token": "cuKAkDvVYyqv/!5ffkCskeE!QP5LzHG?qnWa0-mKEspPYs=QGUfnqhR!vFeL4aBRAVO1LlcNMZF2vIAI?13ft1Dha!Fej565Yt/lTwOd4zLgrAvUYbN/kcmjobfPOBND"
}
EOF

echo curl -k -X POST -H "Content-Type: application/json" \
	-d @action.json \
	 https://$host:16000/api 
curl -k -X POST -H "Content-Type: application/json" \
	-d @action.json \
	 https://$host:16000/api 
