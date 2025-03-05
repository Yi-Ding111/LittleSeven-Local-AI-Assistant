#!/bin/bash

# 让脚本在出现错误时立即退出
set -e

echo "🚀 Applying Kubernetes manifests..."

aws eks --region ap-southeast-2 update-kubeconfig --name eks-auto-demo

# 依次应用 Kubernetes 资源
kubectl apply -f ./manifests/nodeclass.yaml
kubectl apply -f ./manifests/nodepool.yaml
kubectl apply -f ./manifests/namespace.yaml
kubectl apply -f ./manifests/storage-class.yaml
kubectl apply -f ./manifests/pvc.yaml
kubectl apply -f ./manifests/deployment.yaml
kubectl apply -f ./manifests/service.yaml
kubectl apply -f ./manifests/ingressclass.yaml
kubectl apply -f ./manifests/ingress.yaml

echo "✅ All resources applied successfully!"

# 等待 Service 和 Ingress 的 External IP 分配
echo "⏳ Waiting for External IP allocation..."
sleep 10

# 获取 Service 和 Ingress 信息
kubectl get svc -n ollama
kubectl get ingress -n ollama


# 获取 Ingress 的 External IP/Hostname
EXTERNAL_IP=""

echo "⏳ Waiting for Ingress External Address to be assigned..."

while [ -z "$EXTERNAL_IP" ]; do
  # 先尝试获取 AWS ALB/NLB 的 hostname
  EXTERNAL_IP=$(kubectl get ingress -n ollama -o jsonpath='{.items[*].status.loadBalancer.ingress[0].hostname}')

  # 如果没有 hostname，则尝试获取 IP
  if [ -z "$EXTERNAL_IP" ]; then
    EXTERNAL_IP=$(kubectl get ingress -n ollama -o jsonpath='{.items[*].status.loadBalancer.ingress[0].ip}')
  fi

  # 如果仍然没有获取到 External IP，则等待 5 秒后重试
  if [ -z "$EXTERNAL_IP" ]; then
    echo "🔄 Waiting for External IP to be assigned..."
    sleep 5
  fi
done

# 输出最终的 External IP
echo "🌍 Ingress External Address: $EXTERNAL_IP"

