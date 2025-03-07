#!/bin/bash

# exit immediately if an error occurs
set -e

echo "Applying Kubernetes manifests..."

aws eks --region ${AWS_REGION} update-kubeconfig --name eks-auto-demo

# Apply Kubernetes resources one by one
# kubectl apply -f ./manifests/nodeclass.yaml
kubectl apply -f ./manifests/nodeclass.yaml
kubectl apply -f ./manifests/nodepool.yaml
kubectl apply -f ./manifests/namespace.yaml
kubectl apply -f ./manifests/storage-class.yaml
kubectl apply -f ./manifests/pvc.yaml
kubectl apply -f ./manifests/deployment.yaml
kubectl apply -f ./manifests/service.yaml
kubectl apply -f ./manifests/ingressclass.yaml
kubectl apply -f ./manifests/ingress.yaml

echo "All resources applied successfully!"

# Wait for External IPs of Service and Ingress to be allocated
echo "Waiting for External IP allocation..."
sleep 10

# Get Service and Ingress information
kubectl get svc -n ollama
kubectl get ingress -n ollama


# Get the External IP/Hostname of Ingress
EXTERNAL_IP=""

echo "Waiting for Ingress External Address to be assigned..."

# Limit the number of attempts to avoid infinite loops
MAX_RETRY=10
RETRY_COUNT=0

while [ -z "$EXTERNAL_IP" ] && [ "$RETRY_COUNT" -lt "$MAX_RETRY" ]; do
  # Try to get AWS ALB/NLB 的 hostname
  EXTERNAL_IP=$(kubectl get ingress -n ollama -o jsonpath='{.items[*].status.loadBalancer.ingress[0].hostname}')

  # If there is no hostname, try to get the IP
  if [ -z "$EXTERNAL_IP" ]; then
    EXTERNAL_IP=$(kubectl get ingress -n ollama -o jsonpath='{.items[*].status.loadBalancer.ingress[0].ip}')
  fi

  # If the External IP is still not obtained, wait 5 seconds and try again.
  if [ -z "$EXTERNAL_IP" ]; then
    echo "Waiting for External IP to be assigned...Attempt $((RETRY_COUNT+1))/$MAX_RETRIES"
    sleep 5
    RETRY_COUNT=$((RETRY_COUNT + 1))
  fi
done

if [ -z "$EXTERNAL_IP" ]; then
  echo "Failed to obtain External IP after $MAX_RETRY retries."
  exit 1
else
  echo "External IP obtained: $EXTERNAL_IP"
fi

