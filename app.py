import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Computação Gráfica", layout="centered")

# ======================================================
# CABEÇALHO / RELATÓRIO
# ======================================================

st.title("📘 Relatório de Atividade Prática")
st.markdown("""
## Computação Gráfica e Processamento de Imagens

Este projeto demonstra, na prática, conceitos fundamentais da computação gráfica:

- Criação de imagens vetoriais
- Manipulação de imagens matriciais (bitmap)
- Conversão de vetores para pixels (rasterização)

---

### 🎯 Objetivo

Compreender como imagens digitais são construídas e exibidas, utilizando conceitos matemáticos e computacionais.

---

### 🌍 Aplicação na Vida Real

Esses conceitos são utilizados em:

- Jogos digitais 🎮  
- Interfaces gráficas 🖥️  
- Design gráfico 🎨  
- Sistemas médicos 🧠  
- Renderização 2D/3D 🚀  

A rasterização é o processo responsável por transformar dados matemáticos em imagens visíveis.
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


def desenha_circulo(img, centro, raio, cor):
    xc, yc = centro
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if (x - xc)**2 + (y - yc)**2 <= raio**2:
                img[y, x] = cor


def desenha_reta(img, p1, p2, cor):
    x1, y1 = p1
    x2, y2 = p2

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    err = dx - dy

    while True:
        if 0 <= x1 < img.shape[1] and 0 <= y1 < img.shape[0]:
            img[y1, x1] = cor

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x1 += sx

        if e2 < dx:
            err += dx
            y1 += sy


# ======================================================
# PASSO 1 - "VETORIAL" SIMULADO
# ======================================================

def passo1():
    img = np.ones((500, 500), dtype=np.uint8) * 255

    def conv(p):
        return (round(p[0] * 500), round(p[1] * 500))

    desenha_reta(img, conv((0.2, 0.3)), conv((0.8, 0.7)), 0)
    desenha_reta(img, conv((0.8, 0.3)), conv((0.2, 0.7)), 80)

    desenha_circulo(img, conv((0.5, 0.5)), int(0.3 * 500), 200)

    return img


# ======================================================
# PASSO 2 - CÍRCULO MATRICIAL
# ======================================================

def passo2():
    img = np.ones((201, 201), dtype=np.uint8) * 255
    desenha_circulo(img, (100, 100), 60, 230)
    return img


# ======================================================
# PASSO 3 - CONVERSÃO
# ======================================================

def passo3():
    img = np.ones((201, 201), dtype=np.uint8) * 255

    def conv(p):
        return (round(p[0] * 201), round(p[1] * 201))

    desenha_reta(img, conv((0.2, 0.3)), conv((0.8, 0.7)), 0)
    desenha_reta(img, conv((0.8, 0.3)), conv((0.2, 0.7)), 80)

    desenha_circulo(img, conv((0.5, 0.5)), int(0.3 * 201), 230)

    return img


# ======================================================
# MENU
# ======================================================

st.sidebar.title("📌 Navegação")
opcao = st.sidebar.radio(
    "Escolha o passo:",
    ["Passo 1 - Vetorial", "Passo 2 - Matricial", "Passo 3 - Conversão"]
)

# ======================================================
# TELAS
# ======================================================

if opcao == "Passo 1 - Vetorial":
    st.header("🧩 Passo 1 - Representação Vetorial (Simulada)")

    st.markdown("""
    Neste passo, utilizamos coordenadas contínuas (0 a 1) para representar formas geométricas.

    ✔ Independente de resolução  
    ✔ Base para gráficos vetoriais  
    """)

    mostrar(passo1(), "Imagem Vetorial Simulada")


elif opcao == "Passo 2 - Matricial":
    st.header("🧩 Passo 2 - Imagem Matricial")

    st.markdown("""
    Aqui cada pixel é calculado manualmente usando a equação do círculo:

    **(x - xc)² + (y - yc)² ≤ r²**

    ✔ Controle direto dos pixels  
    ✔ Base das imagens digitais  
    """)

    mostrar(passo2(), "Círculo Matricial")


elif opcao == "Passo 3 - Conversão":
    st.header("🧩 Passo 3 - Vetor → Bitmap")

    st.markdown("""
    Neste passo ocorre a rasterização:

    **pixel = coordenada × resolução**

    ✔ Conversão de dados matemáticos em imagem  
    ✔ Processo usado em GPUs e jogos  
    """)

    mostrar(passo3(), "Imagem Convertida")
