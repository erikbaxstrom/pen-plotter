
class FileManager:
    """ Manage writing and reading (printing) printable files
     
    Methods:
        add_to_print_file(data: str): adds a string of gcode to the print
        start_print(): starts printing the gcode file
         """
    def __init__(self, print_controller):
        self.print_string = ''
        self.print_controller = print_controller
        pass

    def add_to_print_file(self, data):
        self.print_string += data.decode('utf-8')
        return
    
    def start_print(self):
        print('starting the print')
        self.print_controller.print_gcode(self.print_string)
    
    def clear_file(self):
        self.print_string = ''

