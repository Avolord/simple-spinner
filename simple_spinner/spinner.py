import threading
import time


class Spinner(threading.Thread):
    def __init__(self, iterable: iter, 
                 glyphs: list[chr] = ['-', '\\', '|', '/'], 
                 order: list[int] = None, 
                 glyphs_per_second: float = 10.0,
                 desc: str = ''):
        super().__init__()
        
        self.iterable = iterable
        self.running = False
        
        self.clock = time.monotonic
        
        self.glyphs = glyphs
        self.glyph_index = 0
        self.seconds_per_glyph = 1.0 / glyphs_per_second
        self.order = order if order else [i for i in range(len(glyphs))]
        self.desc = desc
            
    def next_glyph(self) -> chr:
        # Get the next glyph
        glyph = self.glyphs[self.order[self.glyph_index]]
        # Increment the glyph index
        self.glyph_index = (self.glyph_index + 1) % len(self.glyphs)
        return glyph
            
    def run(self, *args, **kwargs):
        #init a timer
        self.t1 = self.clock()
        
        desc = self.desc + ": " if self.desc else ""
        # Start the spinner
        while True:
            # check if the thread should be stopped
            if not self.running:
                # clear the line
                print(' ' * (len(desc) + 1), end='\r')
                # reset the glyph index
                self.glyph_index = 0
                # exit the loop 
                break
            
            # check if seconds_per_glyph has passed
            if self.clock() - self.t1 >= self.seconds_per_glyph:
                # update the timer
                self.t1 = self.clock()
                # print the next glyph
                print(f"{desc}{self.next_glyph()}", end='\r')
            
    def __iter__(self):
        # start the spinner
        self.start()
        
        for element in self.iterable:
            yield element
            
        # stop the spinner
        self.stop()
    
    def stop(self):
        # stop the spinner
        self.running = False
        self.join()
        
    def start(self):
        # start the spinner
        self.running = True
        super().start()
        
        
if __name__ == '__main__':
    for i in Spinner(range(10), desc="Loading"):
        time.sleep(0.1)
        
    print("Done")