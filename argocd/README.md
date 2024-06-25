# ArgoCD installation
## install ArgoCD instance on Kubernetes
(based on this page: https://argo-cd.readthedocs.io/en/stable/getting_started/)

### Requirements
- Installed kubectl command-line tool.
- ArgoCD will automatically connect to the Kubernetes cluster and manage the cluster it is installed on.
 
### Install Argo CD using gitbash terminal:
```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
This will create a new namespace, argocd, where Argo CD services and application resources will live.

Change the argocd-server service type to NodePort:
```
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "NodePort"}}'
```

Verify the changes following the command:
```
kubectl get svc -n argocd
```
![alt text](pictures/1.png)

Get the password from the new terminal using this command using Gitbash:
```
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d
```

You can now access the Argo CD UI from your browser by typing the following URL:
```
localhost:31523
```

Login to Argo CD UI using the username: 'admin' and and the above password

![alt text](pictures/2.png)

