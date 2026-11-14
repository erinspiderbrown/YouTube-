from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops
from rembg import remove,new_session
J='/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad/jane/'; P=J+'photos/'
F='/home/user/YouTube-/tools/fonts/'; W,H=1280,720
OFF=(244,240,232)
def font(n,s): return ImageFont.truetype(F+n,s)
def txt(c,xy,t,f,fill=OFF,anchor='la',sh=14,so=(0,6),stroke=0):
    lay=Image.new('RGBA',c.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.text((xy[0]+so[0],xy[1]+so[1]),t,font=f,fill=(0,0,0,190),anchor=anchor,stroke_width=stroke,stroke_fill=(0,0,0,190))
    c.alpha_composite(lay.filter(ImageFilter.GaussianBlur(sh)))
    ImageDraw.Draw(c).text(xy,t,font=f,fill=fill,anchor=anchor,stroke_width=stroke,stroke_fill='black')
def tight(im):
    bb=im.split()[3].point(lambda v:255 if v>40 else 0).getbbox(); return im.crop(bb)
def scale_h(im,h): r=h/im.height; return im.resize((int(im.width*r),h),Image.LANCZOS)
def light_subject(cut):
    rgb=cut.convert('RGB'); rgb=ImageEnhance.Contrast(rgb).enhance(1.08); rgb=ImageEnhance.Brightness(rgb).enhance(1.04)
    rgb=rgb.filter(ImageFilter.UnsharpMask(2,60,2)); out=rgb.convert('RGBA'); out.putalpha(cut.split()[3]); return out
def rimlight(c,cut,xy,col=(190,205,225),a=45,r=5):
    al=cut.split()[3]; g=Image.new('RGBA',cut.size,col+(0,)); g.putalpha(al.filter(ImageFilter.GaussianBlur(r)).point(lambda v:min(a,v)))
    c.alpha_composite(g,xy)
stad=Image.open(J+'stadium_bg.jpg').convert('RGBA')

nike=light_subject(tight(Image.open(P+'nike_4k_cut.png')))
# 1: Tuohy style - "WILL SHE BE NEXT?"
c=stad.copy(); cut=scale_h(nike,860); x=W-cut.width+40; y=-40
rimlight(c,cut,(x,y)); c.alpha_composite(cut,(x,y))
f=font('BebasNeue-Regular.ttf',150)
txt(c,(80,150),'WILL SHE',f); txt(c,(80,290),'BE NEXT?',f)
c.convert('RGB').save(J+'thumbs/1_will_she_be_next.jpg',quality=95)

# 2: same, "IS SHE NEXT?" with red NEXT
c=stad.copy(); c.alpha_composite(Image.new('RGBA',(W,H),(0,0,0,0)))
rimlight(c,cut,(x,y)); c.alpha_composite(cut,(x,y))
f=font('BebasNeue-Regular.ttf',175)
txt(c,(80,150),'IS SHE',f); txt(c,(80,315),'NEXT?',f,fill=(232,36,36))
c.convert('RGB').save(J+'thumbs/2_is_she_next_red.jpg',quality=95)

# 3: BYU race photo cutout on stadium bg
ph=Image.open(P+'up_byu2.jpg').convert('RGB')
s_=new_session('isnet-general-use'); m=remove(ph,session=s_,only_mask=True)
md=ImageDraw.Draw(m); w,h=ph.size
md.polygon([(0,0),(int(w*.33),0),(int(w*.33),int(h*.42)),(int(w*.12),int(h*.6)),(int(w*.1),h),(0,h)],fill=0)
md.polygon([(w,0),(int(w*.70),0),(int(w*.70),int(h*.40)),(int(w*.84),int(h*.52)),(int(w*.86),h),(w,h)],fill=0)
m=m.filter(ImageFilter.GaussianBlur(1.5))
rc=ImageEnhance.Contrast(ph).enhance(1.08).filter(ImageFilter.UnsharpMask(2,60,2)).convert('RGBA'); rc.putalpha(m)
rc=tight(rc); rc=scale_h(rc,1050)
c=stad.copy(); x3=W-rc.width+10; y3=-30
rimlight(c,rc,(x3,y3)); c.alpha_composite(rc,(x3,y3))
f=font('BebasNeue-Regular.ttf',150)
txt(c,(70,170),'WILL SHE',f); txt(c,(70,310),'BE NEXT?',f)
c.convert('RGB').save(J+'thumbs/3_race_will_she_be_next.jpg',quality=95)

# 4: Tuohy fading B&W behind, Jane big in colour
c=stad.copy()
t=tight(Image.open(J+'fr/tuohy_cut.png')); t=scale_h(t,640)
tg=ImageOps.grayscale(t.convert('RGB')).convert('RGBA'); tg=ImageEnhance.Brightness(tg).enhance(.55); tg.putalpha(t.split()[3].point(lambda v:int(v*.85)))
c.alpha_composite(tg,(60,H-tg.height+60))
cut4=scale_h(nike,820); x4=W-cut4.width+60; rimlight(c,cut4,(x4,-20)); c.alpha_composite(cut4,(x4,-20))
f=font('BebasNeue-Regular.ttf',165)
txt(c,(40,500),'NEXT?',font('BebasNeue-Regular.ttf',210),fill=(232,36,36))
c.convert('RGB').save(J+'thumbs/4_tuohy_then_jane.jpg',quality=95)
