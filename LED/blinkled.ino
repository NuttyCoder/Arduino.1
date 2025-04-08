int LED=5;
void setup() {

pinMode(LED,OUTPUT);
}

void loop(){
  digitalWrite(LED,HIGH);
  delay(100);
  digitalWrite(LED,LOW);

}
