# Builds compositions/captions.html from work/words.json (VO word timings after pause-tightening).
import json
W=json.load(open('work/words.json'))
# Each group: list of tokens (display, [word ids], highlight)
G=[
 [("You",[0],0),("don't",[1],0),("need",[2],0)],
 [("a",[3],0),("time",[4],1),("machine",[5],1)],
 [("to",[6],0),("look",[7],0),("into",[8],0),("the",[9],0),("past.",[10],1)],
 [("Step",[11],0),("outside",[12],0),("tonight",[13],0)],
 [("and",[14],0),("look",[15],1),("up…",[16],1)],
 [("you're",[17],0),("already",[18],0),("doing",[19],0),("it.",[20],0)],
 [("Light",[21],0),("has",[22],0),("a",[23],0),("speed",[24],1),("limit:",[25],1)],
 [("about",[26],0),("300,000",[27,28,29],1),("km",[30],0)],
 [("a",[31],0),("second.",[32],0)],
 [("So",[33],0),("the",[34],0),("Moon",[35],1),("you",[36],0),("see",[37],0)],
 [("is",[38],0),("1.3",[39,40,41],1),("seconds",[42],1),("old.",[43],0)],
 [("The",[44],0),("Sun?",[45],1)],
 [("8",[46],1),("minutes.",[47],1)],
 [("That",[48],0),("star?",[49],1)],
 [("Its",[50],0),("light",[51],0),("left",[52],0)],
 [("hundreds,",[53],0)],
 [("even",[54],0),("thousands,",[55],1)],
 [("of",[56],0),("years",[57],0),("ago.",[58],0)],
 [("You're",[59],0),("seeing",[60],0)],
 [("every",[61],1),("era",[62],1),("at",[63],0),("once.",[64],0)],
 [("The",[65],0),("night",[66],0),("sky",[67],0)],
 [("isn't",[68],0),("a",[69],0),("photograph.",[70],1)],
 [("It's",[71],0),("a",[72],0),("museum.",[73],1)],
]
LAST_END=26.30
groups=[]
for gi,g in enumerate(G):
    st=W[g[0][1][0]]['start']; en=W[g[-1][1][-1]]['end']
    groups.append([st,en,g])
for i,(st,en,g) in enumerate(groups):
    s=max(0.0, st-0.06) if i==0 else max(st-0.06, groups[i-1][4] if len(groups[i-1])>4 else 0)
    groups[i].append(round(s,3))  # [3]=open
for i in range(len(groups)):
    st,en,g,op=groups[i]
    if i+1<len(groups):
        nxt=groups[i+1][3]
        close=nxt if nxt-en<0.6 else en+0.35
    else: close=LAST_END
    groups[i].append(round(close,3))  # [4]=close
# make sure next open >= this close
for i in range(1,len(groups)):
    if groups[i][3]<groups[i-1][4]: groups[i][3]=groups[i-1][4]
html=[]; js=[]
for i,(st,en,g,op,cl) in enumerate(groups):
    gid=f"cg{i}"
    spans=[]
    for j,(txt,ids,hl) in enumerate(g):
        wid=f"{gid}-w{j}"
        if hl:
            spans.append(f'<span class="w hlw" id="{wid}"><span class="band" id="{wid}-b"></span><span class="t">{txt}</span></span>')
        else:
            spans.append(f'<span class="w" id="{wid}">{txt}</span>')
        t=W[ids[0]]['start']-op
        js.append(f'  tl.fromTo("#{wid}",{{opacity:0.38}},{{opacity:1,duration:0.08,ease:"none"}},{op+max(0,t):.3f});')
        if hl:
            bt=op+max(0,t-0.02)
            js.append(f'  tl.fromTo("#{wid}-b",{{scaleX:0}},{{scaleX:1,duration:0.16,ease:"power2.out"}},{bt:.3f});')
            js.append(f'  tl.set("#{wid} .t",{{color:"#fbf6ea",textShadow:SH}},{op:.3f});')
            js.append(f'  tl.set("#{wid} .t",{{color:"#16213e",textShadow:"none"}},{bt+0.05:.3f});')
    dur=round(cl-op,3)
    html.append(f'    <div id="{gid}" class="cg clip" data-start="{op}" data-duration="{dur}" data-track-index="0"><div class="line">{" ".join(spans)}</div></div>')
    js.append(f'  tl.fromTo("#{gid}",{{opacity:1}},{{opacity:0,duration:0.1,ease:"power2.in",immediateRender:false}},{cl-0.1:.3f});')
out=f'''<template>
  <style>
    @font-face {{ font-family: "Barlow"; font-weight: 800; src: url("assets/fonts/barlow-latin-800-normal.woff2") format("woff2"); }}
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .cg {{ position: absolute; left: 0; top: 1168px; width: 1080px; height: 150px; overflow: visible; }}
    .cg .line {{
      position: absolute; left: 90px; right: 90px; bottom: 18px; text-align: center;
      font-family: "Barlow", sans-serif; font-weight: 800; font-size: 68px; line-height: 1.08; letter-spacing: -.005em;
      color: #fbf6ea; text-shadow: 0 3px 0 rgba(0,0,0,.35), 0 0 18px rgba(0,0,0,.6), 0 0 4px rgba(0,0,0,.5);
    }}
    .w {{ display: inline-block; position: relative; }}
    .hlw {{ isolation: isolate; }}
    .hlw .band {{ position: absolute; left: -8px; right: -8px; top: 8%; bottom: 2%; background: #ffd43b; z-index: 0; transform-origin: 0% 50%;
      box-shadow: 0 4px 10px rgba(0,0,0,.35); }}
    .hlw .t {{ position: relative; z-index: 1; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(html)}
  </div>
  <script>
  (function () {{
  const tl = gsap.timeline({{ paused: true }});
  const SH = "0 3px 0 rgba(0,0,0,.35), 0 0 18px rgba(0,0,0,.6), 0 0 4px rgba(0,0,0,.5)";
{chr(10).join(js)}
  window.__timelines["captions"] = tl;
  }})();
  </script>
</template>
'''
open('compositions/captions.html','w').write(out)
for i,(st,en,g,op,cl) in enumerate(groups): print(i,op,cl,' '.join(t for t,_,_ in g))
