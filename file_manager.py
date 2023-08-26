
class file_manager:
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
        for code in self.print_string.split('\n'):
            print('processing code', code)
            if code[0] == ';':
                print('passing over a ;comment', code)
                pass
            self.print_controller.execute_gcode(code)
        self.print_controller.finish_print()
