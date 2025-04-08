void setup() {
  Serial.begin(9600);
  int input=6;
  pinMode(input,INPUT);
 

}

void loop() {
 
int v;
v=digitalRead(6);
Serial.println(v);
}
