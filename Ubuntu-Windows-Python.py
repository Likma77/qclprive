#Ubuntu+Windows Python
import os
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import NetworkSecurityGroup

# Remplacez par votre ID de souscription
SUBSCRIPTION_ID = '09eef35c-bc62-40ab-8932-c171977b897b'
RESOURCE_GROUP_NAME = 'MCI-PYTHON'
LOCATION = 'francecentral'

# Noms des VMs
VM_NAME_UBUNTU = 'MCI-UBUNTU'
VM_NAME_WINDOWS = 'MCI-WINDOWS'

# Autres noms de ressources
VNET_NAME = 'MCI-VNET'
SUBNET_NAME = 'MCI-SUBNET'
NIC_NAME_UBUNTU = 'MCI-NIC-UBUNTU'
NIC_NAME_WINDOWS = 'MCI-NIC-WINDOWS'
PUBLIC_IP_NAME_UBUNTU = 'MCI-IP-UBUNTU'
PUBLIC_IP_NAME_WINDOWS = 'MCI-IP-WINDOWS'
NSG_NAME = 'MCI-NSG'

# Authentification auprès d'Azure en utilisant les informations d'identification CLI
credential = AzureCliCredential()

# Client pour la gestion des ressources
resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)

# Client pour la gestion des machines virtuelles
compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)

# Client pour la gestion réseau
network_client = NetworkManagementClient(credential, SUBSCRIPTION_ID)

# Étape 1 : Créer le groupe de ressources
print("Création du groupe de ressources...")
resource_client.resource_groups.create_or_update(
    RESOURCE_GROUP_NAME,
    {"location": LOCATION}
)

# Étape 2 : Créer le groupe de sécurité réseau (NSG)
print("Création du groupe de sécurité réseau...")
nsg_params = NetworkSecurityGroup(location=LOCATION)
nsg_result = network_client.network_security_groups.begin_create_or_update(
    RESOURCE_GROUP_NAME, NSG_NAME, nsg_params).result()

# Étape 3 : Créer le réseau virtuel et le sous-réseau
print("Création du réseau virtuel...")
vnet_result = network_client.virtual_networks.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    VNET_NAME,
    {
        "location": LOCATION,
        "address_space": {
            "address_prefixes": ["10.13.0.0/16"]
        },
    }
).result()

print("Création du sous-réseau...")
subnet_result = network_client.subnets.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    VNET_NAME,
    SUBNET_NAME,
    {"address_prefix": "10.13.1.0/24"}
).result()

# Étape 4 : Créer des adresses IP publiques pour chaque VM
print("Création de l'adresse IP publique pour Ubuntu...")
ip_address_result_ubuntu = network_client.public_ip_addresses.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    PUBLIC_IP_NAME_UBUNTU,
    {
        "location": LOCATION,
        "sku": {"name": "Standard"},
        "public_ip_allocation_method": "Static",
        "public_ip_address_version": "IPV4"
    }
).result()

print("Création de l'adresse IP publique pour Windows...")
ip_address_result_windows = network_client.public_ip_addresses.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    PUBLIC_IP_NAME_WINDOWS,
    {
        "location": LOCATION,
        "sku": {"name": "Standard"},
        "public_ip_allocation_method": "Static",
        "public_ip_address_version": "IPV4"
    }
).result()

# Étape 5 : Créer les interfaces réseau pour Ubuntu et Windows
print("Création de l'interface réseau pour Ubuntu...")
nic_result_ubuntu = network_client.network_interfaces.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    NIC_NAME_UBUNTU,
    {
        "location": LOCATION,
        "ip_configurations": [{
            "name": "myIpConfig",
            "subnet": {"id": subnet_result.id},
            "public_ip_address": {"id": ip_address_result_ubuntu.id},
            "network_security_group": {"id": nsg_result.id}
        }]
    }
).result()

print("Création de l'interface réseau pour Windows...")
nic_result_windows = network_client.network_interfaces.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    NIC_NAME_WINDOWS,
    {
        "location": LOCATION,
        "ip_configurations": [{
            "name": "myIpConfig",
            "subnet": {"id": subnet_result.id},
            "public_ip_address": {"id": ip_address_result_windows.id},
            "network_security_group": {"id": nsg_result.id}
        }]
    }
).result()

# Étape 6 : Créer les machines virtuelles (Ubuntu et Windows)
print("Création de la machine virtuelle (Ubuntu)...")
vm_parameters_ubuntu = {
    "location": LOCATION,
    "storage_profile": {
        "image_reference": {
            "publisher": 'Canonical',
            "offer": 'UbuntuServer',
            "sku": '18.04-LTS',
            "version": 'latest'
        }
    },
    "hardware_profile": {
        "vm_size": "Standard_DS1_v2"
    },
    "os_profile": {
        "computer_name": VM_NAME_UBUNTU,
        "admin_username": "adminsimplon",
        "admin_password": "P@ssw0rd!!!"
    },
    "network_profile": {
        "network_interfaces": [{
            "id": nic_result_ubuntu.id,
        }]
    }
}

vm_result_ubuntu = compute_client.virtual_machines.begin_create_or_update(
    RESOURCE_GROUP_NAME, VM_NAME_UBUNTU, vm_parameters_ubuntu).result()

print("Création de la machine virtuelle (Windows Server)...")
vm_parameters_windows = {
    "location": LOCATION,
    "storage_profile": {
        "image_reference": {
            "publisher": 'MicrosoftWindowsServer',
            "offer": 'WindowsServer',
            "sku": '2019-Datacenter',
            "version": 'latest'
        }
    },
    "hardware_profile": {
        "vm_size": "Standard_DS1_v2"
    },
    "os_profile": {
        "computer_name": VM_NAME_WINDOWS,
        "admin_username": "adminsimplon", 
        "admin_password": "P@ssword34!!!" 
    },
    "network_profile": {
        "network_interfaces": [{
            "id": nic_result_windows.id,
        }]
    }
}

vm_result_windows = compute_client.virtual_machines.begin_create_or_update(
    RESOURCE_GROUP_NAME, VM_NAME_WINDOWS, vm_parameters_windows).result()

print(f"Les deux VMs ont été créées avec les adresses IP : Ubuntu -> {ip_address_result_ubuntu.ip_address}, Windows -> {ip_address_result_windows.ip_address}")