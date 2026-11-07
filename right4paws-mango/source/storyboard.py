# Builds the captioned storyboard sheet from stills/t_<t>.jpg
import sys
from PIL import Image, ImageDraw, ImageFont
D='films/mango/stills/'
B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; R='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; I='/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf'
shots=[('0.6','1','ECU → medium · pull out','0:00–0:04.5',"A crayon finishes Mango's eye; pull back: he's uncoloured, chin on paws.",'"Right. Confession time. I used to be a terribly fussy eater."'),
('7.5','2','Medium · truck right','0:04.5–0:10','A bowl of brown pellets draws itself; sniff… "hmph", nose turned up.','"Same brown pellets. Every. Single. Day."'),
('11.8','3','Medium → wide · tilt up','0:10–0:14','Thump! The Ultimate Diet pack drops in and gets scribbled red.','"Then one morning… something new turned up."'),
('18.8','4','Full · follow down','0:14–0:20.4','Chicken, eggs, carrot, berries, sardine, pumpkin pop out and colour in on the beat; Mango colours in and jumps up.','"Real chicken. Fresh eggs. Veggies, berries… even sardines!"'),
('21.1','5','Wide · page turn','0:20.4–0:22','The page turns to a new morning; the sun clocks in.','"Now I wake up thinking about breakfast."'),
('25.5','6','Locked medium · slow push','0:22–0:28','Very good boy by his red bowl; eyes flick clock ↔ bowl on the beat. Music stops; tick… tick…','"I sit by my bowl. I wait. Very nicely."'),
('29.6','7','Medium · held','0:28–0:30.6','Flakes pour (first big sound after the silence); he dives in.','(crunch, munch)'),
('36.0','8','Close → wide · pull out + red wash','0:30.6–0:37','Push in on a beaming face, hearts; pull out as a brand-red wash reveals the hidden white-wax "Raw Made Right".','"Best. Bit. Of my day." / "Right4Paws Ultimate Diet. Raw, made right."'),
('39.5','9','Full page · held','0:37–0:40','End card in white crayon on the red: RIGHT4PAWS · Ultimate Diet · Medium & Maxi Adult, with the pack.','(music-box ping, final chord)')]
TW,TH=360,640; CAPH=250; cols=3; pad=24
rows=(len(shots)+cols-1)//cols
W=cols*TW+(cols+1)*pad; H=190+rows*(TH+CAPH+pad)+pad
img=Image.new('RGB',(W,H),(251,239,228)); d=ImageDraw.Draw(img)
fh=ImageFont.truetype(B,34); fb=ImageFont.truetype(B,19); fr=ImageFont.truetype(R,17); fi=ImageFont.truetype(I,18)
d.text((pad,28),"Mango's Mealtime · Right4Paws Ultimate Diet",fill=(224,38,43),font=fh)
d.text((pad,82),"Crayon Picture Book · 9:16 · ~40 s · one camera, no cuts, over two picture-book pages",fill=(58,36,32),font=fr)
d.text((pad,106),"Score: Minuet in G (Bach-era, public domain), chamber arrangement · VO: Mango, playful, mild British",fill=(58,36,32),font=fr)
d.text((pad,136),"Storyboard frames rendered with the real drawing code; poses and timing get polished in production.",fill=(120,100,90),font=fr)
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
    d.rectangle([x,y,x+TW,y+TH],outline=(58,36,32),width=2)
    d.rectangle([x,y,x+46,y+38],fill=(224,38,43)); d.text((x+15,y+7),n,fill=(255,255,255),font=fb)
    yy=y+TH+8
    d.text((x,yy),fr_,fill=(224,38,43),font=fb); yy+=26
    d.text((x,yy),tm,fill=(58,36,32),font=fb); yy+=28
    for l in wrap(act,fr,TW): d.text((x,yy),l,fill=(58,36,32),font=fr); yy+=21
    yy+=4
    for l in wrap(vo,fi,TW): d.text((x,yy),l,fill=(140,60,50),font=fi); yy+=22
img.save(sys.argv[1],quality=90); print(img.size)
