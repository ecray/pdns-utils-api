# pdns-utils-api
PowerDNS API proxy to query zones for available IPs

https://doc.powerdns.com/authoritative/http-api/index.html

# Usage
## specifying the zone and subnet will find you the next available ip 
> curl https://pdns-api.example.com/fetch/?zone=my.example.com&origin=10.35.54
10.35.54.39

## Get all IPs in the sbunet 
> curl https://pdns-api.example.com/fetch/?zone=my.example.com&origin=10.35.54?all=true
10.35.54.39
10.35.54.40
10.35.54.41
10.35.54.45
10.35.54.46
..

