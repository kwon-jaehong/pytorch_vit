# RabbitMQ 및 Redis



RabbitMQ와 Redis는 모두 분산 메시징 시스템입니다. RabbitMQ는 AMQP(Advanced Message Queuing Protocol)를 지원하는 메시징 시스템으로, 메시지 기반의 분산 시스템에서 데이터를 안정적으로 전송하고 처리할 수 있습니다. Redis는 메모리 기반의 데이터 구조 저장소이며, 데이터 캐싱, 키-값 저장소, Pub/Sub 메시징 등의 다양한 용도로 사용됩니다.

<br>

`RabbitMQ와 Redis를 함께 사용하는 이유는 각각의 장점을 활용하여 분산 시스템을 구축하기 위함`입니다. RabbitMQ는 메시지 큐를 사용하여 안정적인 데이터 전송과 처리를 보장하고, Redis는 메모리 기반의 데이터 구조 저장소로서 빠른 데이터 조회와 캐싱에 적합합니다. 또한, RabbitMQ와 Redis는 Pub/Sub 메시징을 모두 지원하므로, 다양한 비동기 통신 시나리오를 구현할 수 있습니다.

<br>

현 프로젝트에서는 RabbitMQ를 사용하여 MSA 간의 메시지 기반 통신하고, Redis를 사용하여 데이터 조회 및 캐싱을 수행하면, MSA 간의 안정적인 통신과 빠른 데이터 조회가 가능해집니다. 




kubectl patch rabbitmqclusters.rabbitmq.com production-rabbitmqcluster -n messagesys --type='json' -p='[{"op": "replace", "path": "/spec/service/type", "value": "LoadBalancer"}]'
kubectl get svc production-rabbitmqcluster -n messagesys    


kubectl patch rabbitmqclusters.rabbitmq.com production-rabbitmqcluster -n messagesys --type='json' -p='[{"op": "replace", "path": "/spec/service/type", "value": "ClusterIP"}]'
kubectl get svc production-rabbitmqcluster -n messagesys    



------------


kubectl apply -f ../k8s/etc_intsall/redis-ui.yaml

kubectl get svc redis-commander -n messagesys  


kubectl delete -f ../k8s/etc_intsall/redis-ui.yaml
-------




아르고 cd

kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d


kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
kubectl get svc argocd-server -n argocd    


kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "ClusterIP"}}'
kubectl get svc argocd-server -n argocd   



---------------------------------------
































kubectl get customresourcedefinition rabbitmqclusters.rabbitmq.com


kubectl get rabbitmqclusters.rabbitmq.com production-rabbitmqcluster -n messagesys    


kubectl get rabbitmqclusters.rabbitmq.com production-rabbitmqcluster -n messagesys    




kubectl patch rabbitmqclusters.rabbitmq.com production-rabbitmqcluster -n messagesys --type='json' -p='[{"op": "replace", "path": "/spec/service/type", "value": "LoadBalancer"}]'
kubectl get svc production-rabbitmqcluster -n messagesys    


kubectl patch rabbitmqclusters.rabbitmq.com production-rabbitmqcluster -n messagesys --type='json' -p='[{"op": "replace", "path": "/spec/service/type", "value": "ClusterIP"}]'
kubectl get svc production-rabbitmqcluster -n messagesys    



------------


kubectl apply -f ../k8s/etc_intsall/redis-ui.yaml

kubectl get svc redis-commander -n messagesys  


kubectl delete -f ../k8s/etc_intsall/redis-ui.yaml

