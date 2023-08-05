'''
Author    : Krypton-Byte
Github    : https://github.com/krypton-byte
Repository: https://github.com/krypton-byte/blackpink
'''
from PIL import Image, ImageFont, ImageDraw
from os import listdir
if "blackpink.otf" in listdir('/'.join(__file__.split("/")[:-1])):
    import requests
    open('/'.join(__file__.split("/")[:-1])+"/blackpink.otf", "wb").write(requests.get("https://raw.githubusercontent.com/krypton-byte/blackpink/master/blackpink.otf").content)
font=ImageFont.truetype('/'.join(__file__.split("/")[:-1])+"/blackpink.otf", 230)
def blackpink(teks):
    (draw:=ImageDraw.Draw((img:=Image.new("RGB", ((length:=font.getsize(teks))[0]+100, length[1]), color=(0, 0, 0))))).text((int((img.width/2)-(draw.textsize(teks, font)[0]/2)), int(-25)), teks, fill=(255, 148, 224), font=font)
    (img2:=Image.new("RGB", ((hasil:=Paste(img)).width+400, hasil.height+400), color=(0, 0, 0))).paste(hasil, (int((img2.width/2)-(hasil.width/2)), int((img2.height/2)-(hasil.height/2))))
    return img2
def Paste(im):
    (new:=Image.new("RGB", (im.width+20, im.height+20), color=(255, 148, 224))).paste(im, (int((new.width/2)-(im.width/2)), int((new.height/2)-(im.height/2))))
    new.paste(im, (int((new.width/2)-(im.width/2)), int((new.height/2)-(im.height/2))))
    return new
