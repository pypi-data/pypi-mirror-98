# roi-iot-device

阿里云 IoT 设备接入封装

- python >=3.5 

## Update

**v1.0.7**

- Fix Auto Deploy

**v1.0.6**

- DeviceInfo 文件名由型号生成

## Dir

目录结构要求

```
root dir
   - config         # 运行时，配置文件存放目录
   - things         # 物模型定义实现
   - main.py        # 主函数
   - thing.json     # 物模型文件，由平台定义后导出，不可自行编辑
```

## Config

新建目录，目录可为空

## Things

物模型定义与实现

**XXXThing**

继承 iot_thing/IoThing 类，并进行实现

```
class PhoneThing(IoThing):
   xxx
```

**XXXProperties**

继承 iot_thing/IoThingProperties 类，并进行实现

```
class Phone(IoThingProperties):

    def __init__(self):
       # 与平台属性定定义一致
       self.number = "" # 序列号
       self.disk = "" # 存储
```
**XXXEvent**

继承 iot_thing/IoThingEvent 类，并进行实现

```
class PhoneEvent(IoThingEvent):

    def __init__(self):
       # 与平台 事件定义一致
       self.event_name = "event_high_temperture" # 事件名称
       self.temperture = "36.0℃" # 存储
```

**XXXService**

继承 iot_thing/IoThingService 类，并进行实现

```
class PhoneService(IoThingService):

    def __init__(self):
       # 与平台 服务定义一致
       self.identifier = "event_high_temperture" # 事件名称
       self.temperture = "36.0℃" # 存储
```

## Main.py

主项目入口，启动项目

**设备秘钥**

表明设备身份的信息，由下面信息进行加密组成

- 秘钥 : 自行定义 key ；
- 内容 : 平台新建产品，对应相关产品信息
- 生成 : IoTools/aes_encode 函数生成

```
{
        "product_key": "复制",
        "product_secret": "复制",
        "endpoint": "",
}
```

**平台定义**

新建产品及其设备

- 产品 : 新建时，定义物模型，并导出 物模型文件。
- 产品 : 设置设备动态注册。
- 产品 : 物模型中的属性、服务、事件定义与 thing 保持一致；
- 设备 : 新建时，记录设备名称，下面要有；
- secret_info : 内容，设备秘钥加密内容；

**设备信息**

初始化设备信息，及其参数，初始化需要参数

- device_name : 设备名称，平台定义，新建设备定义的设备名称
- device_key  : 秘钥，设备秘钥生成的 key;
- secret_info : 内容，设备秘钥加密内容；

```
# IoTDevice 定义
device_info = IoTDeviceInfo(is_debug=True)
device_info.init_info(device_name, product_key, secret_info)
```

**设备物模型**

thing 已经定义后，初始化即可

```
# IoTDevice 定义
device_thing = PhoneThing()
```

**设备连接**

设备动态注册和连接云端

- device_info  : 设备信息对象
- device_thing : 设备物模型对象

```
# 设备连接
device = IoTDevice(device_info, device_thing)
device.connect()
# 阻断运行
while True:
    # print(device.is_conn)
    time.sleep(1000)
```

## Thing.json

由平台定义后，设备管理/产品/产品详情/功能定义/物模型 TSL , 自行导出

## 其他

**日志**

```
# 入参 is_debug = True
device_info = IoTDeviceInfo(is_debug=True)
```

- 开发模式 : is_debug = True

```
# 日志示例
2021-01-31 02:10:24,417 - DEBUG: ali device connect...
Device: 设备连接中..
2021-01-31 02:10:24,418 - DEBUG: connect_async
2021-01-31 02:10:24,418 - DEBUG: LoopThread thread enter
2021-01-31 02:10:24,418 - DEBUG: enter
2021-01-31 02:10:24,419 - INFO: start connect
2021-01-31 02:10:24,419 - DEBUG: current working directory:/Users/yuan/SmartAHC/roi-iot-device
```

- 生产模式：is_debug = False

```
# 日志示例
Device: 设备连接中..
Device: 设备连接成功
Device: 设备运行中
```

## Example

见  sample.py 

## 注意事项

搞清楚设备如何定义，请先在定义产品及其设备，再进行开发；

- 要监控哪些数据（属性）
- 要上报哪些信息（事件）
- 要下发哪些信息，达到反向控制 (服务)
