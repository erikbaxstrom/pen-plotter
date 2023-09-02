from filemanager import FileManager
from printcontrol import PrintController



STEPS_PER_MM = 2048 / 40  # 2048 steps per revolution. 40 mm per revolution
CANVAS_WIDTH = 812  # units: mm (measured as 31 31/32")
CANVAS_HEIGHT = 889  # units: mm (measured as 35")


    # file_manager.add_to_print_file(request.body)

    # file_manager.start_print()


    # print_controller.go_to_home()

    # print('req arg', request.args.getlist('active')[0], bool(request.args.getlist('active')[0]))
    # if request.args.getlist('active')[0] == "false":
    #     print_controller.deactivate_motors()


print_controller = PrintController(CANVAS_WIDTH, CANVAS_HEIGHT, STEPS_PER_MM)
file_manager = FileManager(print_controller)

try:
    print('tests start here')
    # print_controller.nudge(side=request.args.getlist('motor')[0], mm=request.args.getlist('mm')[0])
    print_controller.nudge(side='left', mm=20)
    print_controller.nudge(side='right', mm=20)

except:
    print('broke')
