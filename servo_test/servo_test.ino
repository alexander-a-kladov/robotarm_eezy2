#include <Servo.h> // подключаем библиотеку для сервопривода

Servo servo_claw; // объявляем переменную servo типа "servo"
Servo servo_rotate;
Servo servo_fb;
Servo servo_ud;
int val; // освобождаем память в контроллере для переменой

void setup() {
   Serial.begin(9600); // подключаем последовательный порт
   servo_claw.attach(6);
   servo_rotate.attach(9);
   servo_fb.attach(10);
   servo_ud.attach(11);
}

void loop() {
   // проверяем, поступают ли какие-то команды
   if (Serial.available()) {

       val = Serial.parseInt(); // переменная val равна полученной команде
       if (val>600) {
       servo_ud.write(val-600);
       delay(2);
       } else if (val>400) {
        servo_fb.write(val-400);
        delay(2);
       } else if (val>200) {
        servo_rotate.write(val-200);
        delay(2);
       } else if (val>0) {
        servo_claw.write(val);
        delay(2);
       }
   }
}