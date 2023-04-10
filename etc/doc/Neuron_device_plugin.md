# AWS 뉴런 디바이스 플러그인

<br>

쿠버네티스는 컨테이너화된 애플리케이션의 배포 및 관리를 자동화하는 플랫폼이지만, 컴퓨터의 자원 스케쥴링도 지원합니다. 쿠버네티스는 컨테이너를 배포할 때, 컨테이너가 필요로 하는 `CPU, 메모리, 스토리지 등의 자원을 스케쥴링`하여 할당합니다. 이를 위해서 쿠버네티스는 노드의 리소스 상태를 주기적으로 모니터링하고, 각 컨테이너가 요청한 자원을 할당할 수 있는 노드를 찾아 스케쥴링합니다.

그러나 **GPU나 다른 하드웨어**는 일반적으로 `CPU와는 다르게 스케쥴링이 어렵습니다`. 예를 들어, GPU는 전용 드라이버와 함께 작동하는데, 이 드라이버는 호스트 시스템의 커널과 밀접하게 연동되어야 하기 때문입니다. 이러한 장비들을 스케쥴링 하기 위해서, 쿠버네티스에 [GPU 디바이스 플러그인](https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta4/nvidia-device-plugin.yml)나 [뉴런 디바이스 플러그인](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/_downloads/f57f27621e52b305dba7d624c477977a/k8s-neuron-device-plugin.yml) 등, **사용하고자 하는 디바이스 플러그인을 설치** 해줘야 합니다.

<br><br>

현 프로젝트에서는 `뉴런 디바이스 플러그인` 설치와 관련된 파일과 코드 부분은 다음과 같습니다.   

> `chunjae_project / terraform / install-yamlfile-kubectl.tf`

```
## 뉴런 스케줄러 설치
data "kubectl_file_documents" "neuron_device_plugin_rbac"
.
.
.
.
resource "kubectl_manifest" "neuron_my_scheduler" {
    for_each  = data.kubectl_file_documents.neuron_my_scheduler.manifests
    yaml_body = each.value
    depends_on = [
      kubectl_manifest.neuron_device_plugin
    ]
}
## 뉴런 스케줄러 설치끝
```


<br><br><br>

실제 AWS 뉴런 디바이스 플러그인이 설치되는 파일 경로는 다음과 같습니다

> `chunjae_project / k8s / neuron-device-plugin / k8s-neuron-device-plugin-rbac.yaml`   
> `chunjae_project / k8s / neuron-device-plugin / k8s-neuron-device-plugin.yaml`   
> `chunjae_project / k8s / neuron-device-plugin / k8s-neuron-scheduler-eks.yaml`   
> `chunjae_project / k8s / neuron-device-plugin / my-scheduler.yaml`   


<br><br>



**사용할 수 있는 뉴런 코어 확인**
```
kubectl get nodes "-o=custom-columns=NAME:.metadata.name,NeuronCore:.status.allocatable.aws\.amazon\.com/neuroncore"
```

<br><br>



만약, 뉴런 디바이스 플러그인이 작동하지 않는다면 [AWS Neuron SDK 공식문서](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/)에서 
`[  Deploy Containers with Neuron > kubernetes getting started > deploy neuron device plugin  ]`을 참조하면 된다

<br>

----

<br>




참고    

- [GPU 디바이스 플러그인](https://kubernetes.io/ko/docs/tasks/manage-gpus/scheduling-gpus/)
- [AWS Neuron 디바이스 플러그인](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/containers/index.html)