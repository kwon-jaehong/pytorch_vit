# OCR 서비스 관련 문서

AWS 계정 생성 및 엑세스 키, 시크릿 키 발급
테라폼 설치
kubectl 설치
AWS CLI 설치


## 목차
1. 서비스 인프라 환경
-------
`OCR 서비스` 프로젝트는 AWS EKS 기반으로 구축 되었고, 이를 관리하는 도구는 `Terraform`입니다.

테라폼(Terraform)은 인프라스트럭처 자동화 도구입니다. 즉, 클라우드나 온프레미스 환경에서 인프라를 관리하고 프로비저닝하는 일련의 과정을 자동화할 수 있도록 지원합니다.

<br>

쉽게말해 `파이썬 처럼` 코드를 작성해서 아마존웹서비스(AWS), 구글 클라우드 플랫폼(GCP), 온프레미스 환경을 `프로비저닝` 할 수 있습니다.
- **프로비저닝(provisioning)**: 사용자의 요구에 맞게 시스템 자원을 할당, 배치, 배포해 두었다가 필요 시 시스템을 즉시 사용할 수 있는 상태로 미리 준비해 두는 것을 말한다.

<br><br>


아래는 테라폼에서 aws ec2 인스턴스를 생성하는 예시 코드입니다.
```
resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
}
```


[테라폼 설치](etc/image/doc/terraform_install.md)





AWS EKS (아마존 쿠버네티스 환경)

[label](etc/image/doc/terraform_install.md)
인프라 환경
l


인프라스트럭처Infrastructure as Code, IaC



