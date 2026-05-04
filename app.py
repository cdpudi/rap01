import streamlit as st
import cairocffi as cairo
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Computação Gráfica", layout="centered")

st.title("📘 Relatório de Atividade Prática")

st.markdown("""
## 🧾 Contexto da Atividade

Este projeto foi desenvolvido na disciplina de **Computação Gráfica e Processamento de Imagens**.

A proposta consiste em demonstrar, de forma prática, três conceitos fundamentais:

- Criação de imagens vetoriais
- Manipulação de imagens matriciais (bitmap)
- Conversão de vetores para pixels (rasterização)

---

## 🎯 Objetivo

Aplicar conceitos matemáticos e computacionais para compreender como imagens digitais são construídas e exibidas.

---

## ⚙️ Etapas do Projeto

**Passo 1 — Imagem Vetorial**
- Uso de coordenadas contínuas
- Desenho de retas e círculo

**Passo 2 — Imagem Matricial**
- Manipulação direta de pixels
- Uso da equação do círculo

**Passo 3 — Conversão**
- Transformação de coordenadas reais em pixels
- Simulação de rasterização

---

## 🌍 Aplicação na Prática

Os conceitos deste projeto são utilizados em:

- Jogos digitais 🎮  
- Interfaces gráficas 🖥️  
- Design gráfico 🎨  
- Sistemas médicos 🧠  
- Renderização 2D/3D 🚀  

A rasterização é essencial para transformar dados matemáticos em imagens visíveis.

---
""")

# ======================================================
# FUNÇÕES AUXILIARES
# ======================================================

def mostrar(img, titulo):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap='gray')
    ax.set_title(titulo)
    ax.axis('off')
    st.pyplot(fig)


# ======================================================
# PASSO 1
# ======================================================

def passo1():
    largura, altura = 500, 500
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, largura, altura)
    ctx = cairo.Context(surface)

    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()

    # Linha preta
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(0.2 * largura, 0.3 * altura)
    ctx.line_to(0.8 * largura, 0.7 * altura)
    ctx.stroke()

    # Linha cinza escuro
    ctx.set_source_rgb(0.3, 0.3, 0.3)
    ctx.move_to(0.8 * largura, 0.3 * altura)
    ctx.line_to(0.2 * largura, 0.7 * altura)
    ctx.stroke()

    # Círculo
    ctx.set_source_rgb(0.8, 0.8, 0.8)
    ctx.arc(0.5 * largura, 0.5 * altura, 0.3 * largura, 0, 2 * np.pi)
    ctx.stroke()

    surface.write_to_png("p1.png")
    return Image.open("p1.png")


# ======================================================
# PASSO 2
# ======================================================

def desenhaCirculo(f, c, r, g):
    xc, yc = c
    for x in range(f.shape[0]):
        for y in range(f.shape[1]):
            if (x - xc)**2 + (y - yc)**2 <= r**2:
                f[y, x] = g


def passo2():
    f = np.ones((201, 201), dtype=np.uint8) * 255
    desenhaCirculo(f, (100, 100), 60, 230)
    return f


# ======================================================
# PASSO 3
# ======================================================

def desenhaReta(f, p, q, g):
    x1, y1 = p
    x2, y2 = q

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    err = dx - dy

    while True:
        if 0 <= x1 < f.shape[1] and 0 <= y1 < f.shape[0]:
            f[y1, x1] = g

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x1 += sx

        if e2 < dx:
            err += dx
            y1 += sy


def passo3():
    f = np.ones((201, 201), dtype=np.uint8) * 255

    def conv(p):
        return (round(p[0] * 201), round(p[1] * 201))

    desenhaReta(f, conv((0.2, 0.3)), conv((0.8, 0.7)), 0)
    desenhaReta(f, conv((0.8, 0.3)), conv((0.2, 0.7)), 80)

    desenhaCirculo(f, conv((0.5, 0.5)), round(0.3 * 201), 230)

    return f


# ======================================================
# INTERFACE
# ======================================================

st.sidebar.title("Navegação")
opcao = st.sidebar.radio(
    "Escolha o passo:",
    ["Passo 1 - Vetorial", "Passo 2 - Matricial", "Passo 3 - Conversão"]
)

if opcao == "Passo 1 - Vetorial":
    st.header("🧩 Passo 1 - Imagem Vetorial")

    st.markdown("""
    Aqui usamos **coordenadas contínuas (0 a 1)** para desenhar:
    - 2 retas
    - 1 círculo
    
    ✔ Alta precisão  
    ✔ Escalável sem perder qualidade  
    """)

    img = passo1()
    st.image(img, caption="Imagem Vetorial")

elif opcao == "Passo 2 - Matricial":
    st.header("🧩 Passo 2 - Imagem Matricial")

    st.markdown("""
    Aqui desenhamos pixel por pixel usando a equação do círculo:
    
    **(x - xc)² + (y - yc)² ≤ r²**
    
    ✔ Controle total dos pixels  
    ✔ Base da renderização  
    """)

    img = passo2()
    mostrar(img, "Círculo Matricial")

elif opcao == "Passo 3 - Conversão":
    st.header("🧩 Passo 3 - Vetor → Bitmap")

    st.markdown("""
    Convertendo coordenadas reais para pixels:
    
    **pixel = coordenada × tamanho da imagem**
    
    ✔ Processo chamado de rasterização  
    ✔ Usado em jogos, gráficos e imagens digitais  
    """)

    img = passo3()
    mostrar(img, "Imagem Convertida")
