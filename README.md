# Thesis (Bachelor Thesis)

## The App
Aplikasi ini digunakan untuk memfasilitasi deteksi korban SAR secara otomatis dalam kegiatan SAR menggunakan UAV secara _real-time_. Aplikasi ini berbasiskan arsitektur sistem FogVerse. 

## Keywords
UAV, _Wireless Networking_, FogVerse, _Fog Computing_, _Cloud Computing_, _Publish/Subscribe_, Kafka, _Machine Learning_, YOLO, YOLOv5

## How to use
### _Pre TODO_
1. Siapkan docker image yang dibutuhkan dengan docker registry yang Anda tentukan. 
- Untuk membuat docker image yang diperlukan, dapat gunakan _file-file_ berprefiks `ci yang terkait.
- Jangan lupa untuk atur kembali docker image pada _file-file_ `docker-compose.yml` yang digunakan

### _only local_ scenario
1. Jalankan seluruh _service_ dari `kafka/local-cluster/docker-compose.yml` pada komputer SafeZone
2. Siapkan topic.yaml:
* _Uncomment_ topic __input__. Pastikan nilai __partitions__ nya 1
* _Uncomment_ topic __final_uav_1__
* _Uncomment_ topic __final_uav_2__ jika menggunakan dua UAV
* _Comment_ sisanya
3. Jalankan `python confluent-kafka-topic-administration/main.py` pada komputer SafeZone
4. Jalankan _service_ __local_executor__ dari `docker-compose.yml` pada komputer SafeZone. Pastikan nilai **_environment_** __ARCHITECTURE__ bernilai `ARCHITECTURE=only_local` 
5. Jalankan `python client/main.py` pada komputer SafeZone
6. Nyalakan fitur Wi-Fi Hotspot pada komputer SafeZone
- Gunakan __Hotspot Lite__ jika fitur Wi-Fi Hotspot tidak dapat dinyalakan tanpa adanya koneksi internet
7. Nyalakan UAV DJI Tello dan komputer SAR _group_
8. Buat sebuah virtual environtment, lalu jalankan `pip install -r requirements.txt` pada komputer SAR _group_
9. Integrasikan komputer SAR _group_ dengan __Wi-Fi USB dongle__
10. Koneksikan komputer SAR _group_ ke UAV dan komputer SafeZone
11. Jalankan `python drone-frame-forwarder/main.py`


### _with cloud_ scenario
1. asdfasdfasdfasd
2. asdfasdfasdfasd
3. asdfasdfasdfasd

## Author
Muhamad Andre Gunawan - Bachelor's Degree of Computer Science Study Program, Faculty of Computer Science University of Indonesia

## Supervisor
Muhammad Hafizhuddin Hilman, S.Kom., M.Kom., Ph.D.

##  Thesis Report
* [Report](https://drive.google.com/file/d/1ZfX620KBQb6_frQiQHsDuWsVFuQBTr0s/view)

## Credit
* [FogVerse](https://github.com/fogverse) by Muhammad Ariq Basyar