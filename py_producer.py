from confluent_kafka import Producer, Consumer, KafkaException
import argparse
from typing import List
import pickle
import time
import asyncio
from datetime import datetime
import sys

# Configura il broker Kafka
kafka_broker = "localhost:9093"

# Producer: invia messaggi
def produce_message(topic, value):
    producer_config = {
        'bootstrap.servers': kafka_broker
    }
    producer = Producer(producer_config)

    try:
        producer.produce(topic, value)
        producer.flush()
        print("------------")
        print(f"Messaggio inviato a Kafka sul topic {topic}: {value}")
        print("------------")
    except KafkaException as e:
        print(f"Errore durante l'invio del messaggio: {e}")
def get_topic(msg):
    sub1 = str(msg).find("topic") + 7
    sub2 = str(msg).find("'", sub1)
    return str(msg)[sub1:sub2]

# Consumer: legge messaggi
def consume_message():
    consumer_config = {
        'bootstrap.servers': kafka_broker,
        'group.id': 'my-group',  # Identifica il gruppo consumer
        'auto.offset.reset': 'earliest'  # Legge i messaggi dall'inizio del topic
    }
    consumer = Consumer(consumer_config)

    try:
        topic = "test_topic"
        consumer.subscribe([topic])
        print(f"In ascolto sul topic: {topic}")

        while True:
            msg = consumer.poll(1.0)  # Attende un messaggio per un massimo di 1 secondo
            if msg is None:
                continue
            if msg.error():
                print(f"Errore nel messaggio: {msg.error()}")
                continue

            print(f"Messaggio ricevuto: {msg.value().decode('utf-8')}")

    except KeyboardInterrupt:
        print("Chiusura consumer...")
    finally:
        consumer.close()

#classe player FCP
class FCPPlayer():

    def __init__(self, path: str, topics: List[str]):
        with open(path,'rb') as f:
            msgs_list = pickle.load(f)

        self._topics = topics
        self._msgs_list = [msg for msg in msgs_list if msg.topic in topics]

    def get_messages(self, simulate_delays: bool=True):
        msgs_list = self._msgs_list
        delay = 0

        yield msgs_list[0]

        for i in range(1,len(msgs_list)):
            if simulate_delays:
                delay = datetime.fromtimestamp(msgs_list[i].timestamp/1000)-datetime.fromtimestamp(msgs_list[i].timestamp/1000)                
                if delay.total_seconds() > 0:
                    time.sleep(delay)
            
            yield msgs_list[i]


    async def get_messages_async(self, simulate_delays: bool=True):
        msgs_list = self._msgs_list
        delay = 0

        yield msgs_list[0]

        for i in range(1,len(msgs_list)):
            if simulate_delays:
                delay = datetime.fromtimestamp(msgs_list[i].timestamp/1000)-datetime.fromtimestamp(msgs_list[i].timestamp/1000)                
                if delay.total_seconds() > 0:
                    asyncio.sleep(delay)
            
            yield msgs_list[i]

parser = argparse.ArgumentParser(description="")
parser.add_argument('record', nargs='?', default=None, help="recording da cui caricare i messaggi")
args = parser.parse_args()
#se ho passato la registrazione
if args.record:

    path = sys.argv[1]
    producer = FCPPlayer(
        path, 
        [   
                #'ice_data_boxio',
                #'ice_data_cell',
                #'ice_data_cell_control',
                #'ice_data_cell_state',
                #'ice_data_cell2',
                #'ice_data_cell2_control',
                #'ice_data_cell2_kpi',
                #'ice_data_cell2_state',
                #'ice_data_cell4',
                #'ice_data_cell4_control',
                #'ice_data_cell4_kpi',
                #'ice_data_cell4_mission',
                #'ice_data_cell4_state',
                #'ice_data_cell5',
                #'ice_data_cell5_kpi',
                #'ice_data_cell5_state',
                #'ice_data_cell6',
                #'ice_data_cell6_kpi',
                #'ice_data_cell6_state',
                #'ice_data_conveyor',
                #'ice_data_conveyor_alarms',
                #'ice_data_conveyor_control',
                'ice_data_conveyor_fifos',
                #'ice_data_conveyor_kpi',
                #'ice_data_conveyor_state',
                #'ice_data_cram',
                #'ice_data_cram_control',
                #'ice_data_cram_state',
                #'ice_data_energy_meters_abb_robot_data',
                #'ice_data_energy_meters_ceccato_air_compressor_data',
                #'ice_data_energy_meters_dws_3d_printer_data',
                #'ice_data_energy_meters_emco_concept_mill_05_data',
                #'ice_data_energy_meters_ferretto_vertimag_data',
                #'ice_data_energy_meters_kuka_robot_data',
                #'ice_data_energy_meters_mini_pallet_line_data',
                #'ice_data_energy_meters_optical_quality_control_data',
                #'ice_data_energy_meters_quality_control_ur5e_robot_data',
                #'ice_data_energy_meters_spea_4020s2_data',
                #'ice_data_energy_meters_stratasys_3d_printer_data',
                #'ice_data_energy_meters_ur5_robot_data',
                #'ice_data_etensil',
                #'ice_data_etensil_control',
                #'ice_data_etensil_json',
                #'ice_data_etensil_kpi',
                #'ice_data_etensil_state',
                #'ice_data_fleet',
                #'ice_data_fleet_control',
                #'ice_data_fleet_state',
                #'ice_data_fufi',
                #'ice_data_fufi_control',
                #'ice_data_fufi_state',
                #'ice_data_hololens',
                #'ice_data_hololens_control',
                #'ice_data_hololens_state',
                #'ice_data_ice_automation_controller',
                #'ice_data_icetracker',
                #'ice_data_icetracker_raw',
                #'ice_data_irinox',
                #'ice_data_irinox_alarms',
                #'ice_data_irinox_state',
                #'ice_data_kraken',
                #'ice_data_kraken_data_aggregator',
                #'ice_data_kraken_logging',
                #'ice_data_kraken_work_operation',


                #'ice_data_rbkairos_a',
                #'ice_data_rbkairos_a_arm',
                #'ice_data_rbkairos_a_battery',
                #'ice_data_rbkairos_a_cmd_navigation',
                #'ice_data_rbkairos_a_control',
                #'ice_data_rbkairos_a_pose',
                #'ice_data_rbkairos_a_safety',
                #'ice_data_rbkairos_b',
                #'ice_data_rbkairos_b_arm',
                #'ice_data_rbkairos_b_battery',
                #'ice_data_rbkairos_b_cmd_navigation',
                #'ice_data_rbkairos_b_control',
                #'ice_data_rbkairos_b_pose',
                #'ice_data_rbkairos_b_safety',


                #'ice_data_shellies_shelly-4F72_input_0',
                #'ice_data_shellies_shelly-4F72_input_0-4F72_input_0',
                #'ice_data_smart_iot_monitor',
                #'ice_data_smart_iot_monitor_conveyor_belt',
                #'ice_data_smart_iot_monitor_robotic_cell',
                #'ice_data_test'
            ]
    )
    #per ogni messaggio nel record di messaggi
    i=0
    for msg in producer.get_messages():
        #if(i==0):
        topic = get_topic(msg)
        produce_message(topic,str(msg))
        i=1

#altrimenti
else:
    print("Nessun record passato!")
    #produce_message("ice_milling_busy","True")
    produce_message("ice_data_conveyor_fifos","Conveyor,category=state,datatype=Integer,opcua_path=Objects/ConveyorHMI/ConveyorObjects/Segments/Segment2/FIFO/item0,position=0,segment=2 Pallet=4i 1698160397516096000")
    #produce_message("ice_data_conveyor_kpi","test2")
    #produce_message("ice_data_rbkairos_a_arm","test3")
exit()