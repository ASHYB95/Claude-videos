# Assemble index.html from index.src.html: inline the Pot path and the logo (flat + animated groups).
import re, os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POT='M31 0H69Q74 0 76.5 4.5L98 44Q100 48 100 54A50 50 0 0 1 0 54Q0 48 2 44L23.5 4.5Q26 0 31 0Z'
svg=open(os.path.join(R,'brand/LogoCharcoal.svg')).read()
P=re.findall(r'<path d="([^"]+)"[^>]*fill="#2F2F32"',svg)   # 0-9 COLLECTION, 10 O of POT, 11 P, 12 T, 13 TM
pp=lambda i:f'<path d="{P[i]}" fill="#2F2F32"/>'
flat=''.join(pp(i) for i in range(len(P)))
groups=('<defs><clipPath id="clL"><rect x="-10" y="-10" width="394" height="60"/></clipPath>'
        '<clipPath id="clR"><rect x="419" y="-10" width="60" height="60"/></clipPath></defs>'
        '<g clip-path="url(#clL)"><g id="lgLeft">'+''.join(pp(i) for i in list(range(10))+[11])+'</g></g>'
        '<g clip-path="url(#clR)"><g id="lgRight">'+pp(12)+pp(13)+'</g></g>'
        '<g id="lgO">'+pp(10)+'</g>'
        f'<g id="lgPotSolid"><path d="{POT}" fill="#2F2F32" transform="translate(386.75 4.15) scale(.3)"/></g>')
s=open(os.path.join(R,'src/index.src.html')).read().replace('LOGOGROUPS',groups).replace('LOGOFLAT',flat).replace('POTPATH',POT)
s=s.replace("gsap.set('#sentPot',{scale:0});gsap.set('#sentTick',{drawSVG:0});","gsap.set('#sentPot',{scale:0});gsap.set('#endLogo',{opacity:0});")
open(os.path.join(R,'index.html'),'w').write(s); print('ok', len(s))
