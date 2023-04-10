# Prometheus & Grafana

<br>

현 프로젝트에서는 프로메테우스와 그라파나를 한꺼번에 설치하는 `kube-prometheus-stack` helm을 이용하여 애플리케이션 구성을 하였습니다. 설치와 관련된 파일은 다음과 같습니다.
<br><br><br>

> `chunjae_project / terraform / install-helm-chart.tf`

<br>

```
## 프로메테우스 stack 설치 코드
resource "helm_release" "prometheus_stack"

.
.
.
.

## 프로메테우스 어댑터 설치 코드
resource "helm_release" "prometheus_adapter"

```
<br><br>

설치시 Helm Value 파일을 다음과 같습니다.
> `chunjae_project / k8s / helm / prometheus-stack-chart-value.yaml`    
> `chunjae_project / k8s / helm / prometheus-adapter-chart-value.yaml`


<br><br>

`프로메테우스` : 자원 사용량 모니터링: 프로메테우스는 클러스터의 자원 사용량을 모니터링하고, 애플리케이션의 성능 문제를 식별하는 데 사용됩니다. 이를 통해 개발자는 애플리케이션의 성능을 향상시키는 데 필요한 자원을 할당하고, 시스템 관리자는 클러스터의 자원 사용량을 최적화할 수 있습니다. 또한 새로운 노드가 클러스터에 추가될 때마다 자동으로 추가됩니다.

<br><br>

`프로메테우스 어댑터(prometheus-adapter)` : 쿠버네티스 클러스터 내에서 실행 중인 애플리케이션의 메트릭을 수집하고, 이를 수집된 데이터를 바탕으로 Kubernetes API 서버에 제공하여 사용자가 원하는 형태로 조회하고, 스케일링 등의 작업을 수행할 수 있도록 하는 도구입니다. 프로메테우스 어댑터를 사용하면 Kubernetes API 서버에서 kubectl top 명령어를 사용하여, 클러스터 내에서 실행 중인 파드, 노드 등의 리소스 사용량에 대한 메트릭을 조회할 수 있습니다. 이러한 조회 결과는 Kubernetes API 서버에서 프로메테우스 어댑터를 통해 수집된 데이터를 바탕으로 생성됩니다. 현재 프로젝트에서는 `Inf 인스턴스의 AWS Neuron Core 메트릭 수집`을 위해 사용합니다.

<br><br>




현재 프로젝트 내에서

IP 노출 취소


```
kubectl patch svc stack-kube-prometheus-stac-prometheus -n monitoring -p '{"spec": {"type": "LoadBalancer"}}'
```

<br><br>

```
kubectl get svc stack-kube-prometheus-stac-prometheus -n monitoring 
kubectl get svc stack-kube-prometheus-stac-prometheus -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

<br><br>

```
kubectl patch svc stack-kube-prometheus-stac-prometheus -n monitoring -p '{"spec": {"type": "ClusterIP"}}'
```






-----
그라파나

다양한 데이터 소스 지원: 그라파나는 다양한 데이터 소스를 지원합니다. 이러한 데이터 소스로는 프로메테우스, 그래파이트, 엘라스틱서치, 인플럭스DB, MySQL 등이 있습니다. 이러한 데이터 소스를 그라파나에 연결하면 데이터를 시각적으로 나타낼 수 있습니다.

대시보드 제작: 그라파나를 사용하면 사용자 정의 대시보드를 만들 수 있습니다. 사용자는 그라파나 대시보드를 사용하여 다양한 데이터를 시각화하고, 상호 작용하는 다양한 차트 및 그래프를 생성할 수 있습니다. 대시보드는 다양한 형태로 구성할 수 있으며, 시간 단위로 스트리밍하거나 정적인 데이터를 사용할 수 있습니다.

경고 및 알림: 그라파나는 특정 경고 및 알림을 설정할 수 있습니다. 이를 통해 사용자는 시스템 또는 응용 프로그램의 문제를 미리 알 수 있으며, 이를 해결할 수 있습니다. 경고 및 알림은 이메일, Slack, PagerDuty 등과 같은 다양한 경로로 전송될 수 있습니다.

템플릿: 그라파나는 다양한 템플릿 기능을 제공합니다. 템플릿을 사용하면 비슷한 대시보드를 쉽게 생성할 수 있으며, 다양한 사용자의 필요에 따라 대시보드를 빠르게 변경할 수 있습니다.

분석: 그라파나는 다양한 분석 기능을 제공합니다. 예를 들어, 쿼리의 결과를 시각화하고, 빠른 분석을 위한 필터 및 정렬 기능을 사용할 수 있습니다.

기타 기능: 그라파나는 다양한 기능을 제공합니다. 예를 들어, 그라파나는 알림에 대한 사용자 정의 기능, 대시보드 배포 및 공유 기능 등을 제공합니다.


모든 노드들의 cpu


-----
kubectl patch svc stack-grafana -n monitoring -p '{"spec": {"type": "LoadBalancer"}}'
kubectl get svc stack-grafana -n monitoring
kubectl get svc stack-grafana -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
kubectl patch svc stack-grafana -n monitoring -p '{"spec": {"type": "ClusterIP"}}'

----


----

kubectl patch svc kibana-kibana -n elasticsearch -p '{"spec": {"type": "LoadBalancer"}}'
kubectl get svc kibana-kibana -n elasticsearch 
kubectl get svc kibana-kibana -n elasticsearch -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'

닫으려면
kubectl patch svc kibana-kibana -n elasticsearch -p '{"spec": {"type": "ClusterIP"}}'


-----------------------

프로메테우스 로드밸런서 노출, 해체
그라파나 로드 밸런서 노출, 해제 


k9s

-------

프로메테우스 어댑터



참고:
https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack

