from kubernetes import client, config
from flask import Flask,request
from os import path
import yaml, random, string, json
import sys
import json

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.CoreV1Api()
app = Flask(__name__)
# app.run(debug = True)

batch_v1 = client.BatchV1Api()

def load_job_yaml(job_type):
    yaml_file = f"{job_type}-job.yaml"
    if not path.exists(yaml_file):
        raise FileNotFoundError(f"Job YAML file {yaml_file} not found")
    
    with open(yaml_file) as f:
        return yaml.safe_load(f)

def create_job(job_type):
    job_yaml = load_job_yaml(job_type)
    
    # Create the job in Kubernetes
    namespace = 'free-service' if job_type == 'free' else 'default'
    api_response = batch_v1.create_namespaced_job(
        body=job_yaml,
        namespace=namespace
    )
    return api_response

@app.route('/config', methods=['GET'])
def get_config():
    pods = []

    pod_list = v1.list_pod_for_all_namespaces()
    
    for pod in pod_list.items:
        pods.append({
            "name": pod.metadata.name,
            "ip": pod.status.pod_ip,
            "namespace": pod.metadata.namespace,
            "node": pod.spec.node_name,
            "status": pod.status.phase
        })

    output = {"pods": pods}
    output = json.dumps(output)

    return output, 200

@app.route('/img-classification/free',methods=['POST'])
def post_free():
    try:
        create_job('free')
        return "success", 200
    except Exception as e:
        return str(e), 500
    

@app.route('/img-classification/premium', methods=['POST'])
def post_premium():
    try:
        create_job('premium')
        return "success", 200
    except Exception as e:
        return str(e), 500

    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
