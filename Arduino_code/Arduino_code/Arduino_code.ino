#include <mcp_can.h>
#include <SPI.h>

//SAMD core/
#ifdef ARDUINO_SAMD_VARIANT_COMPLIANCE
 #define SERIAL SerialUSB
#else
 #define SERIAL Serial
#endif

// Define Joystick connection pins 
#define UP     A1
#define DOWN   A3
#define LEFT   A2
#define RIGHT  A5
#define CLICK  A4
#define pot A0

//Define LED pins
#define LED2 8
#define LED3 7
#define LED4 4
#define STOP_BTN 9
#define LED5 3

// Value Limits
 #define P_MIN -12.5f // Position_min
 #define P_MAX 12.5f // Position_max
 #define V_MIN -76.0f // Vel_min
 #define V_MAX 76.0f // Vel_max
 #define KP_MIN 0.0f // kp_min
 #define KP_MAX 500.0f // kp_max
 #define KD_MIN 0.0f // kd_min
 #define KD_MAX 5.0f // kd_max
 #define T_MIN -12.0f // Torque_min
 #define T_MAX 12.0f //Torque_max

float map2(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

// Set values
float p_in = 0.0f;
float v_in = 0.0f;
float kp_in =0.0f;
float kd_in = 0.0f;
float t_in = 0.0;
// measured values
float p_out = 0.0f;
float v_out = 0.0f;
float t_out = 0.0f;

String id_s;
String p_out_s;
String t_out_s;
String volts;
String kp_in_s;
String coma = ",";
String total;
String py;
String mode = "\0";
String text1 = "Mode";
String text2 = " ";
String v_out_s;

// the cs pin of the version after v1.1 is default to D9
// v0.9b and v1.0 is default D10
const int SPI_CS_PIN = 10;
unsigned long on = 0;
int c_ounter = 0;
int enable = 0;
int sp = 0;

MCP_CAN CAN(SPI_CS_PIN);                                    // Set CS pin

void setup()
{
 SERIAL.begin(115200);
 SERIAL.setTimeout(50);
 delay(1000);
 while (CAN_OK != CAN.begin(CAN_1000KBPS))              // init can bus : baudrate = 500k
 {
   SERIAL.println("CAN BUS Shield init fail");
   SERIAL.println(" Init CAN BUS Shield again");
   delay(100);
 }
 SERIAL.println("CAN BUS Shield init ok!");

  // Initialize pins as necessary
  pinMode(UP,INPUT);
  pinMode(DOWN,INPUT);
  pinMode(LEFT,INPUT);
  pinMode(RIGHT,INPUT);
  pinMode(CLICK,INPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);
  pinMode(STOP_BTN, INPUT);
  pinMode(LED5, OUTPUT);
  pinMode(pot, INPUT);

  // Pull analog pins high to enable reading of joystick movements
  digitalWrite(UP, HIGH);
  digitalWrite(DOWN, HIGH);
  digitalWrite(LEFT, HIGH);
  digitalWrite(RIGHT, HIGH);
  digitalWrite(CLICK, HIGH);
  digitalWrite(pot, LOW);
  digitalWrite(STOP_BTN, LOW);

  // Write LED pins low to turn them off by default
  digitalWrite(LED2, LOW);
  digitalWrite(LED3, LOW);
  digitalWrite(LED4, LOW);
  digitalWrite(LED5, LOW);
  ExitMotorMode();
  Zero();
}

long previousMillis = 0;
void loop()
{
  //do something
/*
  float p_step = 0.01;
  if (digitalRead(UP)==LOW && (enable)==1) 
  {
    //move motor forward
    p_in = p_in + p_step;
  }
  if (digitalRead(DOWN)==LOW && (enable)==1)
  {
    //move motor backward
    p_in = p_in - p_step;
  }
  p_in = constrain(p_in, P_MIN, P_MAX);
  if (digitalRead(RIGHT)==LOW)
  {
    // Enable
    Zero();
    on = millis();
    enable = 1;
    delay(10);
    EnterMotorMode();
    digitalWrite(LED2, HIGH);
    digitalWrite(LED5, HIGH);
  }
  if (digitalRead(LEFT)==LOW)
  {
    // Disable
    Zero();
    enable = 0;
    delay(10);
    ExitMotorMode();
    digitalWrite(LED2, LOW);
    digitalWrite(LED5, LOW);
  }
*/
  if(digitalRead(STOP_BTN)==HIGH){
    // Disable
    sp = 1;

  }
  else if(digitalRead(STOP_BTN)==LOW && sp==1){
    //Disable
    Zero();
    enable = 0;
    delay(10);
    ExitMotorMode();
    digitalWrite(LED2, LOW);
    digitalWrite(LED5, LOW);
    delay(100);
    sp = 0;

  }

  int value = analogRead(pot);
  //SERIAL.println(value);
  float voltage = map2(value, 0, 1023, 0.0, 5.0);
  //float voltage = 1015;
  if (Serial.available()>0){
    py=Serial.readString();

    if(py=="0" && enable==1 && mode=="a"){
      kp_in = 0;
      kd_in = 0;
      t_in = 0;
    }
    else if (py=="1" && enable==1 && mode=="a"){
      kp_in = 0.75;
      kd_in = 1;

    }
    else if (py=="2" && enable==1 && mode=="a"){
      kp_in = 1.4;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="3" && enable==1 && mode=="a"){
      kp_in = 2;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="4" && enable==1 && mode=="a"){
      kp_in = 2.6;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="5" && enable==1 && mode=="a"){
      kp_in = 3.2;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="6" && enable==1 && mode=="a"){
      kp_in = 3.8;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="7" && enable==1 && mode=="a"){
      kp_in = 4.4;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="8" && enable==1 && mode=="a"){
      kp_in = 5;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="9" && enable==1 && mode=="a"){
      kp_in = 5.6;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="10" && enable==1 && mode=="a"){
      kp_in = 6.2;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="11" && enable==1 && mode=="a"){
      kp_in = 6.8;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="12" && enable==1 && mode=="a"){
      kp_in = 7.4;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="-1" && enable==1 && mode=="a"){
      kp_in = 0.75;
      kd_in = 1;

    }
    else if (py=="-2" && enable==1 && mode=="a"){
      kp_in = 1.4;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="-3" && enable==1 && mode=="a"){
      kp_in = 2;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="-4" && enable==1 && mode=="a"){
      kp_in = 2.6;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="-5" && enable==1 && mode=="a"){
      kp_in = 3.2;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="-6" && enable==1 && mode=="a"){
      kp_in = 3.8;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="-7" && enable==1 && mode=="a"){
      kp_in = 4.4;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="-8" && enable==1 && mode=="a"){
      kp_in = 5;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="-9" && enable==1 && mode=="a"){
      kp_in = 5.6;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="-10" && enable==1 && mode=="a"){
      kp_in = 6.2;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="-11" && enable==1 && mode=="a"){
      kp_in = 6.8;
      kd_in = 1;
      t_in = 0;
    }
    else if (py=="-12" && enable==1 && mode=="a"){
      kp_in = 7.4;
      kd_in = 1;
      t_in = 0;
    }
    else if(py=="0" && enable==1 && mode=="b"){
      t_in = 0;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="1" && enable==1 && mode=="b"){
      t_in = 1;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="2" && enable==1 && mode=="b"){
      t_in = 2;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="3" && enable==1 && mode=="b"){
      t_in = 3;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="4" && enable==1 && mode=="b"){
      t_in = 4;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="5" && enable==1 && mode=="b"){
      t_in = 5;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="6" && enable==1 && mode=="b"){
      t_in = 6;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="7" && enable==1 && mode=="b"){
      t_in = 7;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="8" && enable==1 && mode=="b"){
      t_in = 8;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="9" && enable==1 && mode=="b"){
      t_in = 9;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="10" && enable==1 && mode=="b"){
      t_in = 10;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="11" && enable==1 && mode=="b"){
      t_in = 11;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="12" && enable==1 && mode=="b"){
      t_in = 12;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="-1" && enable==1 && mode=="b"){
      t_in = -1;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="-2" && enable==1 && mode=="b"){
      t_in = -2;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="-3" && enable==1 && mode=="b"){
      t_in = -3;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="-4" && enable==1 && mode=="b"){
      t_in = -4;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="-5" && enable==1 && mode=="b"){
      t_in = -5;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="-6" && enable==1 && mode=="b"){
      t_in = -6;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="-7" && enable==1 && mode=="b"){
      t_in = -7;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="-8" && enable==1 && mode=="b"){
      t_in = -8;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="-9" && enable==1 && mode=="b"){
      t_in = -9;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="-10" && enable==1 && mode=="b"){
      t_in = -10;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="-11" && enable==1 && mode=="b"){
      t_in = -11;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="-12" && enable==1 && mode=="b"){
      t_in = -12;
      kp_in = 0;
      kd_in = 0;
    }
    else if (py=="999" && enable==1){
      kp_in = 0;
      kd_in = 0;
      t_in = 0;
      mode = "\0";
      enable = 0;
      py = "\0";
      ExitMotorMode();
      digitalWrite(LED2, LOW);
      digitalWrite(LED5, LOW);
      delay(10);
    }
    else if (py=="998" && enable==0){
      Zero();
      delay(10);
      digitalWrite(LED2, HIGH);
      digitalWrite(LED5, HIGH);
      enable = 1;
      EnterMotorMode();
    }
    else if (py=="997"){
      Zero();
      delay(10);
    }
    else if(py=="a"){
      mode = "a";
      kp_in = 0;
      kd_in = 0;
      t_in = 0;
      enable = 0;
    }
    else if(py=="b"){
      mode = "b";
      kp_in = 0;
      kd_in = 0;
      t_in = 0;
      enable = 0;
    }
  }
/*
 if (enable == 1){
      if (millis() - on > 50){
        if(c_ounter == 0){
          p_in = random(0.0, 20.0) / 100.0;
          c_ounter = 1;
        }
        else if(c_ounter == 1){
          p_in = random(0.0, 80.0) / 100.0;
          c_ounter = 0;
        }
        on = millis();
 } 
 }
 */
    // send CAN
  pack_cmd();

  // receive CAN
  if(CAN_MSGAVAIL == CAN.checkReceive())            // check if data coming
  {
    unpack_reply();
  }
  //print data
  //SERIAL.print(millis()-previousMillis);
  //previousMillis = millis();
  //SERIAL.print(" ");
  //SERIAL.print(p_in);
  //SERIAL.print(" ");
  //SERIAL.print(p_out);
  //SERIAL.print(" ");
  //SERIAL.print(v_out);
  //SERIAL.print(" ");
  //SERIAL.println(t_out);
  p_out_s = String(p_out, 2);
  t_out_s = String(t_out, 2);
  volts = String(voltage, 2);
  kp_in_s = String(kp_in, 2);
  v_out_s = String(v_out, 2);
  total = p_out_s+coma+t_out_s+coma+volts+coma+kp_in_s+coma+v_out_s;
  Serial.println(total);
  delay(100);

}

void EnterMotorMode(){
  // Enter Motor Mode (enable)
  byte buf[8];
  buf[0] = 0xFF;
  buf[1] = 0xFF;
  buf[2] = 0xFF;
  buf[3] = 0xFF;
  buf[4] = 0xFF;
  buf[5] = 0xFF;
  buf[6] = 0xFF;
  buf[7] = 0xFC;
  CAN.sendMsgBuf(0x01, 0, 8, buf);
}

void ExitMotorMode(){
  // Enter Motor Mode (enable)
  byte buf[8];
  buf[0] = 0xFF;
  buf[1] = 0xFF;
  buf[2] = 0xFF;
  buf[3] = 0xFF;
  buf[4] = 0xFF;
  buf[5] = 0xFF;
  buf[6] = 0xFF;
  buf[7] = 0xFD;
  CAN.sendMsgBuf(0x01, 0, 8, buf);
}

void Zero(){
  // Enter Motor Mode (enable)
  byte buf[8];
  buf[0] = 0xFF;
  buf[1] = 0xFF;
  buf[2] = 0xFF;
  buf[3] = 0xFF;
  buf[4] = 0xFF;
  buf[5] = 0xFF;
  buf[6] = 0xFF;
  buf[7] = 0xFE;
  CAN.sendMsgBuf(0x01, 0, 8, buf);
}

void pack_cmd(){
  byte buf[8];

  /// CAN Command Packet Structure ///
  /// 16 bit position command, between -4*pi and 4*pi
  /// 12 bit velocity command, between -30 and + 30 rad/s
  /// 12 bit kp, between 0 and 500 N-m/rad
  /// 12 bit kd, between 0 and 100 N-m*s/rad
  /// 12 bit feed forward torque, between -18 and 18 N-m
  /// CAN Packet is 8 8-bit words
  /// Formatted as follows.  For each quantity, bit 0 is LSB
  /// 0: [position[15-8]]
  /// 1: [position[7-0]] 
  /// 2: [velocity[11-4]]
  /// 3: [velocity[3-0], kp[11-8]]
  /// 4: [kp[7-0]]
  /// 5: [kd[11-4]]
  /// 6: [kd[3-0], torque[11-8]]
  /// 7: [torque[7-0]]

  /// limit data to be within bounds ///
  float p_des = constrain(p_in, P_MIN, P_MAX); //fminf(fmaxf(P_MIN, p_in), P_MAX);                    
  float v_des = constrain(v_in, V_MIN, V_MAX); //fminf(fmaxf(V_MIN, v_in), V_MAX);
  float kp = constrain(kp_in, KP_MIN, KP_MAX); //fminf(fmaxf(KP_MIN, kp_in), KP_MAX);
  float kd = constrain(kd_in, KD_MIN, KD_MAX); //fminf(fmaxf(KD_MIN, kd_in), KD_MAX);
  float t_ff = constrain(t_in, T_MIN, T_MAX); //fminf(fmaxf(T_MIN, t_in), T_MAX);
  /// convert floats to unsigned ints ///
  unsigned int p_int = float_to_uint(p_des, P_MIN, P_MAX, 16);            
  unsigned int v_int = float_to_uint(v_des, V_MIN, V_MAX, 12);
  unsigned int kp_int = float_to_uint(kp, KP_MIN, KP_MAX, 12);
  unsigned int kd_int = float_to_uint(kd, KD_MIN, KD_MAX, 12);
  unsigned int t_int = float_to_uint(t_ff, T_MIN, T_MAX, 12);
  /// pack ints into the can buffer ///

  buf[0] = p_int >> 8;                                       
  buf[1] = p_int & 0xFF;
  buf[2] = v_int >> 4;
  buf[3] = ((v_int & 0xF) << 4) | (kp_int >> 8);
  buf[4] = kp_int & 0xFF;
  buf[5] = kd_int >> 4;
  buf[6] = ((kd_int & 0xF) << 4) | (t_int >> 8);
  buf[7] = t_int & 0xFF;
  CAN.sendMsgBuf(0x01, 0, 8, buf);
}

void unpack_reply(){

  /// CAN Reply Packet Structure ///
  /// 16 bit position, between -4*pi and 4*pi
  /// 12 bit velocity, between -30 and + 30 rad/s
  /// 12 bit current, between -40 and 40;
  /// CAN Packet is 5 8-bit words
  /// Formatted as follows.  For each quantity, bit 0 is LSB
  /// 0: [position[15-8]]
  /// 1: [position[7-0]] 
  /// 2: [velocity[11-4]]
  /// 3: [velocity[3-0], current[11-8]]
  /// 4: [current[7-0]]

  byte len = 0;
  byte buf[8];
  CAN.readMsgBuf(&len, buf);

  unsigned long canId = CAN.getCanId();

  /// unpack ints from can buffer ///
  unsigned int id = buf[0];
  unsigned int p_int = (buf[1] << 8) | buf[2];
  unsigned int v_int = (buf[3] << 4) | (buf[4] >> 4);
  unsigned int i_int = ((buf[4] & 0xF) << 8) | buf[5];
  /// convert uints to floats ///
  p_out = uint_to_float(p_int, P_MIN, P_MAX, 16);
  v_out = uint_to_float(v_int, V_MIN, V_MAX, 12);
  t_out = uint_to_float(i_int, -T_MAX, T_MAX, 12);
} 

unsigned int float_to_uint(float x, float x_min, float x_max, int bits){
  /// Converts a float to an unsigned int, given range and number of bits ///
  float span = x_max - x_min;
  float offset = x_min;
  unsigned int pgg = 0;
  if (bits == 12){
    pgg = (unsigned int) ((x-offset)*4095.0/span);
  }
  if (bits == 16){
    pgg = (unsigned int) ((x-offset)*65535.0/span);
  }
  return pgg;
}

float uint_to_float(unsigned int x_int, float x_min, float x_max, int bits){
  /// converts unsigned int to float, given range and number of bits ///
  float span = x_max - x_min;
  float offset = x_min;
  float pgg = 0;
  if (bits == 12){
    pgg = ((float)x_int)*span/4095.0 + offset;
  }
  if (bits == 16){
    pgg = ((float)x_int)*span/65535.0 + offset;
  }
  return pgg;
}

// END FILE