
class FileManager:
    
    def __init__(self, print_controller):
        self.print_string = ''
        self.print_controller = print_controller
        pass

    def add_to_print_file(self, data):
        print('data', 'data')
        self.print_string += data.decode('utf-8')
        print('print_string', self.print_string)
        return
    
    def start_print(self):
        print('starting the print')
        # self.print_controller.activate_printer()
        self.print_controller.print_gcode(self.print_string)
