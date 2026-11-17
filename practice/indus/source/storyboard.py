# Builds the captioned storyboard sheet from stills/t_<t>.jpg
import sys
from PIL import Image, ImageDraw, ImageFont
D='films/indus/stills/sb/'
B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; R='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; I='/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf'
shots=[('4.5','1','Street · slow travel','0:00–0:08',"Dawn on a brick street by the Indus. Drain slabs lift to show water flowing; people carry pots; a reed boat on the river. Painted: 2600 BCE.",'"Four and a half thousand years ago, while Egypt built its pyramids, a city on the Indus had drains under every street."'),
('12.6','2','Scale jump · rise to wide','0:08–0:15',"The camera rises over the whole city: the citadel mound with the Great Bath and granary, the grid of the lower town. Painted: MOHENJO-DARO.",'"This is Mohenjo-daro. With Harappa, it was the heart of the Indus Valley Civilisation."'),
('16.0','3a','Wide · order lighting','0:15–0:16.7',"Every street lights up in the accent, east–west then north–south: the grid.",'"Streets ran in a grid."'),
('18.9','3b','Push in · held','0:16.7–0:19.6',"A stack of real bricks laid up as one big brick; its edges trace in the accent: 1, 2, 4. Painted on clear paving: 1 : 2 : 4 · every brick, in every city.",'"Bricks were baked to the same proportions."'),
('21.6','3c','Lid off · rise','0:19.6–0:22',"The roof lifts off a house: courtyard, well, a bathing platform; a dashed line follows the water out to the street drain.",'"Most homes had their own bathroom."'),
('26.0','4','Travel to the market','0:22–0:27.6',"Bales get stamped with seals (accent marks); a bullock cart passes. The script lands on the street sign by sign, ending in a big ?",'"Merchants stamped their goods with seals, in a script no one can read, to this day."'),
('31.5','5','Rise to wide · colour drains','0:27.6–0:34.6',"Painted: 1900 BCE. The river slides away, sand drifts into the streets, the colour drains, and people walk east out of the city.",'"Around 1900 BCE, the rivers shifted, the monsoon weakened, and the cities emptied."'),
('38.6','6a','Over the dunes · held','0:34.6–0:40.4',"The houses sink beneath dunes. 1922: archaeologists in sun hats uncover brick walls, course by course, and colour starts to return.",'"Four thousand years later, archaeologists dug into a mound called Mohenjo-daro…"'),
('44.0','6b','Pull back · held end','0:40.4–0:45.5',"The title paints itself on the sand beside the excavated houses: MOHENJO-DARO · the Mound of the Dead.",'"…The Mound of the Dead."')]
TW,TH=560,315; CAPH=230; cols=3; pad=24
rows=(len(shots)+cols-1)//cols
W=cols*TW+(cols+1)*pad; H=190+rows*(TH+CAPH+pad)+pad
img=Image.new('RGB',(W,H),(246,239,226)); d=ImageDraw.Draw(img)
fh=ImageFont.truetype(B,34); fb=ImageFont.truetype(B,19); fr=ImageFont.truetype(R,17); fi=ImageFont.truetype(I,18)
d.text((pad,28),"The Mound of the Dead · Mohenjo-daro & Harappa",fill=(150,110,200),font=fh)
d.text((pad,82),"Isometric Picture Book · 16:9 · 45.5 s · one continuous city, the camera travels, nothing cuts",fill=(46,38,34),font=fr)
d.text((pad,106),"Music: original score, harp-like plucks, drone, frame drum, flute (no recognisable raga) · VO: American warm (am_michael)",fill=(46,38,34),font=fr)
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
