# Create main project directory
New-Item -ItemType Directory -Force -Path rag_news_project
Set-Location rag_news_project

# Create GitHub workflows directory
New-Item -ItemType Directory -Force -Path .github\workflows

# Create src directory and its subdirectories
'crawler', 'processing', 'database', 'retrieval', 'generation' | ForEach-Object {
    New-Item -ItemType Directory -Force -Path "src\$_"
}

# Create tests directory
New-Item -ItemType Directory -Force -Path tests

# Create kubernetes directory
New-Item -ItemType Directory -Force -Path kubernetes

# Create files in the root directory
'Dockerfile', 'docker-compose.yml', 'requirements.txt', '.env.production', '.env.staging', 'README.md' | ForEach-Object {
    New-Item -ItemType File -Force -Path $_
}

# Create files in .github/workflows
$cicdContent = @'
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: python -m pytest tests/

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v2
    - name: Build and push Docker image
      env:
        DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
        DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
      run: |
        docker build -t yourdockerhubusername/rag-news-app:${{ github.sha }} .
        echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
        docker push yourdockerhubusername/rag-news-app:${{ github.sha }}

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Kubernetes
      env:
        KUBE_CONFIG: ${{ secrets.KUBE_CONFIG }}
      run: |
        echo "$KUBE_CONFIG" > kubeconfig.yaml
        kubectl --kubeconfig=kubeconfig.yaml set image deployment/rag-news-app rag-news-app=yourdockerhubusername/rag-news-app:${{ github.sha }}
'@
Set-Content -Path .github\workflows\ci-cd.yml -Value $cicdContent

# Create files in src and its subdirectories
New-Item -ItemType File -Force -Path src\app.py
'crawler', 'processing', 'database', 'retrieval', 'generation' | ForEach-Object {
    New-Item -ItemType File -Force -Path "src\$_\__init__.py"
    New-Item -ItemType File -Force -Path "src\$_\$_.py"
}

# Create test files
'test_crawler.py', 'test_processor.py', 'test_vector_store.py', 'test_query_engine.py', 'test_response_generator.py' | ForEach-Object {
    New-Item -ItemType File -Force -Path "tests\$_"
}

# Create Kubernetes configuration files
$deploymentContent = @'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-news-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rag-news-app
  template:
    metadata:
      labels:
        app: rag-news-app
    spec:
      containers:
      - name: rag-news-app
        image: yourdockerhubusername/rag-news-app:latest
        ports:
        - containerPort: 8501
'@
Set-Content -Path kubernetes\deployment.yaml -Value $deploymentContent

$serviceContent = @'
apiVersion: v1
kind: Service
metadata:
  name: rag-news-app-service
spec:
  selector:
    app: rag-news-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8501
  type: LoadBalancer
'@
Set-Content -Path kubernetes\service.yaml -Value $serviceContent

# Create a basic Dockerfile
$dockerfileContent = @'
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
'@
Set-Content -Path Dockerfile -Value $dockerfileContent

# Create a basic docker-compose.yml
$dockerComposeContent = @'
version: '3'
services:
  rag-app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./src:/app
    environment:
      - ENV=development
'@
Set-Content -Path docker-compose.yml -Value $dockerComposeContent

Write-Host "Project structure created successfully!"