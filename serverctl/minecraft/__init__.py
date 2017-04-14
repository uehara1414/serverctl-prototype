import sys
import os
import digitalocean
import ansible_subprocess
import paramiko
import uuid
import time
import boto3
from threading import Thread
from django.conf import settings
import sys
import subprocess
from serverctl_prototype.utils import slack


prefix = 'minecraft'
token = os.getenv('DIGITAL_OCEAN_TOKEN')

s3 = boto3.resource(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_ACCESS_SECRET'),
)


def get_manager():
    return digitalocean.Manager(token=token)


def delete_droplets():
    manager = get_manager()
    for droplet in manager.get_all_droplets():
        print(droplet.id)
        if droplet.name.startswith(prefix):
            droplet.destroy()


def delete_droplet(droplet_name):
    manager = get_manager()
    for droplet in manager.get_all_droplets():
        if droplet.name == droplet_name:
            droplet.destroy()


def get_drpolet_ip(droplet_name):
    manager = get_manager()
    for droplet in manager.get_all_droplets():
        print(droplet.id)
        if droplet.name == droplet_name:
            return droplet.ip_address


def create_droplet(id):
    manager = get_manager()
    keys = manager.get_all_sshkeys()
    droplet = digitalocean.Droplet(token=token,
                                   name=id,
                                   region='sgp1',
                                   image='centos-7-x64',
                                   size_slug='4gb',
                                   ssh_keys=keys,
                                   backups=False)
    print(f'create{droplet}')
    droplet.create()
    for x in range(120):
        time.sleep(1)
        droplet = [droplet for droplet in manager.get_all_droplets() if droplet.name == id][0]
        if droplet.status == 'active':
            return droplet.ip_address
    return None


def ping(ip):
    for x in range(10):
        time.sleep(1)
        status, i, o = ansible_subprocess.run_ping([ip])
        print(i)
        print(status)
        print(x)
        if status == 0:
            break


def start_new_server(id):
    host = create_droplet(id)
    ping(host)
    slack.send(host)

    a, b, c = ansible_subprocess.run_playbook(f'{settings.BASE_DIR}/playbooks/minecraft/new.yml', [host],
                                              private_key=f'{settings.BASE_DIR}/.ssh/id_rsa')
    slack.send(a)
    slack.send(b)
    slack.send(c)


def restart_new_server(prev_id, now_id):
    host = create_droplet(now_id)
    ping(host)
    slack.send(host)
    src = f'{settings.BASE_DIR}/tmp/{prev_id}.tar.gz'
    command = ['ansible-playbook',
                      f'{settings.BASE_DIR}/playbooks/minecraft/restart.yml',
                      '-i',
                      f'{host},',
                      '--extra-vars',
                      f'"src={src}"',
                      '--private-key',
                      f'{settings.BASE_DIR}/.ssh/id_rsa'
                      ]
    slack.send(' '.join(command))
    subprocess.Popen(' '.join(command), universal_newlines=True, shell=True)
    a, b, c = ansible_subprocess.run_playbook(f'{settings.BASE_DIR}/playbooks/minecraft/new.yml', [host],
                                              private_key=f'{settings.BASE_DIR}/.ssh/id_rsa')


def stop(server_id):
    ip = get_drpolet_ip(server_id)
    slack.send(ip)
    dest = f'{settings.BASE_DIR}/tmp/{server_id}.tar.gz'
    slack.send(dest)
    command = ['ansible-playbook',
                      f'{settings.BASE_DIR}/playbooks/minecraft/save.yml',
                      '-i',
                      f'{ip},',
                      '--extra-vars',
                      f'"dest={dest}"',
                      '--private-key',
                      f'{settings.BASE_DIR}/.ssh/id_rsa'
                      ]
    slack.send(command)
    subprocess.Popen(' '.join(command), universal_newlines=True, shell=True)
    delete_droplet(server_id)


def upload(filename):
    with open('playbooks/data.tar.gz', 'rb') as fp:
        data = fp.read()
    s3.Bucket('7dtd').put_object(Key=f'tmp/{filename}', Body=data)


def download(ip, ):
    ansible_subprocess.run_playbook('playbooks/save.yml', [ip], extra_vars={'server_id': id})


if __name__ == '__main__':
    stop()
