# Ansh's Digital Audio Clinic

![Project Screenshot](screenshot.png)

## About The Project
For my final project, I built "Ansh's Digital Audio Clinic," an interactive GUI hearing test. This project is deeply personal to me because I am half deaf myself. I know firsthand how gradual and sneaky hearing loss can be, so I wanted to build something that could help people detect early warning signs before they get worse. 

It actually started out as a basic text-based terminal script asking simple "yes/no" symptom questions. But I knew if I wanted to genuinely help people, I had to push myself to build a real graphical app that could physically test their hearing thresholds. 

## Technical Challenges & Learning
The technical side was a huge learning curve. I originally wanted to just play pre-recorded .mp3 files for the 1000Hz, 4000Hz, and 8000Hz tones, but standard audio libraries kept crashing or feeling clunky. I ended up using AI as a coding tutor to figure out how to synthesize the audio natively. It taught me how to use `numpy` to mathematically generate sine waves and `sounddevice` to pan the audio perfectly to the left or right ear, mimicking how a real clinical audiogram works!

I also spent a lot of time fighting with the UI. Standard Mac buttons wouldn't let me change their background colors, so I learned how to build custom flat buttons using `Label` widgets and event binding to create hover animations. 

## Accessibility First
Since I was already thinking heavily about accessibility with the audio test, I also implemented an Okabe-Ito inspired dark theme so the "Yes/No" buttons (Teal and Orange) are completely accessible for colorblind users. 

## Download and Run
You can download the standalone, ready-to-use versions of this app for Mac and Windows in the **Releases** section on the right side of this page!