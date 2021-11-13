```
Maxmind_Key="xxx"
wget -O /tmp/GeoIP2-ISP.tar.gz \
"https://download.maxmind.com/app/geoip_download?edition_id=GeoIP2-ISP&license_key=$Maxmind_Key&suffix=tar.gz" \
&& tar -zxvf /tmp/GeoIP2-ISP.tar.gz  \
&& mv GeoIP2-ISP*/*.mmdb mmdb/GeoIP2-ISP.mmdb  \
&& wget -O /tmp/GeoIP2-City.tar.gz \
"https://download.maxmind.com/app/geoip_download?edition_id=GeoIP2-City&license_key=$Maxmind_Key&suffix=tar.gz"
&& tar -zxvf /tmp/GeoIP2-City.tar.gz  \
&& mv GeoIP2-City*/*.mmdb mmdb/GeoIP2-City.mmdb 

docker build -t ip-enrich . && docker run -v $(pwd)/mmdb:/app/mmdb ip-enrich 

```