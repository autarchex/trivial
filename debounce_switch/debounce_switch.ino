//Two ways to debounce a switch input
//Both based on Jack Ganssle's advice at www.ganssle.com/debouncing-pt2.htm

//method 1 defines
#define switchInput 3    //input used for the single-switch debouncer snippet (method 1)

//method 2 defines and globals
#define DEB_CHECKS  10    //number of of checks before switch considered debounced via method 2
uint8_t debouncedState;
volatile uint8_t debState[DEB_CHECKS];  //circular array remembers bounce status of up to 8 switches

//test: rotary encoder
int line;
uint8_t rotA, rotB;              //encoder states

void setup(){
  //setup for method 1:
  pinMode(switchInput, INPUT_PULLUP);
  //setup for method 2:
  DDRB = 0x00;    //set data direction port b: all inputs
  PORTB = 0x3f;   //engage pullups on port b[5..0], corresponds to arduino ports [13..8]
  DDRB |= (1 << 1);  //set port b pin 1 as output
  PORTB &= ~(1 << 1);  //pull common pin low
  OCR0A = 0x33;   //arbitrary count-compare value for timer0 interrupt
  TIMSK0 |= _BV(OCIE0A);  //enable timer0 compare interrupt
  for(int i = 0; i < DEB_CHECKS; i++) debState[i] = 0;  //initialize to 0
  //setup for test
  Serial.begin(9600);
  line = 0;
  rotA = 0;
  rotB = 0;
}

void loop(){
  //B is on portB.2, A is on portB.0; com is on portB.1 and is set low
  //wait for switch activity on port 2 or 0
  boolean CW = false;
  boolean CCW = false;
  if(uint8_t change = detectSwitchActivity() & 0x05){
    rotA = (rotA << 1) & 0x0f;
    rotB = (rotB << 1) & 0x0f;
    if(debouncedState & (1<<0)) rotA |= 1;
    if(debouncedState & (1<<2)) rotB |= 1;
    if((rotA & 0x0f) == 0x03 && (rotB & 0x07) == 0x01) CCW = true;
    if((rotA & 0x07) == 0x01 && (rotB & 0x0f) == 0x03) CW = true;  
    if(CW || CCW) {
      line++;
      if(CW) Serial.print("CW");
      if(CCW) Serial.print("CCW");
      Serial.print("\n");
    }
  }
}
  
//METHOD 1: This debounces a single switch input.
//Call this from a timer interrupt.
//If switch is active-low, this returns false until 12 sequential closures are detected.
//It then returns true, once, so it can detect debounced edges.
boolean DebounceSwitch() {
  static uint16_t State = 0;  //current debounce status
  State = (State << 1) | !digitalRead(switchInput) | 0xe000;
  if(State == 0xf000) return true;
  return false;
}

//METHOD 2: This debounces an entire port; in this example, port B.
//MAKE SURE TO INIT DEBSTATE TO 0 FIRST
//This service routine called by timer0 interrupt; arduino defaults to trigger every millisecond.
//It only gathers port states every 5 ms.
SIGNAL(TIMER0_COMPA_vect) {
  static uint8_t ms = 0;
  static uint8_t index = 0;
  if(++ms > 5) {            //execute every 5 ms
    debState[index++] = PINB;  //save present port state and increment index
    if(index >= DEB_CHECKS) index = 0;  //wrap circular buffer at end
  }
}
//call this when you need to know if a button was pressed
//returns a state-changed mask identifying which switches changed; updates debouncedState with new state.
uint8_t detectSwitchActivity() {
  uint8_t i, j;
  uint8_t last = debouncedState;
  j = 0xff;
  for(i = 0; i < DEB_CHECKS; i++) j = j & debState[i];  //AND all previous states
  debouncedState = j;            //update debounced state variable
  return j ^ last;              //detect changes
}


  
