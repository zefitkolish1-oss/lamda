# Generates site images from the app's single-source character art (icon/gen.py → lamda_icon.svg) and screens2/.
import re, io, cairosvg
from PIL import Image
SRC='/workspace/lamda/icon/lamda_icon.svg'; OUT='/workspace/lamda/website/assets/img'
s=open(SRC).read()
orb=s.replace('<rect width="108" height="108" fill="url(#bg)"/>','')
orb=orb.replace('viewBox="0 0 108 108"','viewBox="22 22 64 64"').replace('width="108" height="108"','width="256" height="256"')
open(f'{OUT}/orb.svg','w').write(orb)
open(f'{OUT}/favicon.svg','w').write(s)
def png(svg,px): return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),output_width=px,output_height=px))).convert('RGBA')
for n,px in [('favicon-32.png',32),('apple-touch-icon.png',180),('icon-192.png',192),('icon-512.png',512)]:
    png(s,px).save(f'{OUT}/{n}')
png(s,48).save(f'/workspace/lamda/website/favicon.ico',sizes=[(16,16),(32,32),(48,48)])
shots=['30_splash_name_complete_1080x2400','26_chat_light_face','14_onboarding_accessibility','11_bubble_orb','12_bubble_panel','15_settings_light_1','15_settings_light_3']
for n in shots:
    im=Image.open(f'/workspace/lamda/screens2/{n}.png').convert('RGB')
    w=540; h=round(im.height*w/im.width); im=im.resize((w,h),Image.LANCZOS)
    im.save(f'{OUT}/shots/{n.replace("_1080x2400","")}.webp','WEBP',quality=80,method=6)
    print(n, im.size)
