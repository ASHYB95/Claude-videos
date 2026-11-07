# Builds the captioned storyboard sheet from stills/t_<t>.jpg
import sys
from PIL import Image, ImageDraw, ImageFont
D='films/delulu/stills/'
B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; R='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; I='/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf'
shots=[('1.8','1','Close · push-in on the meme','0:00–0:04',"3 days after her last text, he sends a meme. She starts typing… deletes it.",'"Three days of silence. Then… a meme."'),
('4.7','2','Full phone · whip-pan','0:04–0:07',"Export chat → share sheet → tap Delulu Check; whip-pan into the app, upload bar fills.",'"Upload the chat to Delulu Check."'),
('9.0','3','Medium · follow the mascot','0:07–0:11',"Delu, a pixel version of your logo, is born from the upload card and runs along every message row. Counter to 412, ▶▶ 8× tag.",'"It reads every single message…"'),
('12.9','4','Push-in · spotlight freeze','0:11–0:13.5',"Beat of silence, then VIBE CHECK: Interest Level counts to 62, Delu cheers on the card.",'"…and tells you where you actually stand."'),
('14.6','5','Pull up · quote card','0:13.5–0:15.3',"\u201cThey want the feeling, not the responsibility.\u201d lands.",'(music back in)'),
('18.4','6','Medium · drift down','0:15.3–0:19.5',"Doctor Delulu chat: \u201cSo I ignore him?\u201d → \u201cReply when you have something to say…\u201d, \u201cLet him make the plan.\u201d",'"Ask Doctor Delulu what to do next."'),
('22.0','7','Close · keyboard','0:19.5–0:23.5',"Back in the chat: Delulu Keyboard, GOD MODE → \u201ccooking your messages…\u201d → 3 replies; tap CHILL.",'"Then let the keyboard write the reply. In any app."'),
('24.75','8','Push-in to caret → send','0:23.5–0:25',"Pick a reply, send; Delu rides the sent message up.",'(send whoosh, 8-bit jump)'),
('29.0','9','Full · diegetic end title','0:25–0:30',"\u201cYour friends are too nice to tell you. Your chat already did.\u201d Logo + GET THE APP (clicked), 50,000+ people · free preview on your first chat.",'"Your friends are too nice to tell you. Your chat already did."')]
TW,TH=360,640; CAPH=250; cols=3; pad=24
rows=(len(shots)+cols-1)//cols
W=cols*TW+(cols+1)*pad; H=190+rows*(TH+CAPH+pad)+pad
img=Image.new('RGB',(W,H),(14,11,18)); d=ImageDraw.Draw(img)
fh=ImageFont.truetype(B,34); fb=ImageFont.truetype(B,19); fr=ImageFont.truetype(R,17); fi=ImageFont.truetype(I,18)
d.text((pad,28),"Delulu Check · \u201cYour chat already knows\u201d",fill=(192,46,224),font=fh)
d.text((pad,82),"Living Screencast · 9:16 · 30 s · real app screens redrawn in code, pixel mascot \u201cDelu\u201d, cursor = the user",fill=(235,230,245),font=fr)
d.text((pad,106),"Music: original upbeat R&B (92 BPM, keys, bass, tight kit + chiptune voice for Delu) · VO: warm young female (offline)",fill=(235,230,245),font=fr)
d.text((pad,136),"Storyboard frames rendered with the real drawing code; poses and timing get polished in production.",fill=(150,140,170),font=fr)
def wrap(s,font,w):
    out=[];line=''
    for word in s.split(' '):
        t=(line+' '+word).strip()
        if d.textlength(t,font=font)<=w: line=t
        else: out.append(line); line=word
    out.append(line); return out
for i,(t,n,fr_,tm,act,vo) in enumerate(shots):
    r,c=divmod(i,cols); x=pad+c*(TW+pad); y=190+r*(TH+CAPH+pad)
    im=Image.open(D+f't_{t}.jpg').resize((TW,TH),Image.LANCZOS); img.paste(im,(x,y))
    d.rectangle([x,y,x+TW,y+TH],outline=(90,70,110),width=2)
    d.rectangle([x,y,x+46,y+38],fill=(192,46,224)); d.text((x+15,y+7),n,fill=(255,255,255),font=fb)
    yy=y+TH+8
    d.text((x,yy),fr_,fill=(192,46,224),font=fb); yy+=26
    d.text((x,yy),tm,fill=(235,230,245),font=fb); yy+=28
    for l in wrap(act,fr,TW): d.text((x,yy),l,fill=(235,230,245),font=fr); yy+=21
    yy+=4
    for l in wrap(vo,fi,TW): d.text((x,yy),l,fill=(255,120,200),font=fi); yy+=22
img.save(sys.argv[1],quality=90); print(img.size)
