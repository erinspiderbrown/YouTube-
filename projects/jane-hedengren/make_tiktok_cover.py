from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageEnhance,ImageChops
import numpy as np
from scipy import ndimage
SRC='src_clean.png'
src=Image.open(SRC).convert('RGB'); W,H=1080,1920
cx0,cx1=850,1672
crop=src.crop((cx0,0,cx1,src.height)); s=W/crop.width
ph=crop.resize((W,int(crop.height*s)),Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.4,60,2)); py=H-ph.height
al=np.array(Image.open('cut.png').split()[3]); bw=al>40; lab,n=ndimage.label(bw); sz=ndimage.sum(bw,lab,range(1,n+1)); al[lab!=(np.argmax(sz)+1)]=0
m=Image.fromarray(al).crop((cx0,0,cx1,src.height)).resize(ph.size,Image.LANCZOS)
subj=Image.new('L',(W,H),0); subj.paste(m,(0,py))
sky=src.crop((1340,0,1672,260)).resize((W,py+300),Image.BICUBIC).filter(ImageFilter.GaussianBlur(30))
canvas=Image.new('RGB',(W,H)); canvas.paste(sky,(0,0))
fade=Image.linear_gradient('L').resize((W,300)); a=Image.new('L',ph.size,255); a.paste(fade,(0,0)); a=ImageChops.lighter(a,m)
canvas.paste(ph,(0,py),a)
rgb=ImageEnhance.Contrast(canvas).enhance(1.08)
v=Image.new('L',(W,H),0); ImageDraw.Draw(v).ellipse([-350,-250,W+350,H+250],fill=255); v=v.filter(ImageFilter.GaussianBlur(220))
rgb=Image.composite(rgb,ImageEnhance.Brightness(rgb).enhance(.45),v)
base=rgb.convert('RGBA'); out=base.copy()
# crisp red falling arrow behind her
S=2; L=Image.new('RGBA',(W*S,H*S),(0,0,0,0)); d=ImageDraw.Draw(L)
pts=[(-30,640),(180,790),(270,745),(520,950),(610,905),(900,1110)]
P=[(x*S,y*S) for x,y in pts]
d.line(P,fill=(0,0,0,150),width=40*S,joint='curve'); d.line(P,fill=(226,28,28,255),width=24*S,joint='curve')
ah=[(1010,1195),(860,1170),(955,1060)]
d.polygon([(x*S+6,y*S+6) for x,y in ah],fill=(0,0,0,150)); d.polygon([(x*S,y*S) for x,y in ah],fill=(226,28,28,255))
out.alpha_composite(L.resize((W,H),Image.LANCZOS))
out=Image.composite(base,out,subj.point(lambda q:255 if q>120 else int(q*2)))
# title, same look as the thumbnail: heavy italic cream caps
F=ImageFont.truetype('/home/user/YouTube-/tools/fonts/Anton-Regular.ttf',250); CREAM=(246,240,228)
def title(txt,y):
    lay=Image.new('RGBA',(W*2,600),(0,0,0,0)); dd=ImageDraw.Draw(lay); dd.text((W,300),txt,font=F,fill=CREAM,anchor='mm')
    lay=lay.transform(lay.size,Image.AFFINE,(1,0.2,-60,0,1,0),Image.BICUBIC)
    sh=Image.new('RGBA',lay.size,(0,0,0,0)); sh.putalpha(lay.split()[3].point(lambda q:int(q*0.8))); sh=sh.filter(ImageFilter.GaussianBlur(16))
    out.alpha_composite(sh.crop((W//2-6,-10,W//2+W-6,590)),(0,y-300)); out.alpha_composite(lay.crop((W//2,0,W//2+W,600)),(0,y-300))
title('NEXT TO',300); title('FALL?',560)
g=np.random.default_rng(2).normal(0,5,(H,W,1)); res=np.clip(np.array(out.convert('RGB')).astype(float)+g,0,255).astype('uint8')
Image.fromarray(res).save('jane_tiktok_cover.jpg',quality=96); Image.fromarray(res).resize((540,960),Image.LANCZOS).save('prev.jpg')
Image.fromarray(res).crop((150,600,850,1250)).save('face.jpg')
