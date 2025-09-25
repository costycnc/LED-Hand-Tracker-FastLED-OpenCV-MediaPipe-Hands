# LED Hand Tracker – FastLED + OpenCV + MediaPipe Hands

This project combines **Arduino with FastLED** and **computer vision in Python** using **OpenCV** and **MediaPipe Hands**.  
It allows controlling LED colors and brightness based on real-time hand movements captured from a webcam.

Check out the demo video on YouTube: [Watch here](https://www.youtube.com/shorts/u6FXnKp06Jg)



---

## 📦 Requirements

### Hardware
- Arduino Uno / Nano / Mega (or compatible board)  
- WS2812 / WS2812B LED strip  
- Appropriate power supply for the LED strip  

### Software
- Arduino IDE  
- Python 3.x  
- Python libraries: OpenCV, MediaPipe, PySerial  

---

## ⚙️ Hardware Setup

1. Connect the LED data pin to a digital pin on Arduino (e.g., D6).  
2. Connect LED GND and VCC to the proper power source.  
3. Connect Arduino GND to the LED power GND.  

---

## 🔹 Project Overview

- **Arduino / FastLED**: Controls the LED strip, receives commands via serial.  
- **Python / OpenCV & MediaPipe**: Tracks hand movements and sends brightness or color values to Arduino in real-time.  

---

## 🚀 Features

- Real-time hand tracking with webcam  
- LED brightness and color control based on hand gestures  
- Smooth fade and animation effects possible  
- Easily extensible for multi-hand tracking, custom colors, or interactive effects  

---

## 📌 Notes

- Make sure to use the correct serial port for your Arduino.  
- LED brightness ranges from 0 (off) to 255 (full brightness).  
- Can be combined with additional FastLED effects such as fading, rainbow cycles, or sparkles.  

---

## 📖 Resources

- [FastLED GitHub](https://github.com/FastLED/FastLED)  
- [OpenCV Python](https://opencv.org/)  
- [MediaPipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)  

---

## ✨ Contributing

Contributions are welcome! Feel free to suggest new effects, animations, or enhancements for hand tracking and LED interaction.
