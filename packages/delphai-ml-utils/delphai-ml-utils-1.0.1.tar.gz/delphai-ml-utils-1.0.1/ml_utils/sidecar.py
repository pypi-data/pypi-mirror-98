from kubernetes import client as kube_client, config as kube_config
from kubernetes.config import ConfigException
from multiprocessing import Process
from datetime import datetime
import os
import logging
import time

try:
    DEPLOYMENT = os.getenv('DEPLOYMENT')
    NAMESPACE  = os.getenv('NAMESPACE')
    MORTAL     = float(os.getenv('MORTAL')) * 60
except:
    logging.error('Set the environment variables')

def watch():
    logging.basicConfig(level=logging.DEBUG)
    while True:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')
        now_obj = datetime.strptime(now,'%Y-%m-%d %H:%M:%S,%f')
        try:
            last = __read_logs()
        except:
            logging.error('Failed to read logs!')
            logging.info('Killing deployment: {} in 10 minutes')
            time.sleep(10*60)
            __kill_deployment(DEPLOYMENT,NAMESPACE)
            logging.info('Deployment Killed!')


        delta_time = now_obj - last
        secounds = delta_time.seconds
        
        kill_in = MORTAL - secounds
        logging.info(f'Killing in: {kill_in} secounds')

        # Execute the Kill
        if kill_in <= 0:
            logging.info('Executing the kill')
            __kill_deployment(DEPLOYMENT,NAMESPACE)
            logging.info('Deployment is killed')
        time.sleep(5)

def __read_logs():
    last_line = ''
    with open('requests.log', 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
    split = last_line.split('/')
    t = split[0]
    t_obj = datetime.strptime(t,'%Y-%m-%d %H:%M:%S,%f')
    return t_obj

def __kill_deployment(deployment_name:str,namespace:str):
    try:
        connect_kube = __connect_to_kubernetes_incluster()
        logging.info('Connected to kubernetes incluster')
    except ConfigException as kube_exception:
        logging.error('Failed to connect to kubernetes incluster')
    
    if not connect_kube:
        logging.error('Failed to connect to kubernetes incluster')
        try:
            __connect_to_kubernetes()
            logging.info('Connected to kubernetes')
        except ConfigException as kube_exception:
            logging.error('Failed to connect to kubernetes')
            raise(kube_exception)

    apps_v1 = kube_client.AppsV1Api()
    api_response = apps_v1.delete_namespaced_deployment(
        name=deployment_name,
        namespace=namespace,
        body=kube_client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Deployment deleted. status='%s'" % str(api_response.status))

def __connect_to_kubernetes_incluster():
    try:
        kube_config.load_incluster_config()
        return True
    except Exception as ex:
        logging.debug(str(ex))
        kube_config.load_kube_config()

def __connect_to_kubernetes():
    try:
        kube_config.load_kube_config()
    except Exception as ex:
        logging.debug(str(ex))
        kube_config.load_kube_config()