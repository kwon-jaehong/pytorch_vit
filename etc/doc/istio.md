# Istio 

<br><br>

Istio는 마이크로서비스 아키텍처를 관리하고 보호하기 위한 오픈 소스 플랫폼입니다. 이를 통해 사용자는 서비스 간의 통신, 트래픽 관리, 보안, 모니터링 등을 중앙에서 제어할 수 있습니다.

<br>

Istio는 Kubernetes와 같은 컨테이너 오케스트레이션 플랫폼 위에서 동작하며, 컨테이너 기반 애플리케이션에서 발생하는 일반적인 문제를 해결하기 위한 다양한 기능을 제공합니다. 이를 통해 개발자는 애플리케이션 로직에만 집중할 수 있으며, 인프라 관리에 소요되는 시간과 노력을 줄일 수 있습니다.

<br>

Istio의 주요 기능으로는 다음과 같은 것들이 있습니다:

<br>

- Traffic management: 트래픽 라우팅, 분산 로드 밸런싱, 장애 조치 및 회복, 블랙홀 및 백오프 등을 관리합니다.
- Security: 서비스 간의 인증, 권한 부여, 데이터 보호 등의 보안 기능을 제공합니다.
- Observability: 모니터링, 추적, 로그 등을 통해 서비스의 성능 및 문제를 파악할 수 있습니다.

<br>

Istio는 많은 기능을 제공하고 있으며, 이를 통해 사용자는 마이크로서비스 아키텍처를 보다 효과적으로 관리할 수 있습니다.

<br><br><br><br>



현 프로젝트에서는 Istio의 `base` , `istiod` , `gateway` helm을 이용하여 설치합니다. Istio Helm에서는 다음과 같은 차트를 사용합니다:
<br>

`base` helm : Istio의 기본 구성을 정의하는 차트입니다. 이를 기반으로 사용자가 원하는 대로 Istio를 구성할 수 있습니다. 이 차트는 Istio Control Plane을 배포하지 않으며, 일반적으로 사용자 지정 차트에서 상속합니다.

<br>

`istiod` helm: Istio Control Plane의 핵심 구성 요소인 istiod를 배포하는 차트입니다. istiod는 Istio의 데이터 평면을 제어하고 관리합니다. 이 차트는 base 차트를 상속합니다.

<br>

`gateway` helm: Istio Gateway를 배포하는 차트입니다. Istio Gateway는 외부 트래픽을 처리하고 분산 애플리케이션에 대한 라우팅 규칙을 정의합니다. 이 차트는 base 차트를 상속합니다.

<br><br><br><br>

istio helm 설치와 관련된 파일은 다음과 같습니다
> `chunjae_project / terraform / install-helm-chart.tf`


```
## istio 설치 시작
resource "helm_release" "istio_base"

.
.
.
.
.

resource "helm_release" "istio_gateway" {
  name = "gateway"

  repository       = "https://istio-release.storage.googleapis.com/charts"
  chart            = "gateway"
  namespace        = "istio-ingress"
  create_namespace = true
  version          = "1.17.1"
  values = ["${file("${var.PATH_HELM_VALUE}/istio-gateway-chart-value.yaml")}"]

  depends_on = [
    helm_release.istio_base,
    helm_release.istiod
  ]
}
## istio 설치 끝
```

<br><br><br><br>


설치시 필요한 `Helm Value` 파일경로는 다음과 같습니다.
> `chunjae_project / k8s / helm / istiod-chart-value.yaml`     
> `chunjae_project / k8s / helm / istio-gateway-chart-value.yaml`    















