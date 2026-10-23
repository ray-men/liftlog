# Applique les réglages Lift Log au projet Android généré par Capacitor.
import os
from PIL import Image, ImageDraw
R='android/app/src/main/'
def rw(path,f):
    s=open(R+path,encoding='utf-8').read();s=f(s);open(R+path,'w',encoding='utf-8').write(s)
def manifest(m):
    m=m.replace('<uses-permission android:name="android.permission.INTERNET" />','<uses-permission android:name="android.permission.INTERNET" />\n    <uses-permission android:name="android.permission.VIBRATE" />')
    return m.replace('android:launchMode="singleTask"','android:launchMode="singleTask"\n            android:windowSoftInputMode="adjustResize"\n            android:screenOrientation="portrait"')
rw('AndroidManifest.xml',manifest)
def styles(st):
    st=st.replace('<item name="android:background">@null</item>','<item name="android:background">@null</item>\n        <item name="android:windowBackground">@color/bg</item>')
    return st.replace('<item name="android:background">@drawable/splash</item>','<item name="android:background">@color/bg</item>\n        <item name="windowSplashScreenBackground">@color/bg</item>')
rw('res/values/styles.xml',styles)
open(R+'res/values/ic_launcher_background.xml','w').write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#12151A</color>\n    <color name="bg">#12151A</color>\n</resources>\n')
fg=R+'res/drawable-v24/ic_launcher_foreground.xml'
if os.path.exists(fg): os.remove(fg)
OR=(255,176,32,255);BG=(18,21,26,255)
def dumbbell(sz,scale):
    S=sz*4;im=Image.new('RGBA',(S,S),(0,0,0,0));d=ImageDraw.Draw(im);u=S*scale/100;c=S/2
    def rr(x0,y0,x1,y1,r):d.rounded_rectangle([c+x0*u,c+y0*u,c+x1*u,c+y1*u],r*u,fill=OR)
    rr(-24,-4,24,4,2);rr(-34,-20,-24,20,3);rr(24,-20,34,20,3);rr(-42,-13,-34,13,3);rr(34,-13,42,13,3)
    return im.resize((sz,sz),Image.LANCZOS)
for k,(l,f) in {'mdpi':(48,108),'hdpi':(72,162),'xhdpi':(96,216),'xxhdpi':(144,324),'xxxhdpi':(192,432)}.items():
    d=R+f'res/mipmap-{k}/'
    dumbbell(f,0.62).save(d+'ic_launcher_foreground.png')
    for name,sq in (('ic_launcher',True),('ic_launcher_round',False)):
        im=Image.new('RGBA',(l*4,l*4),(0,0,0,0));dd=ImageDraw.Draw(im)
        if sq: dd.rounded_rectangle([0,0,l*4-1,l*4-1],l*4*0.22,fill=BG)
        else: dd.ellipse([0,0,l*4-1,l*4-1],fill=BG)
        im=im.resize((l,l),Image.LANCZOS);im.alpha_composite(dumbbell(l,1.1));im.save(d+name+'.png')
for root,_,fs in os.walk(R+'res'):
    for f in fs:
        if f=='splash.png':
            p=os.path.join(root,f);w,h=Image.open(p).size;Image.new('RGB',(w,h),(18,21,26)).save(p)
print('setup ok')
