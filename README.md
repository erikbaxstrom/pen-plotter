# Overview

### Why?

Pen Plotters are cool. Genearative art is cool.

I fell in love with the aestehtic of pen plots when I saw [this video](https://youtu.be/gLG6Mp4n-Ms?si=5o8p-6Cip7ZlzuvK) on youtube. There's something magical about controlling the movement of a pen with a robot. And there a lot of cool possibilities with algorithmically generated art, and much of the [original computer generated art](https://piratefsh.github.io/2019/01/07/computer-art-history-part-2.html) was drawn with pen plotters.

### Photos

The plotter drawing a Hilbert Curve during testing.
![photo](./plotterBuild/overview.JPG)

A close-up of the electronics
![photo](./plotterBuild/electronics.JPG)

# Project Goals

- Designed and build a pen plotter with a web interface where you can upload gcode vector files and plot them on paper.
- Deepen my understanding of Python

### Existing Implementations

There are many implementations of pen plotters using Arduino microcontrollers, including Makelangelo, Polargraph, and versions of the GRBL firmware, not to mention the Maslow CNC and countless other hacked-together CNC devices.

Most of these implementations use Arduio boards and require either direct USB connection to a computer or use a rotary encoder and display built into the plotter.

# Design Goals

### Compact and Easily Stored

I have multiple hobbies, and want a plotter that doesn't take up floor or desk space. When not in use, I want to easily store it in a closet.

### Inexpensive and Simple Construction

As few parts as possible. Motors, belts, microcontrollers, etc should be widely available and inexpensive. Parts that require fabrication should not require specialized or precision tools.

### Web Interface Controls

Controlling the plotter through a web interface requires fewer parts and is more versatile than an onboard display and control interface, and does not require a USB connection to be maintained through the duration of the print.

### Support Common Vector File Formats

There is no universal standard for pen plotters, especially for hobby pen plotters. However, there are some common formats. On research, gcode (ubiquitous in CNC machining) is a common format and is easy to implement. Some generative art programs and graphics editors (like Inkscape) can generate gcode, but more commonly save files in SVG format. Since past work I've done in generative art uses gcode, I implemented gcode first.

# Hardware

### Raspberry Pi Pico W Microcontroller

It's inexpensive, powerful, has plenty of memory and disk space, lots of I/O, and there's a version with WiFi built in. It also has unique I/O functionality that allows outputting bit sequences without using processor cycles.

### 28BYJ-48 Stepper Motors

Inexpensive motors that are reasonable accurate (if slow). Commonly sold with ULN2003 motor drivers included.

### 2GT 6mm Pulleys and Belts

Standard size for 3D printers, and therefore easily acquired.

# Tech Stack

- MicroPython for backend and plotter control
- MicroDot library for web backend
- Vanilla JavaScript web frontend

# Planned Additional Features

- Pen lifter (currently, it only draws one continuous line)
- SD Card support to enable much larger print files
- Provide better feedback about plotter status through the web UI
- Auto-homing of the pen
