; Basic Printer Settings
M140 S0 ;set bed temp to zero. don't wait
M104 S0 ; set hotend temp to zero. don't wait
G21 ; use metric
G90 ; use absolute positioning
M107 ; turn fan off
G28 ; home the print head
; Set up the coordinate system
G0 F4320 Z15 ; lift brush
G0 F4320 X10 Y35 ; move to X10 Y35
G92 X0 Y0 Z0 ; set the zero point to the current coordinates
;
; move
G0 F90 Z-2.25
G0 F4300 X2.59 Y0.0
G0 F90 Z-3.5
; paint
G1 F4300.0 X2.59 Y5.18 Z-3.9
; move
G0 F90 Z-2.25
G0 F4300 X0.0 Y7.76
G0 F90 Z-3.6
; paint
G1 F4300.0 X10.35 Y7.76 Z-3.6
; move
G0 F90 Z-2.25
G0 F4300 X0.0 Y12.94
G0 F90 Z-3.6
; paint
G1 F4300.0 X10.35 Y12.94 Z-3.6
; move
G0 F90 Z-2.25
G0 F4300 X0.0 Y18.12
G0 F90 Z-3.7
; paint
G1 F4300.0 X10.35 Y18.12 Z-3.7
; move
G0 F90 Z-2.25
G0 F4300 X2.59 Y20.71
G0 F90 Z-3.5
; paint
G1 F4300.0 X2.59 Y25.88 Z-3.9
; move
G0 F90 Z-2.25
G0 F4300 X2.59 Y25.88
G0 F90 Z-4.2
; paint
G1 F4300.0 X2.59 Y31.06 Z-3.2
; move
G0 F90 Z-2.25
G0 F4300 X0.0 Y33.65
G0 F90 Z-3.7
; paint
G1 F4300.0 X10.35 Y33.65 Z-3.7
; move
G0 F90 Z-2.25
G0 F4300 X2.59 Y36.24
G0 F90 Z-3.6
; paint
G1 F4300.0 X2.59 Y41.41 Z-3.8
; move
G0 F90 Z-2.25
G0 F4300 X2.59 Y41.41
G0 F90 Z-3.3
; paint
G1 F4300.0 X2.59 Y46.59 Z-4.1
; move
G0 F90 Z-2.25
G0 F4300 X0.0 Y49.18
G0 F90 Z-3.7
; paint
G1 F4300.0 X10.35 Y49.18 Z-3.7
; move
G0 F90 Z-2.25
G0 F4300 X5.18 Y2.59
G0 F90 Z-3.5
; paint
G1 F4300.0 X15.53 Y2.59 Z-3.5
; move
G0 F90 Z-2.25
G0 F4300 X7.76 Y5.18
G0 F90 Z-3.7
; paint
G1 F4300.0 X7.76 Y10.35 Z-3.7
; move
G0 F90 Z-2.25
G0 F4300 X100.94 Y31.06
G0 F90 Z-4.1
; paint
G1 F4300.0 X100.94 Y36.24 Z-3.3
; move
G0 F90 Z-2.25
G0 F4300 X98.35 Y38.82
G0 F90 Z-3.5
; paint
G1 F4300.0 X108.71 Y38.82 Z-3.5
; move
G0 F90 Z-2.25
G0 F4300 X98.35 Y44.0
G0 F90 Z-3.3
; paint
G1 F4300.0 X108.71 Y44.0 Z-3.3
; move
G0 F90 Z-2.25
G0 F4300 X98.35 Y49.18
G0 F90 Z-3.7
; paint
G1 F4300.0 X108.71 Y49.18 Z-3.7
;
; Finish the Painting
G0 F4300 Z10 ; lift the brush
; G0 X0 Y85 ; stick out the finished print
G28
M84 ; Turn off stepper motors
;End of Gcode