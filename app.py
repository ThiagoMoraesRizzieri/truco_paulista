import streamlit as st
import random

def calcular_probabilidade_truco(minha_mao_original, vira, n_simulacoes=10000):
    ordem_base = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
    naipes = ['ouro', 'espadilha', 'copas', 'zap']
    
    idx_vira = ordem_base.index(vira[0])
    manilha_valor = ordem_base[(idx_vira + 1) % 10]
    
    def get_peso(carta):
        valor, naipe = carta
        if valor == manilha_valor:
            return 11 + naipes.index(naipe)
        return ordem_base.index(valor) + 1

    baralho_completo = [(v, n) for v in ordem_base for n in naipes]
    baralho_restante = [c for c in baralho_completo if c not in minha_mao_original and c != vira]
    
    meus_pesos = sorted([get_peso(c) for c in minha_mao_original], reverse=True)
    baralho_pesos = [get_peso(c) for c in baralho_restante]

    vitorias = 0
    for _ in range(n_simulacoes):
        mao_adv = sorted(random.sample(baralho_pesos, 3), reverse=True)
        resultado_rodadas = [] 
        ganhador = None

        for i in range(3):
            if meus_pesos[i] > mao_adv[i]: resultado_rodadas.append(1)
            elif mao_adv[i] > meus_pesos[i]: resultado_rodadas.append(-1)
            else: resultado_rodadas.append(0)

            if resultado_rodadas.count(1) == 2: ganhador = 'eu'; break
            if resultado_rodadas.count(-1) == 2: ganhador = 'ele'; break
            if resultado_rodadas[0] == 0:
                if len(resultado_rodadas) > 1:
                    if resultado_rodadas[1] == 1: ganhador = 'eu'; break
                    if resultado_rodadas[1] == -1: ganhador = 'ele'; break
            elif i > 0 and resultado_rodadas[i] == 0:
                if resultado_rodadas[0] == 1: ganhador = 'eu'; break
                if resultado_rodadas[0] == -1: ganhador = 'ele'; break

        if not ganhador:
            sum_res = sum(resultado_rodadas)
            ganhador = 'eu' if sum_res > 0 else 'ele'
        if ganhador == 'eu': vitorias += 1

    return vitorias / n_simulacoes

# --- INTERFACE STREAMLIT ---
st.title("🃏 Calculadora de Probabilidade: Truco Paulista")
st.markdown("Baseado em Simulações de **Monte Carlo**")

# Sidebar para configurações
st.sidebar.header("Configurações")
simulacoes = st.sidebar.slider("Número de Simulações", 1000, 50000, 10000)

# --- SEÇÃO 1: A VIRA ---
st.header("1. Defina o Vira")
col_v1, col_v2 = st.columns(2)
with col_v1:
    v_val = st.selectbox("Valor do Vira", ordem_base, index=8) 
with col_v2:
    v_naipe = st.selectbox("Naipe do Vira", naipes, index=2) 

vira = (v_val, v_naipe)

# --- ESPAÇAMENTO ---
st.markdown("---")

# --- SEÇÃO 2: MINHA MÃO ---
st.header("2. Sua Mão")
col_c1, col_c2, col_c3 = st.columns(3)

with col_c1:
    st.markdown("**Carta 1**")
    v1 = st.selectbox("Valor", ordem_base, index=9, key="v1")
    n1 = st.selectbox("Naipe", naipes, index=3, key="n1")

with col_c2:
    st.markdown("**Carta 2**")
    v2 = st.selectbox("Valor", ordem_base, index=9, key="v2")
    n2 = st.selectbox("Naipe", naipes, index=2, key="n2")

with col_c3:
    st.markdown("**Carta 3**")
    v3 = st.selectbox("Valor", ordem_base, index=9, key="v3")
    n3 = st.selectbox("Naipe", naipes, index=0, key="n3")

minha_mao = [(v1, n1), (v2, n2), (v3, n3)]

if st.button("Calcular Chance de Vitória"):
    # Validações antes de rodar a função
    if len(set(minha_mao)) < 3:
        st.error("Erro: Você selecionou cartas repetidas na mão.")
    elif vira in minha_mao:
        st.error("Erro: O vira não pode estar na sua mão.")
    else:
        # Aqui você chama sua função 'calcular_probabilidade_truco'
        # prob = calcular_probabilidade_truco(minha_mao, vira)
        st.success("Cálculo realizado!")
        with st.spinner('Rodando simulações...'):
            prob = calcular_probabilidade_truco(mao, vira, simulacoes)
            
        st.metric("Probabilidade", f"{prob*100:.2f}%")
        
        if prob > 0.7:
            st.success("🔥 TRUCA, MARRECO!")
        elif prob < 0.4:
            st.error("🤫 Vai de mansinho ou corre...")
        else:
    
            st.warning("⚖️ Jogo parelho. Cuidado no blefe.")


