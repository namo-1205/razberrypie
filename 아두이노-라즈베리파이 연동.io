#include "HX711.h" //(무게센서)
#include "DHT.h" // (온습도센서)

#define calibration_factor -7050.0 // (무게센서) 최초 영점을 잡기 위한 calibration(교정)

#define DOUT  4 //(무게센서) 데이터 핀
#define CLK  7 //(무게센서) 클럭 핀

#define DHTPIN 2        // (온습도센서) SDA 핀의 설정
#define DHTTYPE DHT22   // (온습도센서) DHT22 (AM2302) 센서종류 설정

int CDS = A1;   // (조도센서) 모듈 연결한 핀
int GasPin = A0;   // (가스센서) 입력을 위한 아날로그 핀

HX711 scale(DOUT, CLK); //(무게센서)
DHT dht(DHTPIN, DHTTYPE); //(온습도센서)

void setup() {
	Serial.begin(9600); 
	scale.set_scale(calibration_factor); 
	scale.tare();  // for 초기화
	pinMode(CDS, INPUT);  // 조도 센서를 입력 핀으로 설정
	pinMode(GasPin ,INPUT);   // 아날로그 핀 A0를 입력모드로 설정
	dht.begin();
}

void loop() {
	Serial.print("Wei: ");
	Serial.println(scale.get_units()*45, 1); //g, 소수점 자릿수 1

	Serial.print("CDS: ");
	Serial.println( analogRead(A1) );         // 시리얼 모니터에 조도 센서의 측정 값 출력, 0~1023 사이의 값 출력.
  
	Serial.print("Gas: ");
	Serial.println(analogRead(GasPin));
	
	float h = dht.readHumidity();
	float t = dht.readTemperature();
 
  Serial.print("Hum: "); 
  Serial.println(h);

  Serial.print("Tem: "); 
  Serial.println(t);
  }
}
