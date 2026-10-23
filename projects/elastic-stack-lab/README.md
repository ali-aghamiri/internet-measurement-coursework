# Elastic Stack lab: monitoring and threat-event search

This is a **new portfolio reconstruction** of the Elastic Stack workflow described in my two 2024 Internet Measurement project reports. The submitted archives retained the reports and screenshots, but not the original Elasticsearch/Filebeat configuration files. This lab therefore provides fresh, version-matched configuration and executable code; it does not present these files as the historical deployment.

The lab starts a local single-node Elasticsearch, Kibana, and Filebeat. A Python script creates **synthetic** Suricata-style EVE JSON containing 20 normal flow records and five alert records. Filebeat ingests the JSON lines; another script verifies that the alerts reached Elasticsearch. This exercises the collection, indexing, and querying path used in the course projects. It does not run the Suricata detection engine or capture live network traffic.

## Run

Docker Compose and Python 3.10+ are required. From this directory:

```bash
python scripts/generate_eve.py
docker compose up -d
python scripts/check_alerts.py
```

Open Kibana at <http://127.0.0.1:5601>, create a data view for `filebeat-*` using `@timestamp`, and search `event_type: alert` in Discover. Elasticsearch is bound to <http://127.0.0.1:9200>. The generator uses the current UTC time so events appear in Kibana's recent-time view. The demo is for a local machine only; it disables Elasticsearch authentication and binds its web ports to localhost.

Stop the lab with `docker compose down`. To analyze authorized real traffic later, replace `data/eve.json` with EVE JSON from your own Suricata deployment and adapt the input path as needed. Do not commit real packet captures or personal network logs.

The submitted [phase-one](../01-network-monitoring/report-fa.pdf) and [phase-two](../02-threat-detection/report-fa.pdf) reports document the historical course work. This reconstruction focuses on the common Elastic/Filebeat path and a small threat-event query; the reports also discuss other tools such as Suricata, NetFlow, and Metricbeat that are not run by this lab.

Configuration follows the [Elastic Docker quickstart](https://www.elastic.co/search-labs/tutorials/install-elasticsearch/docker), [Filebeat Docker guide](https://www.elastic.co/docs/reference/beats/filebeat/running-on-docker), and [filestream input guide](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-filestream). All three images are pinned to the same Elastic Stack version.
