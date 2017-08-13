
import numpy as np

class RunsFiles:
    def __init__(self, uut, files):
        self.uut = uut
        self.files = files
        
    def load(self):
        for f in self.files:
            with open(f, mode='r') as fp:
                self.uut.load_awg(fp.read())
            yield f        


class RainbowGen:
    NCYCLES = 5
    def offset(self, ch):
        return -9.0 + 8.0*ch/self.nchan;
    
    def rainbow(self, ch):
        return np.add(self.sw, self.offset(ch))
    
    def sin(self):
        nsam = self.nsam
        NCYCLES = self.NCYCLES    
        return np.sin(np.array(range(nsam))*NCYCLES*2*np.pi/nsam)   # sin, amplitude of 1 (volt)
        
    def sinc(self, ch):
        nsam = self.nsam
        nchan = self.nchan
        NCYCLES = self.NCYCLES
        xoff = ch*nsam/NCYCLES/10
        xx = np.array(range(-nsam/2-xoff,nsam/2-xoff))*NCYCLES*2*np.pi/nsam
        return [ np.sin(x)/x if x != 0 else 1 for x in xx ]
    
    def __init__(self, uut, nchan, nsam):
        self.uut = uut
        self.nchan = nchan
        self.nsam = nsam        
        self.sw = self.sin()        
        self.aw = np.zeros((nsam,nchan))
        for ch in range(nchan):
            self.aw[:,ch] = self.rainbow(ch)

    def load(self):        
        #for ch in range(self.nchan):
        for ch in range(8):             # convenient to plot 8
            aw1 = np.copy(self.aw)
            aw1[:,ch] = np.add(np.multiply(self.sinc(ch),5),2)
            print("loading array ", aw1.shape)
            self.uut.load_awg((aw1*(2**15-1)/10).astype(np.int16))           
            print("loaded array ", aw1.shape)
            yield ch
