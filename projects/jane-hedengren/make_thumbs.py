import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
J='/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad/jane/'
F='/home/user/YouTube-/tools/fonts/'
W,H=1280,720
def font(n,s): return ImageFont.truetype(F+n,s)
def fill(im,w,h,cx=.5,cy=.5):
    r=max(w/im.width,h/im.height); im=im.resize((int(im.width*r+.5),int(im.height*r+.5)),Image.LANCZOS)
    x=int((im.width-w)*cx); y=int((im.height-h)*cy); return im.crop((x,y,x+w,y+h))
def shadow_text(c,xy,txt,f,fillc='white',sh=10,anchor='la',stroke=0):
    lay=Image.new('RGBA',c.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.text((xy[0]+4,xy[1]+6),txt,font=f,fill=(0,0,0,200),anchor=anchor,stroke_width=stroke,stroke_fill=(0,0,0,200))
    lay=lay.filter(ImageFilter.GaussianBlur(sh)); c.alpha_composite(lay)
    ImageDraw.Draw(c).text(xy,txt,font=f,fill=fillc,anchor=anchor,stroke_width=stroke,stroke_fill='black')
def grade(im,b=.8,c=1.15,s=.95): return ImageEnhance.Color(ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(b)).enhance(c)).enhance(s)
def vgrad(c,x0,x1,alpha=230,left=True):
    g=Image.new('L',(W,H),0); d=ImageDraw.Draw(g)
    for x in range(W):
        t=(x1-x)/(x1-x0) if left else (x-x0)/(x1-x0); t=max(0,min(1,t)); d.line([(x,0),(x,H)],fill=int(alpha*t))
    c.alpha_composite(Image.merge('RGBA',[Image.new('L',(W,H),0)]*3+[g]))
def rim(cut,glow=(255,255,255),r=6,a=120):
    al=cut.split()[3].filter(ImageFilter.GaussianBlur(r)); g=Image.new('RGBA',cut.size,glow+(0,)); g.putalpha(al.point(lambda v:min(a,v)))
    return g
def cutout(path,h):
    im=Image.open(path).convert('RGBA'); bb=im.split()[3].getbbox(); im=im.crop(bb); r=h/im.height
    return im.resize((int(im.width*r),h),Image.LANCZOS)

FACE60=sys.argv[1] if len(sys.argv)>1 else J+'fr/bfull_60_cut.png'
FACE90=sys.argv[2] if len(sys.argv)>2 else J+'fr/bfull_90_cut.png'
PROF=sys.argv[3] if len(sys.argv)>3 else J+'fr/nike_365.jpg'


P=J+'photos/'
# A: Tuohy style - pensive Nike photoshoot, text left
bg=fill(Image.open(J+'fr/nike_207.jpg').convert('RGB'),W,H).filter(ImageFilter.GaussianBlur(10))
bg=grade(bg,.45,1.1,.6).convert('RGBA')
cut=cutout(P+'c_nike.png',900); x=W-cut.width-60; y=H-cut.height+150
bg.alpha_composite(rim(cut,r=8,a=70),(x,y)); bg.alpha_composite(cut,(x,y))
f=font('Anton-Regular.ttf',140)
shadow_text(bg,(60,150),'WILL SHE',f); shadow_text(bg,(60,330),'BE NEXT?',f)
bg.convert('RGB').save(J+'thumbs/A_will_she_be_next.jpg',quality=95)

# B: Webb style - race cutout, falling red arrow
sky=Image.open(J+'fr/nike_280.jpg').convert('RGB').crop((0,0,950,534))
bg=fill(sky,W,H).filter(ImageFilter.GaussianBlur(3)); bg=grade(bg,.5,1.2,.55).convert('RGBA')
d=ImageDraw.Draw(bg)
pts=[(470,20),(560,140),(600,160),(780,360),(860,315),(1060,560)]
for wdt,col in [(26,(0,0,0,140)),(14,(225,25,25,255))]: d.line(pts,fill=col,width=wdt,joint='curve')
d.polygon([(1130,630),(1010,600),(1090,510)],fill=(225,25,25,255))
cut=cutout(P+'c_wiki.png',900); x=20; y=-10
bg.alpha_composite(rim(cut),(x,y)); bg.alpha_composite(cut,(x,y))
f=font('Anton-Regular.ttf',120)
shadow_text(bg,(1020,90),'IS SHE',f,fillc=(245,236,220),anchor='ma'); shadow_text(bg,(1020,240),'NEXT?',f,fillc=(245,236,220),anchor='ma')
bg.convert('RGB').save(J+'thumbs/B_is_she_next_arrow.jpg',quality=95)

# C: Steiner style - real NCAA race photo, face left, white/red italic text right
im=Image.open(P+'p_byunews.jpg').convert('RGB').crop((760,120,1760,683))
bg=fill(im,W,H); bg=ImageEnhance.Contrast(bg).enhance(1.08).convert('RGBA')
vgrad(bg,560,1280,215,left=False)
f1=font('Montserrat-BlackItalic.ttf',112); f2=font('Montserrat-BlackItalic.ttf',150)
shadow_text(bg,(970,230),'IS SHE',f1,anchor='ma',stroke=4)
shadow_text(bg,(970,365),'NEXT?',f2,fillc=(230,30,35),anchor='ma',stroke=5)
d=ImageDraw.Draw(bg); d.line([(745,560),(945,548),(1195,540)],fill=(230,30,35),width=12)
bg.convert('RGB').save(J+'thumbs/C_is_she_next_face.jpg',quality=95)

# D: Tuohy (fading, B&W) vs Jane (colour)
bg=fill(Image.open(J+'fr/nike_207.jpg').convert('RGB'),W,H).filter(ImageFilter.GaussianBlur(14))
bg=grade(bg,.35,1.0,.4).convert('RGBA')
t=cutout(J+'fr/tuohy_cut.png',700); g=ImageOps.grayscale(t.convert('RGB')).convert('RGBA'); g.putalpha(t.split()[3].point(lambda v:int(v*.8)))
g=ImageEnhance.Brightness(g).enhance(.75)
bg.alpha_composite(g,(-120,H-t.height+40))
j=cutout(P+'c_wiki.png',860); bg.alpha_composite(rim(j),(W-j.width+20,-20)); bg.alpha_composite(j,(W-j.width+20,-20))
f=font('Anton-Regular.ttf',190)
shadow_text(bg,(W//2+10,250),'NEXT?',f,fillc=(230,30,35),anchor='ma',stroke=4)
fs=font('Anton-Regular.ttf',44)
shadow_text(bg,(W//2+10,470),'TUOHY  →  JANE',fs,fillc=(235,235,235),anchor='ma')
bg.convert('RGB').save(J+'thumbs/D_tuohy_vs_jane.jpg',quality=95)
