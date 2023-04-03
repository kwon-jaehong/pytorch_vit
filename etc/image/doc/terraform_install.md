# Terraform 설치 - Ubuntu

1.테라폼 설치를 위한 다운로드 링크 확인
```
# 최신 버전 다운로드 링크 확인
LATEST_VERSION=$(curl -s https://api.github.com/repos/hashicorp/terraform/releases/latest | grep tag_name | cut -d '"' -f 4)
DOWNLOAD_URL="https://releases.hashicorp.com/terraform/${LATEST_VERSION}/terraform_${LATEST_VERSION}_linux_amd64.zip"
```

<br><br>

2.다운로드 받은 압축 파일을 /usr/local/bin/ 디렉토리에 설치하기 위해 unzip 패키지 설치
```
sudo apt-get update
sudo apt-get install -y unzip
```
<br><br>


3.다운로드 받은 압축 파일 다운로드 및 압축 해제
```
# 다운로드
wget $DOWNLOAD_URL -O terraform.zip

# 압축 해제
sudo unzip terraform.zip -d /usr/local/bin/
```

<br><br>
4.설치 확인
```
terraform version
```
