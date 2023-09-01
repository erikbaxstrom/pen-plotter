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
; paint
G1 F2300.0 X35.96 Y19.62 Z-3.3
; paint
G1 F2300.0 X35.96 Y68.65 Z-3.3
; paint
G1 F2300.0 X68.65 Y52.31 Z-3.3
; paint
G1 F2300.0 X1.63 Y34.33 Z-3.3
; paint
G1 F2300.0 X34.33 Y17.98 Z-3.3
; paint
G1 F2300.0 X35.96 Y34.33 Z-3.3
; paint
G1 F2300.0 X34.33 Y52.31 Z-3.3
;
;
; Finish the Painting
G0 F4300 Z10 ; lift the brush
; G0 X0 Y85 ; stick out the finished print
G28
M84 ; Turn off stepper motors
;End of Gcode