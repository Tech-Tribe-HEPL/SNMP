from pysnmp.hlapi import *
import time

def get_snmp_data(oid, host, community='public'):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),
        UdpTransportTarget((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )
    
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
    
    if errorIndication:
        print(errorIndication)
        return None
    elif errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
        ))
        return None
    else:
        for varBind in varBinds:
            return int(varBind[1])

def get_cpu_usage(host, community='public', interval=1):
    # OIDs pour la récupération de valeurs de CPU
    oids = {
        'user': '1.3.6.1.4.1.2021.11.50.0',
        'system': '1.3.6.1.4.1.2021.11.52.0',
        'idle': '1.3.6.1.4.1.2021.11.53.0'
    }
    
    # Récupération de la valeur initiale
    cpu_start = {k: get_snmp_data(v, host, community) for k, v in oids.items()}
    time.sleep(interval)
    # Récupération de la valeur après un interval de temps donné
    cpu_end = {k: get_snmp_data(v, host, community) for k, v in oids.items()}
    
    # Vérification de la bonne récupération des données
    if None in cpu_start.values() or None in cpu_end.values():
        return None
    
    # Calcul delta
    delta = {k: cpu_end[k] - cpu_start[k] for k in oids}
    total_delta = sum(delta.values())
    
    if total_delta == 0:
        return None
    
    # Calcul du pourcentage de CPU utilisé
    cpu_usage = 100 * (1 - (delta['idle'] / total_delta))
    return cpu_usage

if __name__ == '__main__':
    host = '192.168.1.33' 
    community = 'groupelecture'
    interval = 5    

    while True :
        cpu_usage = get_cpu_usage(host, community, interval)
        if cpu_usage is not None:
            print(f"CPU Usage: {cpu_usage:.2f}%")
        else:
            print("Failed to retrieve CPU usage.")
