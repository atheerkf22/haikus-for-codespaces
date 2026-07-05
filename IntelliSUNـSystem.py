#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define TEMP_PIN A0
#define HUMIDITY_PIN A1
#define LDR_R A2
#define LDR_L A3
#define TRIG 10
#define ECHO 11
#define RED 5
#define GREEN 6
#define BLUE 9
#define SERVO_PIN 3
#define BUZZER 8
#define BTN_ON 7
#define BTN_OFF 4

Servo servo;
LiquidCrystal_I2C lcd(0x27, 16, 2);

int angle = 90;
bool systemOn = false;

void setup() {
  Serial.begin(9600);

  lcd.init();        
  lcd.backlight();    

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  pinMode(BTN_ON, INPUT_PULLUP);
  pinMode(BTN_OFF, INPUT_PULLUP);

  servo.attach(SERVO_PIN);
  servo.write(angle);
}

void loop() {
  if (digitalRead(BTN_ON) == LOW) {
    systemOn = true;
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("System ON");
    delay(1000);
  }

  if (digitalRead(BTN_OFF) == LOW) {
    systemOn = false;
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("System OFF");
    setRGB(0, 0, 0);
    digitalWrite(BUZZER, LOW);
    delay(1000);
  }

  if (!systemOn) return;

  float voltage = analogRead(TEMP_PIN) * 0.004882814;
  float tempC = (voltage - 0.5) * 100;

  
  int humidity = analogRead(HUMIDITY_PIN);

  
  if (tempC < 20) setRGB(0, 0, 255);       
  else if (tempC > 35) setRGB(255, 0, 0);  
  else setRGB(0, 255, 0);                  


  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  float dist = pulseIn(ECHO, HIGH) * 0.034 / 2;

  
  if (dist < 20) {
    digitalWrite(BUZZER, HIGH);
  } else {
    digitalWrite(BUZZER, LOW);
  }

  
  int ldrR = analogRead(LDR_R);
  int ldrL = analogRead(LDR_L);
  int diff = abs(ldrR - ldrL);

  if (diff > 50) {
    if (ldrR > ldrL) angle = constrain(angle + 1, 0, 180);
    else angle = constrain(angle - 1, 0, 180);
    servo.write(angle);
  }

 
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  lcd.print(tempC);
  lcd.print("C");

  lcd.setCursor(0, 1);
  lcd.print("Hum: ");
  lcd.print(humidity);

  
  Serial.print(", LDR_R: "); Serial.print(ldrR);
  Serial.print(", LDR_L: "); Serial.print(ldrL);
  Serial.print(", Dist: "); Serial.println(dist);

  delay(1000);
}

void setRGB(int r, int g, int b) {
  analogWrite(RED, r);
  analogWrite(GREEN, g);
  analogWrite(BLUE, b);
}
