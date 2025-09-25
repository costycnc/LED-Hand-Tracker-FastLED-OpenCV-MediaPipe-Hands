#include <FastLED.h>

#define NUM_LEDS 22          // numero di LED nella striscia
#define DATA_PIN 8          // pin dati collegato alla striscia

CRGB leds[NUM_LEDS];

void setup() {
  Serial.begin(115200);     // comunicazione seriale con Python
  FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(10); 
}


void loop() {
  if (Serial.available() > 0) {
    String color = Serial.readStringUntil('\n');
    color.trim();

    CRGB c = CRGB::Black;

    if (color.equalsIgnoreCase("Rosso")) {
      c = CRGB::Red;
    } else if (color.equalsIgnoreCase("Verde")) {
      c = CRGB::Green;
    } else if (color.equalsIgnoreCase("Blu")) {
      c = CRGB::Blue;
    }

    // aggiorna tutta la striscia
    for (int i = 0; i < NUM_LEDS; i++) {
      leds[i] = c;
    }
    FastLED.show();
  }
}
