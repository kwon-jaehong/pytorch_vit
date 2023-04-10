

쿠버네티스는 컨테이너화된 애플리케이션의 배포 및 관리를 자동화하는 플랫폼이지만, 컴퓨터의 자원 스케쥴링도 지원합니다. 쿠버네티스는 컨테이너를 배포할 때, 컨테이너가 필요로 하는 `CPU, 메모리, 스토리지 등의 자원을 스케쥴링`하여 할당합니다. 이를 위해서 쿠버네티스는 노드의 리소스 상태를 주기적으로 모니터링하고, 각 컨테이너가 요청한 자원을 할당할 수 있는 노드를 찾아 스케쥴링합니다.


그러나 `GPU나 다른 하드웨어는 일반적으로 CPU와는 다르게 스케쥴링이 어렵습니다`. 예를 들어, GPU는 전용 드라이버와 함께 작동하는데, 이 드라이버는 호스트 시스템의 커널과 밀접하게 연동되어야 하기 때문입니다. 이를 위해 쿠버네티스에 [GPU 디바이스 플러그인](https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta4/nvidia-device-plugin.yml)나 [뉴런 디바이스 플러그인](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/_downloads/f57f27621e52b305dba7d624c477977a/k8s-neuron-device-plugin.yml) 등, 사용하고자 하는 디바이스 플러그인을 설치해줘야 한다.


AWS Inferentia 인스턴스의 Neuron chip


쿠버네티스에는 기본적으로 CPU, RAM 등 컴퓨터가 
GPU 





그러나 최근에는 NVIDIA의 Kubernetes on GPU(GoGPU)와 같은 프로젝트가 출시되어 GPU 자원 스케쥴링을 지원하고 있습니다. 이러한 프로젝트들은 GPU 리소스를 컨테이너 내부에서 직접 할당할 수 있는 기능을 제공하여, GPU를 쿠버네티스에서 사용할 수 있게 해줍니다.



참고:    
[GPU 스케쥴링](https://kubernetes.io/ko/docs/tasks/manage-gpus/scheduling-gpus/)
[AWS Neuron 스케쥴링](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/containers/index.html)