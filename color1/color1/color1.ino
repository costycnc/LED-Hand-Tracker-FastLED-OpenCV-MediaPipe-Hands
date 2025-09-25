#include <FastLED.h>

#define NUM_LEDS 10       // numero totale di LED
#define DATA_PIN 8        // pin collegato ai WS2812
CRGB leds[NUM_LEDS];
CRGB currentColor = CRGB::Red;
int value=10;

String inputString = "";  // buffer per dati seriali

void setup() {
  Serial.begin(115200);
  FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS);
    FastLED.setBrightness(10);  // luminosità iniziale (0-255)
}

void loop() {
  // Leggi dati da seriale
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      processCommand(inputString);
      inputString = "";
    } else {
      inputString += inChar;
    }
  }
}

void processCommand(String cmd) {
  cmd.trim();

  if (cmd.startsWith("SLIDER:")) {
    value = cmd.substring(7).toInt();  // estrai numero dopo "SLIDER:"
    Serial.print("Slider value: ");
    Serial.println(value);

      // Accendi i LED da 1 fino a "value"
    FastLED.clear();
    for (int i = 0; i < value ; i++) {
      leds[i] = currentColor;  // puoi cambiare colore
    }
    FastLED.show();
  }

  else if (cmd == "RED") {
    currentColor=CRGB::Red;
      // Accendi i LED da 1 fino a "value"
    FastLED.clear();
    for (int i = 0; i < value ; i++) {
      leds[i] = currentColor;  // puoi cambiare colore
    }
    FastLED.show();
  }

  else if (cmd == "GREEN") {
    currentColor=CRGB::Green;
      // Accendi i LED da 1 fino a "value"
    FastLED.clear();
    for (int i = 0; i < value; i++) {
      leds[i] = currentColor;  // puoi cambiare colore
    }
    FastLED.show();
  }

  else if (cmd == "BLUE") {
    currentColor=CRGB::Blue;
      // Accendi i LED da 1 fino a "value"
    FastLED.clear();
    for (int i = 0; i < value; i++) {
      leds[i] = currentColor;  // puoi cambiare colore
    }
    FastLED.show();
  }
}


