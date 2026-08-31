# -*- coding: utf-8 -*-
"""Generador de la identidad visual y las piezas de redes de Cumplia.

Uso:   python3 generar-piezas.py
Salida: ./assets/*.png

Requisitos: pillow (pip install pillow) y la fuente Inter instalada.
  Linux:   sudo apt install fonts-inter
  Windows: descargar de https://rsms.me/inter/ e instalar, luego ajustar la
           ruta de la constante F (p. ej. C:/Windows/Fonts/).

Para cambiar el nombre de la marca: reemplazar "cumplia" en logo_horizontal()
y logo_vertical(). Para cambiar la paleta: editar el bloque Paleta.
"""

import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

F = "/usr/share/fonts/opentype/inter/"
FONTS = {
    "black":    F + "Inter-Black.otf",
    "extrabold":F + "Inter-ExtraBold.otf",
    "bold":     F + "Inter-Bold.otf",
    "semibold": F + "Inter-SemiBold.otf",
    "medium":   F + "Inter-Medium.otf",
    "regular":  F + "Inter-Regular.otf",
}
for k, v in list(FONTS.items()):
    if not os.path.exists(v):
        FONTS[k] = F + "Inter-Bold.otf"

def f(weight, size):
    return ImageFont.truetype(FONTS[weight], size)

# ---------------- Paleta ----------------
AZUL      = (16, 60, 87)      # #103C57  primario
AZUL_OSC  = (10, 38, 56)      # #0A2638
AZUL_CLARO= (43, 110, 150)    # #2B6E96
VERDE     = (22, 169, 124)    # #16A97C  acento / cumplido
AMBAR     = (233, 160, 32)    # #E9A020  alerta
ROJO      = (209, 71, 56)     # #D14738  crítico
TINTA     = (12, 26, 36)      # #0C1A24  texto
PIZARRA   = (91, 112, 128)    # #5B7080  texto secundario
LINEA     = (221, 229, 235)   # #DDE5EB
NIEBLA    = (244, 247, 249)   # #F4F7F9
BLANCO    = (255, 255, 255)

# ---------------- Helpers ----------------
def canvas(w, h, bg=BLANCO):
    im = Image.new("RGBA", (w, h), bg + (255,) if len(bg) == 3 else bg)
    return im, ImageDraw.Draw(im)

def tw(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0], b[3] - b[1]

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(draw, t, font)[0] <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def draw_block(draw, x, y, text, font, fill, maxw, leading=1.22, align="left"):
    lines = wrap(draw, text, font, maxw)
    lh = int(font.size * leading)
    for i, ln in enumerate(lines):
        xx = x
        if align == "center":
            xx = x + (maxw - tw(draw, ln, font)[0]) // 2
        draw.text((xx, y + i * lh), ln, font=font, fill=fill)
    return y + len(lines) * lh

def squircle(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)

def check(draw, cx, cy, size, color, width_ratio=0.155):
    """Visto de bordes redondeados, centrado en (cx, cy) dentro de un cuadro 'size'."""
    w = max(2, int(size * width_ratio))
    p1 = (cx - size * 0.30, cy + size * 0.02)
    p2 = (cx - size * 0.08, cy + size * 0.24)
    p3 = (cx + size * 0.33, cy - size * 0.26)
    draw.line([p1, p2], fill=color, width=w)
    draw.line([p2, p3], fill=color, width=w)
    r = w / 2
    for p in (p1, p2, p3):
        draw.ellipse([p[0]-r, p[1]-r, p[0]+r, p[1]+r], fill=color)

def isotipo(size, bg=AZUL, mark=BLANCO, acento=VERDE, transparente=False):
    S = size * 4
    im, d = canvas(S, S, (0, 0, 0, 0))
    pad = 0
    squircle(d, [pad, pad, S-1-pad, S-1-pad], radius=int(S*0.235), fill=bg)
    # arco de acento (progreso de cumplimiento)
    m = int(S*0.185)
    d.arc([m, m, S-m, S-m], start=118, end=422, fill=acento, width=int(S*0.062))
    check(d, S/2, S/2 + S*0.012, S*0.50, mark, 0.165)
    return im.resize((size, size), Image.LANCZOS)

def logo_horizontal(h=600, color_texto=AZUL, transparente=True, con_punto=True):
    ico = int(h * 0.78)
    icon = isotipo(ico)
    fs = int(h * 0.50)
    tmp, dtmp = canvas(10, 10)
    font = f("extrabold", fs)
    txt = "cumplia"
    tw_, th_ = tw(dtmp, txt, font)
    gap = int(h * 0.20)
    W = ico + gap + tw_ + int(h*0.16)
    im, d = canvas(W, h, (0,0,0,0) if transparente else BLANCO)
    im.paste(icon, (0, (h - ico)//2), icon)
    bb = d.textbbox((0,0), txt, font=font)
    d.text((ico + gap - bb[0], (h - (bb[3]-bb[1]))//2 - bb[1]), txt, font=font, fill=color_texto)
    if con_punto:
        r = int(h*0.055)
        cx = ico + gap + tw_ + int(h*0.075)
        cy = (h//2) + int(h*0.155)
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=VERDE)
    return im

def save(im, name):
    p = os.path.join(OUT, name)
    im.convert("RGBA").save(p)
    print("  ", name, im.size)

# ---------------- 1. Logos ----------------
save(isotipo(1024), "isotipo-1024.png")
save(isotipo(512), "favicon-512.png")
save(isotipo(400), "avatar-400.png")
save(isotipo(1024, bg=BLANCO, mark=AZUL, acento=VERDE), "isotipo-fondo-claro-1024.png")
save(isotipo(1024, bg=(0,0,0,0), mark=BLANCO, acento=VERDE, transparente=True), "isotipo-transparente-1024.png")
save(logo_horizontal(600), "logo-horizontal.png")
save(logo_horizontal(600, color_texto=BLANCO), "logo-horizontal-blanco.png")

# vertical
def logo_vertical(w=1000):
    ico = int(w*0.46)
    im, d = canvas(w, int(w*0.78), (0,0,0,0))
    icon = isotipo(ico)
    im.paste(icon, ((w-ico)//2, 0), icon)
    font = f("extrabold", int(w*0.20))
    txt = "cumplia"
    bb = d.textbbox((0,0), txt, font=font)
    d.text(((w-(bb[2]-bb[0]))//2 - bb[0], ico + int(w*0.06) - bb[1]), txt, font=font, fill=AZUL)
    f2 = f("medium", int(w*0.052))
    sub = "CUMPLIMIENTO EMPRESARIAL"
    bb2 = d.textbbox((0,0), sub, font=f2)
    d.text(((w-(bb2[2]-bb2[0]))//2 - bb2[0], ico + int(w*0.30)), sub, font=f2, fill=PIZARRA)
    return im
save(logo_vertical(), "logo-vertical.png")

print("logos listos")



def lg(h, blanco=False):
    return logo_horizontal(h, color_texto=(BLANCO if blanco else AZUL))

def fondo_azul(w, h, oscuro=True):
    base = AZUL_OSC if oscuro else AZUL
    im = Image.new("RGBA", (w, h), base + (255,))
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    step = max(48, w // 22)
    for x in range(0, w, step):
        od.line([(x, 0), (x, h)], fill=(255, 255, 255, 12), width=1)
    for y in range(0, h, step):
        od.line([(0, y), (w, y)], fill=(255, 255, 255, 12), width=1)
    # arco de marca, anclado a la esquina inferior derecha y fuera del area de texto
    r = int(min(w, h) * 1.5)
    cx, cy = w + int(r * 0.10), h + int(r * 0.10)
    od.arc([cx - r, cy - r, cx + r, cy + r], start=180, end=290,
           fill=(22, 169, 124, 70), width=max(5, min(w, h) // 60))
    im = Image.alpha_composite(im, ov)
    return im, ImageDraw.Draw(im)

def barra(d, x, y, w, h, color=VERDE):
    d.rounded_rectangle([x, y, x+w, y+h], radius=h//2, fill=color)

def pegar(base, im, x, y):
    base.paste(im, (int(x), int(y)), im)

# ---------- LinkedIn: portada de página 1128x191 ----------
def linkedin_pagina():
    W, H = 1128, 191
    im, d = fondo_azul(W, H)
    ft = f("bold", 40); fs = f("medium", 21)
    d.text((56, 52), "Cumplimiento empresarial, en una sola plataforma", font=ft, fill=BLANCO)
    d.text((56, 108), "SG-SST  ·  PESV  ·  SAGRILAFT  ·  Acompañamiento jurídico", font=fs, fill=(160, 196, 214))
    barra(d, 56, 145, 120, 6)
    return im

# ---------- LinkedIn: portada personal 1584x396 ----------
def linkedin_personal():
    W, H = 1584, 396
    im, d = fondo_azul(W, H)
    logo = lg(96, blanco=True); pegar(im, logo, 90, 88)
    ft = f("bold", 52); fs = f("regular", 27)
    d.text((90, 210), "Cumplimiento empresarial, en una sola plataforma", font=ft, fill=BLANCO)
    d.text((90, 282), "SG-SST · PESV · SAGRILAFT · Acompañamiento jurídico   —   Bogotá, Colombia",
           font=fs, fill=(160, 196, 214))
    barra(d, 90, 340, 160, 8)
    return im

# ---------- Facebook portada 1640x624 ----------
def facebook_portada():
    W, H = 1640, 624
    im, d = fondo_azul(W, H)
    logo = lg(150, blanco=True); pegar(im, logo, 110, 118)
    ft = f("bold", 62); fs = f("regular", 32)
    y = draw_block(d, 110, 300, "Cumplimiento empresarial, en una sola plataforma", ft, BLANCO, 1050)
    d.text((110, y + 18), "SG-SST  ·  PESV  ·  SAGRILAFT  ·  Acompañamiento jurídico",
           font=fs, fill=(160, 196, 214))
    barra(d, 110, y + 92, 190, 9)
    return im

# ---------- YouTube banner 2560x1440, zona segura 1546x423 ----------
def youtube_banner():
    W, H = 2560, 1440
    im, d = fondo_azul(W, H)
    cx, cy = W // 2, H // 2
    sw, sh = 1546, 423
    x0, y0 = cx - sw // 2, cy - sh // 2
    logo = lg(150, blanco=True)
    pegar(im, logo, cx - logo.width // 2, y0 + 20)
    ft = f("bold", 58); fs = f("medium", 30)
    t1 = "Cumplimiento sin adivinar"
    bb = d.textbbox((0,0), t1, font=ft)
    d.text((cx - (bb[2]-bb[0])//2 - bb[0], y0 + 215), t1, font=ft, fill=BLANCO)
    t2 = "SG-SST  ·  PESV  ·  SAGRILAFT  ·  Normativa colombiana explicada"
    bb2 = d.textbbox((0,0), t2, font=fs)
    d.text((cx - (bb2[2]-bb2[0])//2 - bb2[0], y0 + 300), t2, font=fs, fill=(160, 196, 214))
    barra(d, cx - 90, y0 + 370, 180, 9)
    return im

# ---------- Miniatura YouTube 1280x720 ----------
def miniatura(kicker, titulo, dato=None, color_kicker=AMBAR):
    W, H = 1280, 720
    im, d = fondo_azul(W, H)
    d.rounded_rectangle([0, 0, 26, H], radius=0, fill=VERDE)
    fk = f("extrabold", 34); ft = f("black", 92) if len(titulo) < 30 else f("black", 74)
    d.text((88, 92), kicker.upper(), font=fk, fill=color_kicker)
    y = draw_block(d, 88, 158, titulo.upper(), ft, BLANCO, 900, leading=1.05)
    if dato:
        fd = f("extrabold", 46)
        pad = 26
        wdt = tw(d, dato, fd)[0]
        d.rounded_rectangle([88, y + 34, 88 + wdt + pad*2, y + 34 + 86], radius=14, fill=VERDE)
        d.text((88 + pad, y + 34 + 20), dato, font=fd, fill=AZUL_OSC)
    logo = lg(58, blanco=True); pegar(im, logo, W - logo.width - 60, H - 110)
    return im

# ---------- Post cuadrado 1080x1080 ----------
def post_cuadrado(kicker, titulo, cuerpo, pie="cumplia.co", color_kicker=VERDE, claro=False):
    W = H = 1080
    if claro:
        im, d = canvas(W, H, NIEBLA)
        col_t, col_c, col_s = TINTA, PIZARRA, AZUL
        d.rounded_rectangle([0, 0, W, 14], fill=AZUL)
    else:
        im, d = fondo_azul(W, H)
        col_t, col_c, col_s = BLANCO, (160, 196, 214), BLANCO
    fk = f("extrabold", 30); ft = f("black", 76); fc = f("regular", 34)
    nt = len(wrap(d, titulo, ft, 920)); nc = len(wrap(d, cuerpo, fc, 920))
    alto = 68 + int(ft.size*1.10)*nt + 42 + int(fc.size*1.38)*nc
    y0 = max(110, (H - 150 - alto) // 2)
    d.text((80, y0), kicker.upper(), font=fk, fill=color_kicker)
    y = draw_block(d, 80, y0 + 68, titulo, ft, col_t, 920, leading=1.10)
    barra(d, 80, y + 34, 110, 8, VERDE if not claro else AZUL)
    y = draw_block(d, 80, y + 76, cuerpo, fc, col_c, 920, leading=1.38)
    logo = lg(56, blanco=not claro)
    pegar(im, logo, 80, H - 140)
    fp = f("medium", 28)
    d.text((W - 80 - tw(d, pie, fp)[0], H - 122), pie, font=fp, fill=col_c)
    return im

# ---------- Post vertical 1080x1350 ----------
def post_vertical(kicker, titulo, cuerpo, pie="cumplia.co"):
    W, H = 1080, 1350
    im, d = fondo_azul(W, H)
    fk = f("extrabold", 32); ft = f("black", 86); fc = f("regular", 36)
    nt = len(wrap(d, titulo, ft, 920)); nc = len(wrap(d, cuerpo, fc, 920))
    alto = 76 + int(ft.size*1.10)*nt + 46 + int(fc.size*1.40)*nc
    y0 = max(150, (H - 170 - alto) // 2)
    d.text((80, y0), kicker.upper(), font=fk, fill=VERDE)
    y = draw_block(d, 80, y0 + 76, titulo, ft, BLANCO, 920, leading=1.10)
    barra(d, 80, y + 40, 120, 8)
    y = draw_block(d, 80, y + 86, cuerpo, fc, (160, 196, 214), 920, leading=1.40)
    logo = lg(60, blanco=True); pegar(im, logo, 80, H - 150)
    fp = f("medium", 30)
    d.text((W - 80 - tw(d, pie, fp)[0], H - 132), pie, font=fp, fill=(160, 196, 214))
    return im

# ---------- Paleta ----------
def paleta():
    cols = [("Azul Cumplia", AZUL, "#103C57"), ("Azul profundo", AZUL_OSC, "#0A2638"),
            ("Azul claro", AZUL_CLARO, "#2B6E96"), ("Verde cumplido", VERDE, "#16A97C"),
            ("Ámbar alerta", AMBAR, "#E9A020"), ("Rojo crítico", ROJO, "#D14738"),
            ("Tinta", TINTA, "#0C1A24"), ("Pizarra", PIZARRA, "#5B7080"),
            ("Línea", LINEA, "#DDE5EB"), ("Niebla", NIEBLA, "#F4F7F9")]
    W, H = 1600, 700
    im, d = canvas(W, H, BLANCO)
    logo = lg(70); pegar(im, logo, 60, 50)
    fn = f("semibold", 26); fh = f("medium", 24)
    bw, bh = 280, 190
    for i, (n, c, hx) in enumerate(cols):
        x = 60 + (i % 5) * (bw + 20); y = 190 + (i // 5) * (bh + 110)
        d.rounded_rectangle([x, y, x + bw, y + bh], radius=16, fill=c,
                            outline=LINEA if c in (BLANCO, NIEBLA, LINEA) else None)
        d.text((x, y + bh + 16), n, font=fn, fill=TINTA)
        d.text((x, y + bh + 52), hx, font=fh, fill=PIZARRA)
    return im

save(linkedin_pagina(), "linkedin-portada-pagina-1128x191.png")
save(linkedin_personal(), "linkedin-portada-personal-1584x396.png")
save(facebook_portada(), "facebook-portada-1640x624.png")
save(youtube_banner(), "youtube-banner-2560x1440.png")

save(miniatura("Sanciones", "¿Cuánto cuesta una multa de SG-SST?", "Se liquida en UVT", AMBAR),
     "youtube-miniatura-01-multas.png")
save(miniatura("Plazo 31 de julio", "Autoevaluación 0312 en SGRL", "Paso a paso", VERDE),
     "youtube-miniatura-02-autoevaluacion.png")
save(miniatura("Seguridad vial", "¿Su empresa está obligada al PESV?", "Reporte: 6 al 31 de enero", AMBAR),
     "youtube-miniatura-03-pesv.png")

save(post_cuadrado("Dato que casi nadie tiene bien",
    "Las multas del SG-SST se liquidan en UVT, no en salarios mínimos.",
    "Desde el Decreto 2642 de 2022 la base cambió. Buena parte del material comercial del sector todavía lo dice mal — y eso importa cuando hay que calcular el riesgo real.",
    color_kicker=AMBAR), "post-01-uvt.png")

save(post_cuadrado("Calendario",
    "31 de julio: autoevaluación de estándares mínimos.",
    "La autoevaluación de la Resolución 0312 de 2019 se registra en la plataforma SGRL del Fondo de Riesgos Laborales. La ventana va de mayo a julio (Circular 027 de 2026)."),
    "post-02-autoevaluacion.png")

save(post_cuadrado("Calendario",
    "6 al 31 de enero: reporte del PESV.",
    "El Plan Estratégico de Seguridad Vial se reporta en enero (Circular 0034 de 2026). Si su empresa tiene flota, esa fecha no se mueve.",
    color_kicker=AMBAR), "post-03-pesv.png")

save(post_cuadrado("Programa de aliados",
    "20% de comisión recurrente para consultores SST.",
    "Los primeros 12 meses de cada empresa que refiera, y 10% mientras siga activa. Sin exclusividad, sin metas, sin costo de entrada."),
    "post-04-aliados.png")

save(post_cuadrado("Cómo trabajamos",
    "Precio público. Prueba de 14 días. Sin tarjeta.",
    "Solo 5 de cada 25 plataformas del sector publican su precio. Nosotros sí. Lo que ve en la página es lo que paga.",
    claro=True, color_kicker=VERDE), "post-05-precio.png")

save(post_vertical("Aliados",
    "5 empresas referidas = $349.000 al mes.",
    "Comisión del 20% sobre el plan Profesional durante los primeros 12 meses, y 10% mientras cada empresa siga activa. Usted ya asesora esas empresas."),
    "post-vertical-01-aliados.png")

save(post_vertical("SAGRILAFT",
    "Desde 40.000 SMMLV su empresa entra en el SAGRILAFT completo.",
    "El umbral se mide a 31 de diciembre sobre ingresos totales o activos. Hay además un régimen de medidas mínimas, más liviano, para sectores específicos."),
    "post-vertical-02-sagrilaft.png")

save(paleta(), "paleta-de-color.png")
print("piezas listas")
