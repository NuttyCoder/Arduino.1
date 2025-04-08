int  trig=10;
int echo=8;
long int t;
float d;
void setup() {
 Serial.begin(9600);
 pinMode(trig,OUTPUT);
 pinMode(echo,INPUT);
 

}

void loop() {
  digitalWrite(trig,LOW);
  delayMicroseconds(2);
  digitalWrite(trig,HIGH);
  delayMicroseconds(10);
  t=pulseIn(echo,HIGH);
  d=0.34*(t/2);
  Serial.print("distance=");
  Serial.println(d);  
  delayMicroseconds(10);
  
  
  
}
