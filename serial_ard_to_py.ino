void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
//Serial.println("Initialization");
pinMode(12,OUTPUT);
digitalWrite(12, LOW);
//Serial.println("Initialization complete!");

}
char state =0;
void loop() {
  // put your main code here, to run repeatedly:
//Serial.println("hello");
if (Serial.available()) {   
  state=Serial.read();
  Serial.print(state);
  if(state=='1'){
    Serial.println("OFF");
    digitalWrite(12,LOW);
    
  }else if(state=='0') {
    
    Serial.println("ON");
    digitalWrite(12,HIGH);
    
       }
 }

}
