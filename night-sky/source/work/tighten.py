# Shorten long pauses between sentences in the VO and shift word timings to match.
import json, subprocess, numpy as np, sys
SR=44100
raw=subprocess.run(["ffmpeg","-v","error","-i","assets/audio/vo_raw.mp3","-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
x=np.frombuffer(raw,dtype=np.float32).copy()
a=json.load(open('work/vo_alignment.json'))
ch=a['characters'];s=a['character_start_times_seconds'];e=a['character_end_times_seconds']
words=[];cur='';st=None
for c,cs,ce in zip(ch,s,e):
    if c.isspace():
        if cur: words.append([cur,st,pe]); cur=''
        continue
    if not cur: st=cs
    cur+=c; pe=ce
if cur: words.append([cur,st,pe])
# target pauses: last pause before "It's a museum." stays a touch longer
cuts=[]  # (t0,t1) to remove in original time
for i in range(1,len(words)):
    gap=words[i][1]-words[i-1][2]
    target=0.52 if words[i][0]=="It's" else 0.38
    if gap>target+0.05:
        # find quietest window inside the gap to remove (centre of the gap, avoiding 60ms around words)
        g0=words[i-1][2]+0.08; g1=words[i][1]-0.06
        rm=gap-target
        if g1-g0<rm: rm=max(0,g1-g0)
        c0=(g0+g1)/2-rm/2
        cuts.append((c0,c0+rm))
fade=int(0.008*SR)
out=[];pos=0
for c0,c1 in cuts:
    i0=int(c0*SR);i1=int(c1*SR)
    seg=x[pos:i0].copy()
    if len(out): seg[:fade]*=np.linspace(0,1,fade)
    seg[-fade:]*=np.linspace(1,0,fade)
    out.append(seg);pos=i1
seg=x[pos:].copy(); seg[:fade]*=np.linspace(0,1,fade); out.append(seg)
y=np.concatenate(out)
def shift(t):
    d=0
    for c0,c1 in cuts:
        if t>=c1: d+=c1-c0
        elif t>c0: d+=t-c0
    return t-d
nw=[{"id":f"w{i}","text":w,"start":round(shift(a1),3),"end":round(shift(b),3)} for i,(w,a1,b) in enumerate(words)]
json.dump(nw,open('work/words.json','w'),indent=1)
p=subprocess.run(["ffmpeg","-y","-v","error","-f","f32le","-ar",str(SR),"-ac","1","-i","-","-af","loudnorm=I=-16:TP=-1.5:LRA=7","-ar","44100","assets/audio/vo.wav"],input=y.tobytes())
print("removed %.2fs over %d cuts -> %.2fs"%(sum(c1-c0 for c0,c1 in cuts),len(cuts),len(y)/SR))
