## Elasticsearch, Fluentd, Kibana

EFK는 로그 수집, 저장, 검색, 분석 및 시각화를 위한 오픈 소스 스택입니다. EFK이전, ELK (Elasticsearch, Logstash, Kibana)를 사용 하였지만... ELK는 대량의 로그 데이터를 처리하기 위해 `높은 CPU 및 메모리 리소스를 필요`로 하며, 이는 쿠버네티스 환경에서는 비용 효율적이지 않을 수 있습니다. `Logstash`는 로그 데이터 처리를 위해 자바로 작성되어 있기 때문에 `자바의 메모리 누수 등의 문제`로 인해 쿠버네티스에서는 안정적으로 동작하지 않을 수도 있습니다. 또한 `Fluentd가 Logstash에 비해 가볍고 더 많은 데이터를 처리할 수 있기 때문`입니다. Fluentd는 다양한 로그 데이터 소스에서 데이터를 수집하고 Elasticsearch로 전달하는 동시에 필요한 데이터를 필터링하고 가공하는 데에 유용합니다. 또한 Fluentd는 쿠버네티스의 네이티브 로그 수집 도구인 kubectl logs와 통합이 가능하며, 쿠버네티스 환경에서 사용하기 적합한 다양한 플러그인을 제공합니다.




kubectl patch svc kibana-kibana -n elasticsearch -p '{"spec": {"type": "LoadBalancer"}}'
kubectl get svc kibana-kibana -n elasticsearch

닫으려면
kubectl patch svc kibana-kibana -n elasticsearch -p '{"spec": {"type": "ClusterIP"}}'

---------
