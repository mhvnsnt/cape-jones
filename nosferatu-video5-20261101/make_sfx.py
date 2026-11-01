import math, random, struct, wave
SR=44100; DUR=211.0; N=int(SR*DUR)
buf=[0]*N
random.seed(42)
def add(t, gen, amp=0.5):
    s=int(t*SR)
    for i, v in enumerate(gen()):
        if s+i < N: buf[s+i] += int(v*amp*32767)
def step():
    for i in range(int(0.09*SR)):
        yield math.sin(2*math.pi*80*i/SR)*math.exp(-i/(0.03*SR))
def snap():
    for i in range(int(0.05*SR)):
        yield (random.uniform(-1,1)*0.7 + math.sin(2*math.pi*2000*i/SR)*0.5)*math.exp(-i/(0.015*SR))
def whoosh():
    for i in range(int(0.30*SR)):
        yield random.uniform(-1,1)*math.sin(math.pi*i/(0.30*SR))
def bounce():
    for i in range(int(0.12*SR)):
        yield math.sin(2*math.pi*140*i/SR)*math.exp(-i/(0.04*SR))*0.6
loop=5.25; t=0.0
while t < DUR:
    for b in range(9):
        bt=t+b*0.583
        if bt>=DUR: break
        add(bt, step, amp=0.45)
        if b in (1,2): add(bt, bounce, amp=0.30)
        if b==3: add(bt, snap, amp=0.55); add(bt, whoosh, amp=0.40)
    t+=loop
out=bytearray()
for v in buf:
    v=max(-32767,min(32767,v)); out+=struct.pack('<h', v)
w=wave.open("/home/hatch/workspace/cape-jones-rig/nosferatu-video5-20261101/sfx-johnny-20261101.wav","wb")
w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(bytes(out)); w.close()
print("sfx written", len(buf)/SR, "s")
