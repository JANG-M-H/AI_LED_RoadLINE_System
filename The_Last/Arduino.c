// Arduino Code
const int RAIN_SENSOR_PIN = 2;  // 빗물 감지 센서가 연결된 디지털 핀
int rainValue = 0;              // 센서 값을 저장할 변수

void setup() {
  Serial.begin(9600);          // Serial 통신 시작
  pinMode(RAIN_SENSOR_PIN, INPUT);  // 빗물 감지 센서를 입력으로 설정
}

void loop() {
  rainValue = digitalRead(RAIN_SENSOR_PIN);  // 센서 값 읽기 (0 또는 1)
  Serial.println(rainValue);                // 라즈베리파이로 전송
  delay(500);                               // 0.5초마다 데이터 전송
}
