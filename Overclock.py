import mmap, os

def setClock(newClock):
    with open("/dev/mem", os.O_RDWR) as f:
        CPPCR = (0x10 >> 2)

        m = newClock / 6
        if(m >= 200):
            m = 200
        
        if(m < 4):
            m = 4
        

        try:
            map.mmap(1024, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, 0x10000000) 
            map.seek(CPPCR)
            map.write((m << 24) | 0x090520)
            map.close()
        except Exception as ex:
            print(str(ex))