#include <EEPROM.h>
#include <Servo.h>           //https://github.com/arduino-libraries/Servo
#include <ServoEasing.hpp>   //https://github.com/ArminJo/ServoEasing
//#include <ServoEasing.h>


//limitazioni**********************facoltative
int lex1(int gradi){ return constrain(gradi, 5, 175); }
int lex2(int gradi){ return constrain(gradi, 7, 173); }
int lex3(int gradi){ return constrain(gradi, 10, 170); }
int lex4(int gradi){ return constrain(gradi, 10, 170); }
int lex5(int gradi){ return constrain(gradi, 0, 180); }
int lex6(int gradi){ return constrain(gradi, 25, 100); }
//**********************************

ServoEasing servo1;
ServoEasing servo2;
ServoEasing servo3;
ServoEasing servo4;
ServoEasing servo5;
ServoEasing servo6;

//#define MODE EASE_QUARTIC_IN_OUT
//#define MODE EASE_LINEAR
#define MODE EASE_QUADRATIC_IN_OUT
//#define MODE EASE_CUBIC_IN_OUT
//#define MODE EASE_ELASTIC_IN_OUT
//#define MODE EASE_CUBIC_IN_OUT

boolean start_pack = false;
int servo1PPos, servo2PPos, servo3PPos, servo4PPos,servo5PPos,servo6PPos;
int posizioni;
String lettura;
int val1, val2, val3, val4, val5, val6;
float val7, val8;
int limite_posizioni;
boolean ripetizione = false;
boolean autorizzazione = false;
boolean continuum = false;

void stile(){
  servo1.setEasingType(MODE);
  servo2.setEasingType(MODE);
  servo3.setEasingType(MODE);
  servo4.setEasingType(MODE);
  servo5.setEasingType(MODE);
  servo6.setEasingType(MODE);
}

void setup() {
  Serial.begin(115200);
  while (!start_pack){
    if (Serial.available()){
    lettura = Serial.readStringUntil('\n');
    if (getValue(lettura,',',0)=="setup"){
      servo1PPos = getValue(lettura,',',1).toInt();
      servo2PPos = getValue(lettura,',',2).toInt();
      servo3PPos = getValue(lettura,',',3).toInt();
      servo4PPos = getValue(lettura,',',4).toInt();
      servo5PPos = getValue(lettura,',',5).toInt();
      servo6PPos = getValue(lettura,',',6).toInt();
      limite_posizioni = getValue(lettura,',',7).toInt();
      start_pack = true;
    }
   }
  }
  posizioni = EEPROM.read(0);
  delay(1000);
  Serial.println(posizioni);
  servo1.attach(2, servo1PPos);
  servo2.attach(3, servo2PPos);
  servo3.attach(4, servo3PPos);
  servo4.attach(5, servo4PPos);
  servo5.attach(6, servo5PPos);
  servo6.attach(7, servo6PPos);
  stile();
}

//*******************************

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;
  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }
  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

//*******************************

void loop() {
  if (Serial.available()){
    lettura = Serial.readStringUntil('\n');
   if (getValue(lettura,',',0)=="p"){
      servo1PPos = getValue(lettura,',',1).toInt();
      servo2PPos = getValue(lettura,',',2).toInt();
      servo3PPos = getValue(lettura,',',3).toInt();
      servo4PPos = getValue(lettura,',',4).toInt();
      servo5PPos = getValue(lettura,',',5).toInt();
      servo6PPos = getValue(lettura,',',6).toInt();
      servo1.startEaseTo(servo1PPos, 65);
      servo2.startEaseTo(servo2PPos, 65);
      servo3.startEaseTo(servo3PPos, 65);
      servo4.startEaseTo(servo4PPos, 65);
      servo5.startEaseTo(servo5PPos, 65);
      servo6.startEaseTo(servo6PPos, 65);
   }
   if (getValue(lettura,',',0)=="s"){     //save
    if (limite_posizioni > posizioni){
      EEPROM.write((posizioni*8+1), servo1PPos);
      EEPROM.write((posizioni*8+2), servo2PPos);
      EEPROM.write((posizioni*8+3), servo3PPos);
      EEPROM.write((posizioni*8+4), servo4PPos);
      EEPROM.write((posizioni*8+5), servo5PPos);
      EEPROM.write((posizioni*8+6), servo6PPos);
      EEPROM.write((posizioni*8+7), getValue(lettura,',',1).toInt()*2);
      EEPROM.write((posizioni*8+8), getValue(lettura,',',2).toInt()*2);
      posizioni++;
      EEPROM.write(0, posizioni);
    }
   }
   if (lettura=="r"){      //reset
    if (posizioni>0){
      for (int i=posizioni*8+1; i<=(posizioni*8+8); i++){
        EEPROM.write(i, 0);
      }
      posizioni=posizioni-1;
      EEPROM.write(0, posizioni);
    }
   }
   if (lettura=="rn"){      //ripetizione on
    ripetizione = true;
    Serial.println("ok");
   }
   if (lettura=="rf"){     //ripetizione off
    ripetizione = false;
    continuum = false;
   }
   if (lettura=="e"){       //esegui
    autorizzazione = true;
  }
 }
  if (autorizzazione == true || (autorizzazione == true && ripetizione == true) || (ripetizione == true && continuum == true)){
  autorizzazione = false;
  if (ripetizione == true){
    continuum = true;
  }
  if (posizioni>0){
   for (int posa=0; posa<posizioni; posa++){
     val1 = EEPROM.read(posa*8+1);
     val2 = EEPROM.read(posa*8+2);
     val3 = EEPROM.read(posa*8+3);
     val4 = EEPROM.read(posa*8+4);
     val5 = EEPROM.read(posa*8+5);
     val6 = EEPROM.read(posa*8+6);
     val7 = EEPROM.read(posa*8+7)/2;
     val8 = EEPROM.read(posa*8+8)/2;
     azione(val1, val2, val3, val4, val5, val6, val7);
     delay(val7*1000);
     Serial.println("f," + String(val1) + "," + String(val2) + "," + String(val3) + "," + String(val4) + "," + String(val5) + "," + String(val6));  //fatto
     if (posa<(posizioni-1) || ripetizione == true){
       delay(val8*1000);
     }
    }
   }
  }
  delay(1);
}



void azione(int servo1Pos, int servo2Pos, int servo3Pos, int servo4Pos, int servo5Pos, int servo6Pos, float durata){
 durata=constrain(durata, 0.5, 10);
 servo1.startEaseTo(servo1Pos, abs(servo1Pos-servo1PPos)/durata);
 servo1PPos = servo1Pos;
 servo2.startEaseTo(servo2Pos, abs(servo2Pos-servo2PPos)/durata);
 servo2PPos = servo2Pos;
 servo3.startEaseTo(servo3Pos, abs(servo3Pos-servo3PPos)/durata);
 servo3PPos = servo3Pos;
 servo4.startEaseTo(servo4Pos, abs(servo4Pos-servo4PPos)/durata);
 servo4PPos = servo4Pos;
 servo5.startEaseTo(servo5Pos, abs(servo5Pos-servo5PPos)/durata);
 servo5PPos = servo5Pos;
 servo6.startEaseTo(servo6Pos, abs(servo6Pos-servo6PPos)/durata);
 servo6PPos = servo6Pos;
}
