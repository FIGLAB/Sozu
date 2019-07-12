import processing.net.*; 
import java.nio.*;

Client myClient; 

int dataIn; 
int receivedLen = 0;

byte [] byteBuffer = new byte[1024];

int NFFT = 256;
byte [] dataReceived = new byte[NFFT*4];
float[] fftResult = new float [NFFT];

void setup() { 
  size(400, 400); 
  myClient = new Client(this, "localhost", 8089); 
} 
 
void draw() { 
  background(0);
  
  while (myClient.available()>0) {
    
    int byteCount = myClient.readBytes(byteBuffer); 
    
    if(byteCount == dataReceived.length){
      System.arraycopy(byteBuffer, 0, dataReceived, 0, dataReceived.length);
      processData(dataReceived);
    }
    
    else{
      System.arraycopy(byteBuffer, 0, dataReceived, receivedLen, byteCount);
      receivedLen += byteCount;
      if(receivedLen == dataReceived.length){
        receivedLen = 0;
        processData(dataReceived);
      }
    } 
  }
  
  for(int i = 0; i < NFFT; i++){
    float xPos = map(i,0,NFFT,0,width);    
    stroke(255); 
    rect(xPos, 400, 1, -fftResult[i]*40);
  }
} 

void processData(byte[] buf){
  
  ByteBuffer temp = ByteBuffer.wrap(buf);
  for(int i = 0; i < NFFT; i++){
    fftResult[i] = temp.order(ByteOrder.LITTLE_ENDIAN).getFloat();
  }
}