# Karpenter - 클러스터 오토 스케일링

<br>

Karpenter는 Kubernetes 클러스터에서 클러스터 자원(노드)을 동적으로 프로비저닝하고 관리하는 오토스케일링 기능을 제공하는 오픈소스 애플리케이션입니다.

Karpenter를 사용하면 Kubernetes 클러스터에서 Pod를 실행할 수 있는 노드의 수를 자동으로 증가시키거나 감소시키며, `클러스터의 자원 사용량에 따라 노드 수를 조절할 수 있습니다`. 또한 Karpenter는 클러스터 자원 관리에 대한 일부 최적화를 자동으로 처리하여 클러스터의 자원 사용량을 최적화하고, 클러스터 관리자가 노드 관리에 필요한 일부 작업을 자동화합니다.

Karpenter는 다양한 클라우드 환경에서 사용할 수 있으며, 이를 통해 Kubernetes 클러스터를 더욱 효율적으로 관리할 수 있습니다. Karpenter는 Kubernetes와 완전히 호환되며, Kubernetes의 API와 리소스 모델을 사용하여 노드를 자동으로 관리합니다. 따라서 Karpenter를 사용하여 Kubernetes 클러스터의 성능을 향상시키고 비용을 절감할 수 있습니다.

<br><br><br>


**Karpenter 설치와 관련된 파일과 코드 부분은 아래와 같습니다.**   
<br><br>

EKS에서 카펜터가 자원을 컨트롤 할 수 있도록 iam에 역할 등록
> `chunjae_project / terraform / karpenter-controller-role.tf`   
> `chunjae_project / terraform / controller-trust-policy.json`   

<br><br>


쿠버네티스에 카펜터 helm으로 설치
> `chunjae_project / terraform / install-helm-chart.tf`
```
## 쿠버네티스에 카펜터 helm 설치
resource "helm_release" "karpenter" 
.
.
.
.

```
<br><br>


카펜터 프로비저너 쿠버네티스에 배포
> `chunjae_project / terraform / install-yamlfile-kubectl.tf`

```
# 카펜터 프로비저너 설치
data "kubectl_file_documents" "karpenter_provisioner"
.
.
.
.
```

<br><br>

----

<br>

참고    
- [ Karpenter 공식 문서 ](https://karpenter.sh/)
