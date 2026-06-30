from PIL import Image, ImageDraw, ImageTk, ImageFont
import numpy as np

# chars = " .,_+#&*$@"

chars = " .,'\"`^-~:;_+#&*$@"
# chars = " .·'\"`^-~,:;!i|Il1t!?+<>()[]{}©®™°•○◌◍◎●◐◑◒◓◔◕◖◗☐☒☑☖☗☙☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789§¶#&%$@\/*=≠≈+-−×÷±√∞∑∏∫∂∆∇∈∉∋∌∩∪⊂⊃⊆⊇∧∨¬⇒⇔∀∃⌘⌛⌚⏎⏏⏑⏒⏓⏔⏕⏖⏗⏘⏙⏚⏛⏜⏝⏞⏟⏠⏡←↑→↓↔↕↖↗↘↙↚↛↜↝↞↟↠↡↢↣↤↥↦↧↨↩↪↫↬↭↮↯┄┅┆┇┈┉┊┋╱╲╳※☀☁☂☃☄★☆☇☉♀♂♠♣♥♦♪♫⌘⌛⌚⏎⏏⏑⏒⏓⏔⏕⏖⏗⏘⏙="

inversion = 1

def char_to_pixels(char, size=100):
    global inversion
    # ft = ImageFont.truetype("DejaVuSansMono.ttf", 24)
    ft = ImageFont.truetype("UbuntuMono-R.ttf", 24)
    # ft = ImageFont.truetype("arial.ttf", 24)
    bbox=ImageDraw.Draw(Image.new('L', (1, 1), 'black')).textbbox((0,0), char, ft)
    width, height = bbox[2]-bbox[0], bbox[3]
    
    
    img = Image.new('L', (width, height), 'black')
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), char, font=ft, fill='white')
    
    return np.array(img)


def brightness_sort():
    global chars, widthation

    brightness = []

    max_width=0
    max_height=0

    chars = [i for i in chars]

    for i in range(len(chars)):
        pixels = char_to_pixels(chars[i], size=50)
        if pixels.shape[0] > max_height:
            max_height=pixels.shape[0]
        if pixels.shape[1] > max_width:
            max_width=pixels.shape[1]
        brightness.append(sum([sum([int(i) for i in col]) for col in pixels]))
        # chars[i]=(chars[i], pixels.shape[1])

    # if inversion:
    #     brightness = [i/(max_width*max_height)/(max(brightness)/(max_width*max_height)) for i in brightness]
    # else:
    #     brightness = [1-i/(max_width*max_height)/(max(brightness)/(max_width*max_height)) for i in brightness]
    if inversion:
        brightness = [i/(max(brightness)) for i in brightness]
    else:
        brightness = [1-i/(max(brightness)) for i in brightness]
    
    
    widthation = max_height/max_width

    for i in range(len(brightness)-1):
        for idx in range(len(brightness)-i-1):
            if brightness[idx] > brightness[idx+1]:
                brightness[idx], brightness[idx+1] = brightness[idx+1], brightness[idx]
                chars[idx], chars[idx+1] = chars[idx+1], chars[idx]
    
    return brightness, chars



