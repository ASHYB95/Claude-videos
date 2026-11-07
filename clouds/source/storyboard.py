# Builds the captioned storyboard sheet from stills/t_<t>.jpg
import sys
from PIL import Image, ImageDraw, ImageFont
D='films/clouds/stills/'
B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; R='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; I='/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf'
shots=[('1.8','0','Wide sky · slow push → tilt down','0:00–0:06',"Result first: a smiling cloud drifts in the sky; title card stamps on; the camera tilts down the column of air to Professor Nimbus pointing up.",'"Ever wondered how a cloud is made? It takes just four steps."'),
('9.8','1','Full · medallion iris + call-out','0:06–0:12',"WARM: medallion 1 stamps on the sun and irises in (mint sky). She points sun → lake; call-out shows the warm surface shimmering.",'"Step one. The sun warms water in seas, lakes and puddles."'),
('16.0','2','Full → tall · tilt with the pointer','0:12–0:19',"RISE: dotted peach vapour lifts off the lake; her pointer traces it up as the camera climbs. Tags: water vapour · invisible / warm air rises.",'"Step two. Some of it turns into invisible water vapour, and rises with the warm air."'),
('24.0','3','Tall column · iris "3", held','0:19–0:27',"COOL: an altitude ruler draws on; a bubble of rising air grows wider (arrows) while its thermometer drops 20 → 0 °C, a tick at each km.",'"Step three. As the air climbs, it spreads out and cools. Nearly ten degrees for every kilometre."'),
('30.6','4a','Close · round call-out (native scale)','0:27–0:33',"CONDENSE: inside the magnifier, vapour dots drift; specks of dust and salt pop in, then the vapour clings to them.",'"Step four. Cool air can\u2019t hold as much vapour. It clings to specks of dust and salt\u2026"'),
('34.4','4b','Call-out · silence beat → plink','0:33–0:36',"A beat of total silence, then each speck becomes a droplet (celesta plink); thousands more bunch into a puff. Tag: 1 droplet ≈ 0.02 mm.",'"\u2026and becomes tiny droplets."'),
('40.5','P','Pull back · held summary','0:36–0:42',"Droplets swirl into place; the cloud pops with a sunburst; four medallions stamp in a row: WARM · RISE · COOL · CONDENSE (≥ 3 s still).",'"Billions of droplets, side by side. That\u2019s a cloud."'),
('45.4','T','Full · colour-block wipe','0:42–0:46.6',"Tip: one droplet swells and falls; rain follows; she pops a peach umbrella.",'"And when the droplets grow too heavy\u2026 they fall as rain."'),
('47.9','E','Iris out','0:46.6–0:48.5',"The iris closes on the cloud; title card on ink.",'(vibraphone tremolo)')]
TW,TH=360,640; CAPH=250; cols=3; pad=24
rows=(len(shots)+cols-1)//cols
W=cols*TW+(cols+1)*pad; H=190+rows*(TH+CAPH+pad)+pad
img=Image.new('RGB',(W,H),(246,239,226)); d=ImageDraw.Draw(img)
fh=ImageFont.truetype(B,34); fb=ImageFont.truetype(B,19); fr=ImageFont.truetype(R,17); fi=ImageFont.truetype(I,18)
d.text((pad,28),"How a Cloud Is Made",fill=(150,110,200),font=fh)
d.text((pad,82),"Mid-century Cartoon · 9:16 · ~48 s · 4 numbered steps up a column of air · pastel palette",fill=(46,38,34),font=fr)
d.text((pad,106),"Music: original cool jazz (vibraphone, flute, walking bass, brushes) · VO: calm classroom narrator, British male (offline)",fill=(46,38,34),font=fr)
d.text((pad,136),"Storyboard frames rendered with the real drawing code; poses and timing get polished in production.",fill=(120,110,100),font=fr)
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
    d.rectangle([x,y,x+TW,y+TH],outline=(46,38,34),width=2)
    d.rectangle([x,y,x+46,y+38],fill=(150,110,200)); d.text((x+15,y+7),n,fill=(255,255,255),font=fb)
    yy=y+TH+8
    d.text((x,yy),fr_,fill=(150,110,200),font=fb); yy+=26
    d.text((x,yy),tm,fill=(46,38,34),font=fb); yy+=28
    for l in wrap(act,fr,TW): d.text((x,yy),l,fill=(46,38,34),font=fr); yy+=21
    yy+=4
    for l in wrap(vo,fi,TW): d.text((x,yy),l,fill=(170,100,90),font=fi); yy+=22
img.save(sys.argv[1],quality=90); print(img.size)
