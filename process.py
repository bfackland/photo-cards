import os
from PIL import Image, ImageDraw, ImageFont

files = os.listdir("./")
files = [ x for x in files if len(x) > 1 and x[1] == '-' and (
        x.lower().endswith('jpg') or
        x.lower().endswith('jpeg') or
        x.lower().endswith('png'))
          ]

scale = (400, 400)
size = (400, 600)
padding = 20

target = "./out/"

font_path = "/Library/Fonts/Bradley Hand Bold.ttf"

for f in files:
    letter = f[0]
    #if letter != 'g': continue
    text = f[2:f.find('.')]
    words = text.split('_')
    print letter, words
    font = ImageFont.truetype(font_path, 64)

    im = Image.open("./%s" % f)

    # hard-rotate images that use EXIF data for display rotation (e.g. iphone)
    image_orientation = None
    try:
        image_exif = im._getexif()
        image_orientation = image_exif[274]
    except:
        pass

    if image_orientation == 3:
        rotated = im.rotate(180)
    elif image_orientation == 6:
        rotated = im.rotate(-90)
    elif image_orientation == 8:
        rotated = im.rotate(90)

    # resize image to ensure min dimension is max needed, then crop to aspect
    im_w, im_h = im.size
    im_min = min(im.size)
    im_aspect = float(im.size[0]) / float(im.size[1])
    print "w,h,aspect:", im_w, im_h, im_aspect

    if im_aspect > 1.0:
        # wide image
        # (left, upper, right, lower)
        margin = (im_w / 2.0) - (im_h / 2.0)
        crop = (
            margin,
            0,
            im_w - margin,
            im_h,
            )
        print "CROP l,r:", crop
        im = im.crop(crop)
    elif im_aspect < 1.0:
        # tall image
        margin = (im_h / 2.0) - (im_w / 2.0)
        crop = (
            0,
            margin,
            im_w,
            im_h - margin,
            )
        print "CROP left, upper, right, lower:", crop
        im = im.crop(crop)

    im = im.resize(scale, Image.ANTIALIAS)

    card = Image.new('RGB', size, color="white")
    card.paste(im)
    draw = ImageDraw.Draw(card)
    # TODO: could calculate size of single letter and centralise
    # TODO: write a 'centralise' function
    draw.text((180, 400), letter, fill=(0, 0, 0), font=font)

    x = padding
    font_size = 54
    font = ImageFont.truetype(font_path, font_size)
    w, h = draw.textsize(text, font=font)
    print w
    while w > (size[0] - (padding * 2)):
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        w, h = draw.textsize(text, font=font)
        print w

    x = int((size[0] - w) / 2.0)

    for word in words:
        z = 0
        for c in word:
            w, h = draw.textsize(c, font=font)

            if z == 0 and c == letter:
                color = (0, 0, 0)
            else:
                color = (100, 100, 100)
            draw.text((x, 480), c, fill=color, font=font)
            x += w
            z += 1
        x += draw.textsize(' ', font=font)[0]

    card.save("%s/%s.jpg" % (target, letter), "JPEG")

del draw
