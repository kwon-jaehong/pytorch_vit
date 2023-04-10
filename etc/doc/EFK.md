## Elasticsearch, Fluentd, Kibana

EFK는 로그 수집, 저장, 검색, 분석 및 시각화를 위한 오픈 소스 스택입니다. EFK이전, ELK (Elasticsearch, Logstash, Kibana)를 사용 하였지만... ELK는 대량의 로그 데이터를 처리하기 위해 `높은 CPU 및 메모리 리소스를 필요`로 하며, 이는 쿠버네티스 환경에서는 비용 효율적이지 않을 수 있습니다. `Logstash`는 로그 데이터 처리를 위해 자바로 작성되어 있기 때문에 `자바의 메모리 누수 등의 문제`로 인해 쿠버네티스에서는 안정적으로 동작하지 않을 수도 있습니다. 또한 `Fluentd가 Logstash에 비해 가볍고 더 많은 데이터를 처리할 수 있기 때문`입니다. Fluentd는 다양한 로그 데이터 소스에서 데이터를 수집하고 Elasticsearch로 전달하는 동시에 필요한 데이터를 필터링하고 가공하는 데에 유용합니다. 또한 Fluentd는 쿠버네티스의 네이티브 로그 수집 도구인 kubectl logs와 통합이 가능하며, 쿠버네티스 환경에서 사용하기 적합한 다양한 플러그인을 제공합니다.



<br><br>

현 프로젝트에서는 `엘라스틱 서치, 키바나는 helm`으로, `Fluentd`는 yaml파일로 `직접 설치`하여 애플리케이션 구성을 하였습니다. 설치와 관련된 파일과 코드 부분은 다음과 같습니다. 


> `chunjae_project / terraform / install-helm-chart.tf`


```
## 엘라스틱 서치 설치
resource "helm_release" "elasticsearch" 

.
.
.
.

## 키바나 설치
resource "helm_release" "kibana"

```

<br><br><br><br>


설치는 helm을 이용해서 자동적으로 설치되고, 설치시 필요한 `Helm Value` 파일경로는 다음과 같습니다.
> `chunjae_project / k8s / helm / elasticsearch-chart-value.yaml`    
> `chunjae_project / k8s / helm / kibana-chart-value.yaml`


<br><br><br><br>

`Fluentd` 설치는 yaml파일을 이용해서 설치 합니다.

> `chunjae_project / terraform / install-yamlfile-kubectl.tf`


```
## 로그 수집기 flunedtd config맵 설정
resource "kubectl_manifest" "flunedtd_map"

.
.
.
.

## 로그 수집기 flunedtd config맵 배포
resource "kubectl_manifest" "flunedtd_ds"

```
<br><br><br><br>


실제 `Fluentd`가 설치되는 파일 경로는 다음과 같습니다
> `chunjae_project / k8s / etc_intsall / flunedtd-ds.yaml`    
> `chunjae_project / k8s / etc_intsall / flunedtd-map.yaml`

<br><br><br><br>


------------
<br><br>

**꼭, 필요할때만 아래의 절차를 따라 접속을 해 주시길 바랍니다**.( `주소가 노출되면 외부인이 접근하여 취약점이 발생 할 수 있습니다.` )  


```
## 키바나 공개 주소 획득
kubectl patch svc kibana-kibana -n elasticsearch -p '{"spec": {"type": "LoadBalancer"}}'

## 공개 주소 확인
kubectl get svc kibana-kibana -n elasticsearch
```

<br>

<p align="center">
  <img src="../image/kibana_1.png">
</p>
<p align="center"> [ 키바나 UI ] </p>
<br><br><br><br>


**하고싶은 작업을 마쳤다면, 아래와 같은 명령어로 공개 주소를 닫아 줍니다.**

```
## 공개 IP를 제거
kubectl patch svc kibana-kibana -n elasticsearch -p '{"spec": {"type": "ClusterIP"}}'
```

---------
