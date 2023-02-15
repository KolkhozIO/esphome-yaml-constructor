// Auto generated code by esphome
// ========== AUTO GENERATED INCLUDE BLOCK BEGIN ===========
#include "esphome.h"
using namespace esphome;
using std::isnan;
using std::min;
using std::max;
wifi::WiFiComponent *wifi_wificomponent;
mdns::MDNSComponent *mdns_mdnscomponent;
ota::OTAComponent *ota_otacomponent;
api::APIServer *api_apiserver;
using namespace api;
using namespace sensor;
using namespace i2c;
i2c::ArduinoI2CBus *bus_a;
preferences::IntervalSyncer *preferences_intervalsyncer;
dallas::DallasComponent *dallas_dallascomponent;
esp32::ESP32InternalGPIOPin *esp32_esp32internalgpiopin;
modbus_controller::ModbusController *epever;
using namespace uart;
uart::ESP32ArduinoUARTComponent *q23;
esp32::ESP32InternalGPIOPin *esp32_esp32internalgpiopin_3;
esp32::ESP32InternalGPIOPin *esp32_esp32internalgpiopin_2;
using namespace modbus;
modbus::Modbus *q12;
esp32::ESP32InternalGPIOPin *esp32_esp32internalgpiopin_4;
bme280::BME280Component *bme280_bme280component;
sensor::Sensor *sensor_sensor_2;
sensor::Sensor *sensor_sensor;
sensor::Sensor *sensor_sensor_3;
dht::DHT *dht_dht;
esp32::ESP32InternalGPIOPin *esp32_esp32internalgpiopin_5;
sensor::Sensor *sensor_sensor_4;
sensor::Sensor *sensor_sensor_5;
dallas::DallasTemperatureSensor *dallas_dallastemperaturesensor;
scd4x::SCD4XComponent *scd4x_scd4xcomponent;
sensor::Sensor *sensor_sensor_6;
sensor::Sensor *sensor_sensor_7;
sensor::Sensor *sensor_sensor_8;
pulse_counter::PulseCounterSensor *pulse_counter_pulsecountersensor;
esp32::ESP32InternalGPIOPin *esp32_esp32internalgpiopin_6;
mhz19::MHZ19Component *mhz19_mhz19component;
sensor::Sensor *sensor_sensor_9;
sensor::Sensor *sensor_sensor_10;
modbus_controller::ModbusSensor *battery_rated_current;
adc::ADCSensor *adc_adcsensor;
esp32::ESP32InternalGPIOPin *esp32_esp32internalgpiopin_7;
#define yield() esphome::yield()
#define millis() esphome::millis()
#define micros() esphome::micros()
#define delay(x) esphome::delay(x)
#define delayMicroseconds(x) esphome::delayMicroseconds(x)
// ========== AUTO GENERATED INCLUDE BLOCK END ==========="

void setup() {
  // ========== AUTO GENERATED CODE BEGIN ===========
  // esphome:
  //   name: test
  //   build_path: .esphome/build/test
  //   friendly_name: ''
  //   platformio_options: {}
  //   includes: []
  //   libraries: []
  //   name_add_mac_suffix: false
  //   min_version: 2023.2.0
  App.pre_setup("test", "", "", __DATE__ ", " __TIME__, false);
  // wifi:
  //   ap:
  //     password: password
  //     ssid: test
  //     id: wifi_wifiap
  //     ap_timeout: 1min
  //   id: wifi_wificomponent
  //   domain: .local
  //   reboot_timeout: 15min
  //   power_save_mode: LIGHT
  //   fast_connect: false
  //   networks:
  //   - ssid: test
  //     password: password
  //     id: wifi_wifiap_2
  //     priority: 0.0
  //   use_address: test.local
  wifi_wificomponent = new wifi::WiFiComponent();
  wifi_wificomponent->set_use_address("test.local");
  {
  wifi::WiFiAP wifi_wifiap_2 = wifi::WiFiAP();
  wifi_wifiap_2.set_ssid("test");
  wifi_wifiap_2.set_password("password");
  wifi_wifiap_2.set_priority(0.0f);
  wifi_wificomponent->add_sta(wifi_wifiap_2);
  }
  {
  wifi::WiFiAP wifi_wifiap = wifi::WiFiAP();
  wifi_wifiap.set_ssid("test");
  wifi_wifiap.set_password("password");
  wifi_wificomponent->set_ap(wifi_wifiap);
  }
  wifi_wificomponent->set_ap_timeout(60000);
  wifi_wificomponent->set_reboot_timeout(900000);
  wifi_wificomponent->set_power_save_mode(wifi::WIFI_POWER_SAVE_LIGHT);
  wifi_wificomponent->set_fast_connect(false);
  wifi_wificomponent->set_component_source("wifi");
  App.register_component(wifi_wificomponent);
  // mdns:
  //   id: mdns_mdnscomponent
  //   disabled: false
  //   services: []
  mdns_mdnscomponent = new mdns::MDNSComponent();
  mdns_mdnscomponent->set_component_source("mdns");
  App.register_component(mdns_mdnscomponent);
  // ota:
  //   password: password
  //   id: ota_otacomponent
  //   safe_mode: true
  //   port: 3232
  //   reboot_timeout: 5min
  //   num_attempts: 10
  ota_otacomponent = new ota::OTAComponent();
  ota_otacomponent->set_port(3232);
  ota_otacomponent->set_auth_password("password");
  ota_otacomponent->set_component_source("ota");
  App.register_component(ota_otacomponent);
  if (ota_otacomponent->should_enter_safe_mode(10, 300000)) return;
  // api:
  //   password: password
  //   id: api_apiserver
  //   port: 6053
  //   reboot_timeout: 15min
  api_apiserver = new api::APIServer();
  api_apiserver->set_component_source("api");
  App.register_component(api_apiserver);
  api_apiserver->set_port(6053);
  api_apiserver->set_password("password");
  api_apiserver->set_reboot_timeout(900000);
  // sensor:
  // i2c:
  //   sda: 21
  //   scl: 22
  //   scan: true
  //   id: bus_a
  //   frequency: 50000.0
  bus_a = new i2c::ArduinoI2CBus();
  bus_a->set_component_source("i2c");
  App.register_component(bus_a);
  bus_a->set_sda_pin(21);
  bus_a->set_scl_pin(22);
  bus_a->set_frequency(50000);
  bus_a->set_scan(true);
  // esp32:
  //   board: esp32doit-devkit-v1
  //   framework:
  //     version: 2.0.5
  //     source: ~3.20005.0
  //     platform_version: platformio/espressif32 @ 5.2.0
  //     type: arduino
  //   variant: ESP32
  // preferences:
  //   id: preferences_intervalsyncer
  //   flash_write_interval: 60s
  preferences_intervalsyncer = new preferences::IntervalSyncer();
  preferences_intervalsyncer->set_write_interval(60000);
  preferences_intervalsyncer->set_component_source("preferences");
  App.register_component(preferences_intervalsyncer);
  // dallas:
  //   pin:
  //     number: 23
  //     mode:
  //       output: true
  //       input: false
  //       open_drain: false
  //       pullup: false
  //       pulldown: false
  //     drive_strength: 20.0
  //     inverted: false
  //     id: esp32_esp32internalgpiopin
  //   id: dallas_dallascomponent
  //   update_interval: 60s
  dallas_dallascomponent = new dallas::DallasComponent();
  dallas_dallascomponent->set_update_interval(60000);
  dallas_dallascomponent->set_component_source("dallas");
  App.register_component(dallas_dallascomponent);
  esp32_esp32internalgpiopin = new esp32::ESP32InternalGPIOPin();
  esp32_esp32internalgpiopin->set_pin(::GPIO_NUM_23);
  esp32_esp32internalgpiopin->set_inverted(false);
  esp32_esp32internalgpiopin->set_drive_strength(::GPIO_DRIVE_CAP_2);
  esp32_esp32internalgpiopin->set_flags(gpio::Flags::FLAG_OUTPUT);
  dallas_dallascomponent->set_pin(esp32_esp32internalgpiopin);
  // modbus_controller:
  //   id: epever
  //   address: 0x70
  //   modbus_id: q12
  //   setup_priority: 12.0
  //   command_throttle: 0ms
  //   update_interval: 60s
  epever = new modbus_controller::ModbusController(0);
  epever->set_command_throttle(0);
  epever->set_address(0x70);
  epever->set_setup_priority(12.0f);
  epever->set_update_interval(60000);
  epever->set_component_source("modbus_controller");
  App.register_component(epever);
  // uart:
  //   id: q23
  //   rx_pin:
  //     number: 22
  //     mode:
  //       input: true
  //       output: false
  //       open_drain: false
  //       pullup: false
  //       pulldown: false
  //     drive_strength: 20.0
  //     inverted: false
  //     id: esp32_esp32internalgpiopin_2
  //   tx_pin:
  //     number: 21
  //     mode:
  //       output: true
  //       input: false
  //       open_drain: false
  //       pullup: false
  //       pulldown: false
  //     drive_strength: 20.0
  //     inverted: false
  //     id: esp32_esp32internalgpiopin_3
  //   baud_rate: 12
  //   stop_bits: 1
  //   rx_buffer_size: 256
  //   data_bits: 8
  //   parity: NONE
  q23 = new uart::ESP32ArduinoUARTComponent();
  q23->set_component_source("uart");
  App.register_component(q23);
  q23->set_baud_rate(12);
  esp32_esp32internalgpiopin_3 = new esp32::ESP32InternalGPIOPin();
  esp32_esp32internalgpiopin_3->set_pin(::GPIO_NUM_21);
  esp32_esp32internalgpiopin_3->set_inverted(false);
  esp32_esp32internalgpiopin_3->set_drive_strength(::GPIO_DRIVE_CAP_2);
  esp32_esp32internalgpiopin_3->set_flags(gpio::Flags::FLAG_OUTPUT);
  q23->set_tx_pin(esp32_esp32internalgpiopin_3);
  esp32_esp32internalgpiopin_2 = new esp32::ESP32InternalGPIOPin();
  esp32_esp32internalgpiopin_2->set_pin(::GPIO_NUM_22);
  esp32_esp32internalgpiopin_2->set_inverted(false);
  esp32_esp32internalgpiopin_2->set_drive_strength(::GPIO_DRIVE_CAP_2);
  esp32_esp32internalgpiopin_2->set_flags(gpio::Flags::FLAG_INPUT);
  q23->set_rx_pin(esp32_esp32internalgpiopin_2);
  q23->set_rx_buffer_size(256);
  q23->set_stop_bits(1);
  q23->set_data_bits(8);
  q23->set_parity(uart::UART_CONFIG_PARITY_NONE);
  // modbus:
  //   id: q12
  //   flow_control_pin:
  //     number: 22
  //     mode:
  //       output: true
  //       input: false
  //       open_drain: false
  //       pullup: false
  //       pulldown: false
  //     drive_strength: 20.0
  //     inverted: false
  //     id: esp32_esp32internalgpiopin_4
  //   send_wait_time: 250ms
  //   disable_crc: false
  //   uart_id: q23
  q12 = new modbus::Modbus();
  q12->set_component_source("modbus");
  App.register_component(q12);
  q12->set_uart_parent(q23);
  esp32_esp32internalgpiopin_4 = new esp32::ESP32InternalGPIOPin();
  esp32_esp32internalgpiopin_4->set_pin(::GPIO_NUM_22);
  esp32_esp32internalgpiopin_4->set_inverted(false);
  esp32_esp32internalgpiopin_4->set_drive_strength(::GPIO_DRIVE_CAP_2);
  esp32_esp32internalgpiopin_4->set_flags(gpio::Flags::FLAG_OUTPUT);
  q12->set_flow_control_pin(esp32_esp32internalgpiopin_4);
  q12->set_send_wait_time(250);
  q12->set_disable_crc(false);
  // sensor.bme280:
  //   platform: bme280
  //   pressure:
  //     name: test
  //     disabled_by_default: false
  //     id: sensor_sensor
  //     force_update: false
  //     unit_of_measurement: hPa
  //     accuracy_decimals: 1
  //     device_class: pressure
  //     state_class: measurement
  //     oversampling: 16X
  //   temperature:
  //     name: test
  //     oversampling: 16X
  //     disabled_by_default: false
  //     id: sensor_sensor_2
  //     force_update: false
  //     unit_of_measurement: °C
  //     accuracy_decimals: 1
  //     device_class: temperature
  //     state_class: measurement
  //   humidity:
  //     name: test
  //     disabled_by_default: false
  //     id: sensor_sensor_3
  //     force_update: false
  //     unit_of_measurement: '%'
  //     accuracy_decimals: 1
  //     device_class: humidity
  //     state_class: measurement
  //     oversampling: 16X
  //   address: 0x70
  //   update_interval: 60s
  //   id: bme280_bme280component
  //   iir_filter: 'OFF'
  //   i2c_id: bus_a
  bme280_bme280component = new bme280::BME280Component();
  bme280_bme280component->set_update_interval(60000);
  bme280_bme280component->set_component_source("bme280.sensor");
  App.register_component(bme280_bme280component);
  bme280_bme280component->set_i2c_bus(bus_a);
  bme280_bme280component->set_i2c_address(0x70);
  sensor_sensor_2 = new sensor::Sensor();
  App.register_sensor(sensor_sensor_2);
  sensor_sensor_2->set_name("test");
  sensor_sensor_2->set_disabled_by_default(false);
  sensor_sensor_2->set_device_class("temperature");
  sensor_sensor_2->set_state_class(sensor::STATE_CLASS_MEASUREMENT);
  sensor_sensor_2->set_unit_of_measurement("\302\260C");
  sensor_sensor_2->set_accuracy_decimals(1);
  sensor_sensor_2->set_force_update(false);
  bme280_bme280component->set_temperature_sensor(sensor_sensor_2);
  bme280_bme280component->set_temperature_oversampling(bme280::BME280_OVERSAMPLING_16X);
  sensor_sensor = new sensor::Sensor();
  App.register_sensor(sensor_sensor);
  sensor_sensor->set_name("test");
  sensor_sensor->set_disabled_by_default(false);
  sensor_sensor->set_device_class("pressure");
  sensor_sensor->set_state_class(sensor::STATE_CLASS_MEASUREMENT);
  sensor_sensor->set_unit_of_measurement("hPa");
  sensor_sensor->set_accuracy_decimals(1);
  sensor_sensor->set_force_update(false);
  bme280_bme280component->set_pressure_sensor(sensor_sensor);
  bme280_bme280component->set_pressure_oversampling(bme280::BME280_OVERSAMPLING_16X);
  sensor_sensor_3 = new sensor::Sensor();
  App.register_sensor(sensor_sensor_3);
  sensor_sensor_3->set_name("test");
  sensor_sensor_3->set_disabled_by_default(false);
  sensor_sensor_3->set_device_class("humidity");
  sensor_sensor_3->set_state_class(sensor::STATE_CLASS_MEASUREMENT);
  sensor_sensor_3->set_unit_of_measurement("%");
  sensor_sensor_3->set_accuracy_decimals(1);
  sensor_sensor_3->set_force_update(false);
  bme280_bme280component->set_humidity_sensor(sensor_sensor_3);
  bme280_bme280component->set_humidity_oversampling(bme280::BME280_OVERSAMPLING_16X);
  bme280_bme280component->set_iir_filter(bme280::BME280_IIR_FILTER_OFF);
  // sensor.dht:
  //   platform: dht
  //   temperature:
  //     name: temperature
  //     disabled_by_default: false
  //     id: sensor_sensor_4
  //     force_update: false
  //     unit_of_measurement: °C
  //     accuracy_decimals: 1
  //     device_class: temperature
  //     state_class: measurement
  //   humidity:
  //     name: humidity
  //     disabled_by_default: false
  //     id: sensor_sensor_5
  //     force_update: false
  //     unit_of_measurement: '%'
  //     accuracy_decimals: 0
  //     device_class: humidity
  //     state_class: measurement
  //   pin:
  //     number: 12
  //     mode:
  //       input: true
  //       output: false
  //       open_drain: false
  //       pullup: false
  //       pulldown: false
  //     drive_strength: 20.0
  //     inverted: false
  //     id: esp32_esp32internalgpiopin_5
  //   id: dht_dht
  //   model: AUTO_DETECT
  //   update_interval: 60s
  dht_dht = new dht::DHT();
  dht_dht->set_update_interval(60000);
  dht_dht->set_component_source("dht.sensor");
  App.register_component(dht_dht);
  esp32_esp32internalgpiopin_5 = new esp32::ESP32InternalGPIOPin();
  esp32_esp32internalgpiopin_5->set_pin(::GPIO_NUM_12);
  esp32_esp32internalgpiopin_5->set_inverted(false);
  esp32_esp32internalgpiopin_5->set_drive_strength(::GPIO_DRIVE_CAP_2);
  esp32_esp32internalgpiopin_5->set_flags(gpio::Flags::FLAG_INPUT);
  dht_dht->set_pin(esp32_esp32internalgpiopin_5);
  sensor_sensor_4 = new sensor::Sensor();
  App.register_sensor(sensor_sensor_4);
  sensor_sensor_4->set_name("temperature");
  sensor_sensor_4->set_disabled_by_default(false);
  sensor_sensor_4->set_device_class("temperature");
  sensor_sensor_4->set_state_class(sensor::STATE_CLASS_MEASUREMENT);
  sensor_sensor_4->set_unit_of_measurement("\302\260C");
  sensor_sensor_4->set_accuracy_decimals(1);
  sensor_sensor_4->set_force_update(false);
  dht_dht->set_temperature_sensor(sensor_sensor_4);
  sensor_sensor_5 = new sensor::Sensor();
  App.register_sensor(sensor_sensor_5);
  sensor_sensor_5->set_name("humidity");
  sensor_sensor_5->set_disabled_by_default(false);
  sensor_sensor_5->set_device_class("humidity");
  sensor_sensor_5->set_state_class(sensor::STATE_CLASS_MEASUREMENT);
  sensor_sensor_5->set_unit_of_measurement("%");
  sensor_sensor_5->set_accuracy_decimals(0);
  sensor_sensor_5->set_force_update(false);
  dht_dht->set_humidity_sensor(sensor_sensor_5);
  dht_dht->set_dht_model(dht::DHT_MODEL_AUTO_DETECT);
  // sensor.dallas:
  //   platform: dallas
  //   name: dallas_temp
  //   address: 0x70
  //   disabled_by_default: false
  //   force_update: false
  //   id: dallas_dallastemperaturesensor
  //   unit_of_measurement: °C
  //   accuracy_decimals: 1
  //   device_class: temperature
  //   state_class: measurement
  //   dallas_id: dallas_dallascomponent
  //   resolution: 12
  dallas_dallastemperaturesensor = new dallas::DallasTemperatureSensor();
  App.register_sensor(dallas_dallastemperaturesensor);
  dallas_dallastemperaturesensor->set_name("dallas_temp");
  dallas_dallastemperaturesensor->set_disabled_by_default(false);
  dallas_dallastemperaturesensor->set_device_class("temperature");
  dallas_dallastemperaturesensor->set_state_class(sensor::STATE_CLASS_MEASUREMENT);
  dallas_dallastemperaturesensor->set_unit_of_measurement("\302\260C");
  dallas_dallastemperaturesensor->set_accuracy_decimals(1);
  dallas_dallastemperaturesensor->set_force_update(false);
  dallas_dallastemperaturesensor->set_address(0x70);
  dallas_dallastemperaturesensor->set_resolution(12);
  dallas_dallastemperaturesensor->set_parent(dallas_dallascomponent);
  dallas_dallascomponent->register_sensor(dallas_dallastemperaturesensor);
  // sensor.scd4x:
  //   platform: scd4x
  //   co2:
  //     name: co2
  //     disabled_by_default: false
  //     id: sensor_sensor_6
  //     force_update: false
  //     unit_of_measurement: ppm
  //     icon: mdi:molecule-co2
  //     accuracy_decimals: 0
  //     device_class: carbon_dioxide
  //     state_class: measurement
  //   temperature:
  //     name: temperature
  //     disabled_by_default: false
  //     id: sensor_sensor_7
  //     force_update: false
  //     unit_of_measurement: °C
  //     icon: mdi:thermometer
  //     accuracy_decimals: 2
  //     device_class: temperature
  //     state_class: measurement
  //   humidity:
  //     name: humidity
  //     disabled_by_default: false
  //     id: sensor_sensor_8
  //     force_update: false
  //     unit_of_measurement: '%'
  //     icon: mdi:water-percent
  //     accuracy_decimals: 2
  //     device_class: humidity
  //     state_class: measurement
  //   id: scd4x_scd4xcomponent
  //   automatic_self_calibration: true
  //   altitude_compensation: 0
  //   temperature_offset: 4.0
  //   measurement_mode: periodic
  //   update_interval: 60s
  //   i2c_id: bus_a
  //   address: 0x62
  scd4x_scd4xcomponent = new scd4x::SCD4XComponent();
  scd4x_scd4xcomponent->set_update_interval(60000);
  scd4x_scd4xcomponent->set_component_source("scd4x.sensor");
  App.register_component(scd4x_scd4xcomponent);
  scd4x_scd4xcomponent->set_i2c_bus(bus_a);
  scd4x_scd4xcomponent->set_i2c_address(0x62);
  scd4x_scd4xcomponent->set_automatic_self_calibration(true);
  scd4x_scd4xcomponent->set_altitude_compensation(0);
  scd4x_scd4xcomponent->set_temperature_offset(4.0f);
  sensor_sensor_6 = new sensor::Sensor();
  App.register_sensor(sensor_sensor_6);
  sensor_sensor_6->set_name("co2");
  sensor_sensor_6->set_disabled_by_default(false);
  sensor_sensor_6->set_icon("mdi:molecule-co2");
  sensor_sensor_6->set_device_class("carbon_dioxide");
  sensor_sensor_6->set_state_class(sensor::STATE_CLASS_MEASUREMENT);
  sensor_sensor_6->set_unit_of_measurement("ppm");
  sensor_sensor_6->set_accuracy_decimals(0);
  sensor_sensor_6->set_force_update(false);
  scd4x_scd4xcomponent->set_co2_sensor(sensor_sensor_6);
  sensor_sensor_7 = new sensor::Sensor();
  App.register_sensor(sensor_sensor_7);
  sensor_sensor_7->set_name("temperature");
  sensor_sensor_7->set_disabled_by_default(false);
  sensor_sensor_7->set_icon("mdi:thermometer");
  sensor_sensor_7->set_device_class("temperature");
  sensor_sensor_7->set_state_class(sensor::STATE_CLASS_MEASUREMENT);
  sensor_sensor_7->set_unit_of_measurement("\302\260C");
  sensor_sensor_7->set_accuracy_decimals(2);
  sensor_sensor_7->set_force_update(false);
  scd4x_scd4xcomponent->set_temperature_sensor(sensor_sensor_7);
  sensor_sensor_8 = new sensor::Sensor();
  App.register_sensor(sensor_sensor_8);
  sensor_sensor_8->set_name("humidity");
  sensor_sensor_8->set_disabled_by_default(false);
  sensor_sensor_8->set_icon("mdi:water-percent");
  sensor_sensor_8->set_device_class("humidity");
  sensor_sensor_8->set_state_class(sensor::STATE_CLASS_MEASUREMENT);
  sensor_sensor_8->set_unit_of_measurement("%");
  sensor_sensor_8->set_accuracy_decimals(2);
  sensor_sensor_8->set_force_update(false);
  scd4x_scd4xcomponent->set_humidity_sensor(sensor_sensor_8);
  scd4x_scd4xcomponent->set_measurement_mode(scd4x::PERIODIC);
  // sensor.pulse_counter:
  //   platform: pulse_counter
  //   pin:
  //     number: 12
  //     mode:
  //       input: true
  //       output: false
  //       open_drain: false
  //       pullup: false
  //       pulldown: false
  //     drive_strength: 20.0
  //     inverted: false
  //     id: esp32_esp32internalgpiopin_6
  //   name: pulse_counter
  //   disabled_by_default: false
  //   force_update: false
  //   id: pulse_counter_pulsecountersensor
  //   unit_of_measurement: pulses/min
  //   icon: mdi:pulse
  //   accuracy_decimals: 2
  //   state_class: measurement
  //   count_mode:
  //     rising_edge: INCREMENT
  //     falling_edge: DISABLE
  //   use_pcnt: true
  //   internal_filter: 13us
  //   update_interval: 60s
  pulse_counter_pulsecountersensor = new pulse_counter::PulseCounterSensor(true);
  App.register_sensor(pulse_counter_pulsecountersensor);
  pulse_counter_pulsecountersensor->set_name("pulse_counter");
  pulse_counter_pulsecountersensor->set_disabled_by_default(false);
  pulse_counter_pulsecountersensor->set_icon("mdi:pulse");
  pulse_counter_pulsecountersensor->set_state_class(sensor::STATE_CLASS_MEASUREMENT);
  pulse_counter_pulsecountersensor->set_unit_of_measurement("pulses/min");
  pulse_counter_pulsecountersensor->set_accuracy_decimals(2);
  pulse_counter_pulsecountersensor->set_force_update(false);
  pulse_counter_pulsecountersensor->set_update_interval(60000);
  pulse_counter_pulsecountersensor->set_component_source("pulse_counter.sensor");
  App.register_component(pulse_counter_pulsecountersensor);
  esp32_esp32internalgpiopin_6 = new esp32::ESP32InternalGPIOPin();
  esp32_esp32internalgpiopin_6->set_pin(::GPIO_NUM_12);
  esp32_esp32internalgpiopin_6->set_inverted(false);
  esp32_esp32internalgpiopin_6->set_drive_strength(::GPIO_DRIVE_CAP_2);
  esp32_esp32internalgpiopin_6->set_flags(gpio::Flags::FLAG_INPUT);
  pulse_counter_pulsecountersensor->set_pin(esp32_esp32internalgpiopin_6);
  pulse_counter_pulsecountersensor->set_rising_edge_mode(pulse_counter::PULSE_COUNTER_INCREMENT);
  pulse_counter_pulsecountersensor->set_falling_edge_mode(pulse_counter::PULSE_COUNTER_DISABLE);
  pulse_counter_pulsecountersensor->set_filter_us(13);
  // sensor.mhz19:
  //   platform: mhz19
  //   co2:
  //     name: co2
  //     disabled_by_default: false
  //     id: sensor_sensor_9
  //     force_update: false
  //     unit_of_measurement: ppm
  //     icon: mdi:molecule-co2
  //     accuracy_decimals: 0
  //     device_class: carbon_dioxide
  //     state_class: measurement
  //   temperature:
  //     name: temperature
  //     disabled_by_default: false
  //     id: sensor_sensor_10
  //     force_update: false
  //     unit_of_measurement: °C
  //     accuracy_decimals: 0
  //     device_class: temperature
  //     state_class: measurement
  //   id: mhz19_mhz19component
  //   update_interval: 60s
  //   uart_id: q23
  mhz19_mhz19component = new mhz19::MHZ19Component();
  mhz19_mhz19component->set_update_interval(60000);
  mhz19_mhz19component->set_component_source("mhz19.sensor");
  App.register_component(mhz19_mhz19component);
  mhz19_mhz19component->set_uart_parent(q23);
  sensor_sensor_9 = new sensor::Sensor();
  App.register_sensor(sensor_sensor_9);
  sensor_sensor_9->set_name("co2");
  sensor_sensor_9->set_disabled_by_default(false);
  sensor_sensor_9->set_icon("mdi:molecule-co2");
  sensor_sensor_9->set_device_class("carbon_dioxide");
  sensor_sensor_9->set_state_class(sensor::STATE_CLASS_MEASUREMENT);
  sensor_sensor_9->set_unit_of_measurement("ppm");
  sensor_sensor_9->set_accuracy_decimals(0);
  sensor_sensor_9->set_force_update(false);
  mhz19_mhz19component->set_co2_sensor(sensor_sensor_9);
  sensor_sensor_10 = new sensor::Sensor();
  App.register_sensor(sensor_sensor_10);
  sensor_sensor_10->set_name("temperature");
  sensor_sensor_10->set_disabled_by_default(false);
  sensor_sensor_10->set_device_class("temperature");
  sensor_sensor_10->set_state_class(sensor::STATE_CLASS_MEASUREMENT);
  sensor_sensor_10->set_unit_of_measurement("\302\260C");
  sensor_sensor_10->set_accuracy_decimals(0);
  sensor_sensor_10->set_force_update(false);
  mhz19_mhz19component->set_temperature_sensor(sensor_sensor_10);
  // sensor.modbus_controller:
  //   platform: modbus_controller
  //   modbus_controller_id: epever
  //   name: test
  //   id: battery_rated_current
  //   register_type: read
  //   address: 112
  //   unit_of_measurement: 'V '
  //   value_type: U_WORD
  //   disabled_by_default: false
  //   force_update: false
  //   bitmask: 0xFFFFFFFF
  //   skip_updates: 0
  //   force_new_range: false
  //   response_size: 0
  //   register_count: 0
  battery_rated_current = new modbus_controller::ModbusSensor(modbus_controller::ModbusRegisterType::READ, 112, 0, 0xFFFFFFFF, modbus_controller::SensorValueType::U_WORD, 1, 0, false);
  battery_rated_current->set_component_source("modbus_controller.sensor");
  App.register_component(battery_rated_current);
  App.register_sensor(battery_rated_current);
  battery_rated_current->set_name("test");
  battery_rated_current->set_disabled_by_default(false);
  battery_rated_current->set_unit_of_measurement("V ");
  battery_rated_current->set_force_update(false);
  epever->add_sensor_item(battery_rated_current);
  // sensor.adc:
  //   platform: adc
  //   pin:
  //     number: 36
  //     mode:
  //       input: true
  //       output: false
  //       open_drain: false
  //       pullup: false
  //       pulldown: false
  //     drive_strength: 20.0
  //     inverted: false
  //     id: esp32_esp32internalgpiopin_7
  //   name: abc
  //   attenuation: 6db
  //   update_interval: 60s
  //   raw: true
  //   disabled_by_default: false
  //   force_update: false
  //   id: adc_adcsensor
  //   unit_of_measurement: V
  //   accuracy_decimals: 2
  //   device_class: voltage
  //   state_class: measurement
  adc_adcsensor = new adc::ADCSensor();
  adc_adcsensor->set_update_interval(60000);
  adc_adcsensor->set_component_source("adc.sensor");
  App.register_component(adc_adcsensor);
  App.register_sensor(adc_adcsensor);
  adc_adcsensor->set_name("abc");
  adc_adcsensor->set_disabled_by_default(false);
  adc_adcsensor->set_device_class("voltage");
  adc_adcsensor->set_state_class(sensor::STATE_CLASS_MEASUREMENT);
  adc_adcsensor->set_unit_of_measurement("V");
  adc_adcsensor->set_accuracy_decimals(2);
  adc_adcsensor->set_force_update(false);
  esp32_esp32internalgpiopin_7 = new esp32::ESP32InternalGPIOPin();
  esp32_esp32internalgpiopin_7->set_pin(::GPIO_NUM_36);
  esp32_esp32internalgpiopin_7->set_inverted(false);
  esp32_esp32internalgpiopin_7->set_drive_strength(::GPIO_DRIVE_CAP_2);
  esp32_esp32internalgpiopin_7->set_flags(gpio::Flags::FLAG_INPUT);
  adc_adcsensor->set_pin(esp32_esp32internalgpiopin_7);
  adc_adcsensor->set_output_raw(true);
  adc_adcsensor->set_attenuation(ADC_ATTEN_DB_6);
  adc_adcsensor->set_channel(::ADC1_CHANNEL_0);
  // socket:
  //   implementation: bsd_sockets
  // network:
  //   {}
  epever->set_parent(q12);
  epever->set_address(0x70);
  q12->register_device(epever);
  // =========== AUTO GENERATED CODE END ============
  App.setup();
}

void loop() {
  App.loop();
}
