# OCR 서비스 관련 문서

<br><br><br>

## 목차
1. 필요 툴 설치
2. 서비스 인프라 환경


<br><br><br><br><br><br><br>

-------
## 1.필요 툴 설치
<br> 
OCR 서비스 운영을 위해, 사전 준비 작업으로 로컬 환경에 `terraform & aws-cli`를 설치합니다.

<br>

[테라폼 & aws-cli 설치 및 계정 등록](etc/doc/terraform_aws_install.md)


<br><br>

-----

## 2.서비스 인프라 환경
<br>

`OCR 서비스` 프로젝트는 AWS EKS 기반으로 구축 되었고, 이를 관리하는 도구는 `Terraform`입니다.

테라폼(Terraform)은 인프라스트럭처 자동화 도구입니다. 즉, 클라우드나 온프레미스 환경에서 인프라를 관리하고 프로비저닝하는 일련의 과정을 자동화할 수 있도록 지원합니다.

<br>

쉽게말해 `파이썬 처럼` 코드를 작성해서 아마존웹서비스(AWS), 구글 클라우드 플랫폼(GCP), 온프레미스 환경을 `프로비저닝` 할 수 있습니다.
- **프로비저닝(provisioning)**: 사용자의 요구에 맞게 시스템 자원을 할당, 배치, 배포해 두었다가 필요 시 시스템을 즉시 사용할 수 있는 상태로 미리 준비해 두는 것을 말합니다.

<br>


아래는 테라폼에서 aws ec2 인스턴스를 생성하는 예시 코드입니다.
```
resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
}
```
<br><br>



Amazon `EKS`는 AWS에서 Kubernetes를 완전히 관리하여 사용자는 자신의 애플리케이션에만 집중할 수 있게 해줍니다. 사용자는 Amazon EKS를 통해 클러스터를 만들고 노드를 추가할 수 있습니다. Amazon EKS는 클러스터와 노드를 관리하며 Kubernetes의 모든 기능을 지원합니다. 또한, Amazon EKS는 AWS 서비스와의 통합을 지원하여 AWS 리소스를 쉽게 사용할 수 있습니다.

<br>

즉, `내가 서비스할 컨테이너`만 있으면, 이것들을 자동적으로 리소스 스케쥴 관리, 확장, 자동화된 배포 환경을 제공해주는 컨테이너 오케스트레이션 도구입니다. EKS = 아마존 `쿠버네티스`라고 생각 하면 됩니다.

<br>

------------------------

## 3. Terraform으로 OCR 서비스 환경 구축

<br>

- 먼저 아래의 `테라폼으로 구성한 AWS 구조` 설명을 읽고, 문서를 보는것이 좋습니다.

<br>

[테라폼으로 구성한 AWS 구조 설명](etc/doc/terraform_structure.md)

<br><br><br><br><br><br><br><br><br>




프로젝트 내, 테라폼 작업 폴더로 이동한다
```
cd ./chunjae_project/terraform
```
<br><br><br>

현재 폴더에서 `aws.auto.tfvars` 파일을 생성 후, 다음과 같이 기입한다.

```
AWS_REGION = "OCR 서비스를 설치할 AWS 지역"
AWS_ACCKEY = "AWS 엑세스 키"
AWS_SECRKEY = "AWS 시크릿키 기입"
```

<br>
<p align="center">
  <img src="etc/image/terraform_e1.png">
</p>
<p align="center"> [ 예시 ] </p>
```

<br><br><br><br><br>

그런 다음, 테라폼 작업 폴더로 이동하고 `초기화`를 진행합니다.

```
## 테라폼 프로젝트 초기화 명령어
terraform init
```
<br>
<p align="center">
  <img src="etc/image/terraform_e2.png">
</p>
<p align="center"> [ 테라폼 초기화 성공시 나오는 메세지 ] </p>
```

<br><br><br><br><br>


테라폼 초기화가 성공적으로 되었으면, `terraform apply`으로 현재까지 구성된, 테라폼 코드의 구성요소들을 프로비저닝 할 수 있습니다.
```
## 테라폼 적용 명령어
terraform apply
```
<br><br>



그런다음, terraform apply를 치고 yes를 입력하면 인프라 구축이 진행 됩니다.











------
eip 사전에 미리 만들어라,



https://astrid.tech/2021/02/07/0/grafana-debugging/

https://docs.adeptia.com/display/AC40/Centralized+logging+and+monitoring

https://pro.ideaportriga.com/techlife/what-oracles-dx4c-has-brought-to-siebel-crm-customers

https://www.google.com/imgres?imgurl=https%3A%2F%2Fdocs.vmware.com%2Fen%2FVMware-Tanzu-for-Kubernetes-Operations%2F1.6%2Ftko-reference-architecture%2FImages%2Freference-designs-img-tko-on-aws-tkg-aws-overview.png&tbnid=eurlpvm1iNPvKM&vet=10CEUQMyjXAmoYChMIuIvGhtuP_gIVAAAAAB0AAAAAEMcD..i&imgrefurl=https%3A%2F%2Fdocs.vmware.com%2Fen%2FVMware-Tanzu-for-Kubernetes-Operations%2F1.6%2Ftko-reference-architecture%2FGUID-reference-designs-tko-on-aws.html&docid=s_z1qHWmeEVKtM&w=1548&h=1242&q=kubernetes%20prometheus%20fluntd&ved=0CEUQMyjXAmoYChMIuIvGhtuP_gIVAAAAAB0AAAAAEMcD



각종 소프트웨어 설정들 설명






