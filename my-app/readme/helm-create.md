# Helm Charts
## Overview
This README provides a detailed guide on how to create and manage Helm charts for deploying a Flask application. Helm is a package manager for Kubernetes that allows you to define, install, and upgrade even the most complex Kubernetes applications.

## Prerequisites
Before you start, ensure you have the following installed and configured:
- **Kubernetes Cluster**: You need a running Kubernetes cluster. You can use Minikube for local development or any cloud provider for production.
- **kubectl**: The Kubernetes command-line tool. Install it from [here](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
- **Helm**: The package manager for Kubernetes. Install it from [here](https://helm.sh/docs/intro/install/).
- **Docker**: Ensure Docker is installed and running. Install it from [here](https://docs.docker.com/get-docker/).
- **Git**: Make sure Git is installed and configured. Install it from [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

## Repository Structure
The repository structure relevant to Helm charts is as follows:
```
my-app/
├── app/
│   ├── static/
│   ├── templates/
│   ├── app.py
│   ├── requirements.txt
│   ├── .gitattributes
│   └── .gitignore
├── helm-charts/
│   ├── argocd-app/
│   │   ├── templates/
│   │   │   └── application.yaml
│   │   ├── Chart.yaml
│   │   └── values.yaml
│   ├── todo-app/
│   │   ├── templates/
│   │   │   ├── service.yaml
│   │   │   ├── deployment.yaml
│   │   │   └── _helpers.tpl
│   │   ├── Chart.yaml
│   │   └── values.yaml
├── agent.yaml
├── argocd.yaml
├── Dockerfile
├── Jenkinsfile
└── README.md
```
## Creating Helm Charts

### Step 1: Initialize Helm Chart
To create a new Helm chart for your application, navigate to the `my-app` directory and use the following command:
```sh
helm create todo-app
```
This command will create a new directory called todo-app with the default Helm chart structure.

### Step 2: Define the Chart Metadata
The `Chart.yaml` file contains metadata about the chart. It is located in the `helm-charts/todo-app` directory.

### Step 3: Configure Values
The `values.yaml` file contains the default values for your chart. It is also located in the `helm-charts/todo-app` directory. You can define values such as the Docker image repository, tag, and other configuration options.

### Step 4: Define Kubernetes Resources
The `templates` directory contains the Kubernetes resource definitions.

- **service.yaml**: This file defines the Kubernetes Service resource, which exposes your application to other services or the internet.
- **deployment.yaml**: This file defines the Kubernetes Deployment resource, which ensures that a specified number of pod replicas are running.
- **_helpers.tpl**: This file contains helper templates used in other templates.

### Step 5: Customizing Templates

#### service.yaml
Define the service that exposes your application. This typically includes the type of service (ClusterIP, NodePort, LoadBalancer), the port on which your application will run, and the selector that matches the deployment.

#### deployment.yaml
Define the deployment that manages your application's pods. This includes the Docker image to use, and any environment variables or configurations needed for your application to run. The number of replicas is specified in the `values.yaml` file.

#### _helpers.tpl
This file is used to define reusable template snippets that can be included in other templates to avoid repetition.

### Step 6: Update Values File
In the `values.yaml` file, specify the configuration values that your templates will use. For example, you can define the Docker image repository and tag:
```yaml
image:
  repository: yahav12321/todo-app
  tag: "latest"
```

### Step 7: Install or Upgrade the Helm Chart

#### Create Namespace
Before installing the chart, create a namespace for your application using the following command:
```sh
kubectl create namespace todons
```

#### Install the Chart
Once you have defined your Helm chart, you can install it using the following command:
```sh
helm install todo-app helm-charts/todo-app --namespace todons
```

#### Upgrade the Chart

If you make changes to the chart and want to apply them, use the upgrade command:
```
helm upgrade todo-app helm-charts/todo-app --namespace todons
```

### Conclusion
This guide provides a comprehensive overview of creating and managing Helm charts for deploying a Flask application on Kubernetes. By following the steps outlined, you can efficiently manage your application's deployment configuration and leverage Helm's powerful features to simplify Kubernetes deployments.