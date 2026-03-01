import numpy as np
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(page_title="Simulador IPR", layout="wide")
st.title("Simulador IPR (Streamlit + Plotly)")

with st.sidebar:
    st.header("Datos de entrada")
    pr = st.number_input("Pr (psi)", min_value=1, value=2200, step=50)
    pb = st.number_input("Pb (psi)", min_value=1, value=2000, step=50)
    q_test = st.number_input("q_test (BPD)", min_value=1, value=500, step=50)
    pwf_test = st.number_input("Pwf_test (psi)", min_value=0, value=1500, step=50)
    mostrar_escenarios = st.toggle("Mostrar escenarios -5% y -10%", value=True)

# ==============================
# VALIDACIÓN DE ENTRADAS
# ==============================
if pwf_test >= pr:
    st.error(
        f"No se permite Pwf_test mayor o igual que Pr ({pr} psi). "
        f"Valor ingresado: Pwf_test={pwf_test}"
    )
    st.stop()

# ==============================
# RANGO DE Pwf
# ==============================
pwf = np.linspace(0, pr, 200)

# ==============================
# RESERVORIO SATURADO / SUB-SATURADO
# ==============================
if pr <= pb:
    st.info("Reservorio saturado con cortes de agua menor al 50% → Aplicando Vogel")
    qmax = q_test / (1 - 0.2 * (pwf_test / pr) - 0.8 * (pwf_test / pr) ** 2)
    q = qmax * (1 - 0.2 * (pwf / pr) - 0.8 * (pwf / pr) ** 2)
    denominador = pr - pwf_test
    j = np.inf if denominador == 0 else q_test / denominador
else:
    st.info("Reservorio sub-saturado → Aplicando Darcy")
    j = q_test / (pr - pwf_test)
    q = j * (pr - pwf)

# ==============================
# GRAFICA PLOTLY
# ==============================
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=q,
        y=pwf,
        mode="lines",
        name="Curva IPR"
    )
)

fig.add_trace(
    go.Scatter(
        x=[q_test],
        y=[pwf_test],
        mode="markers",
        name="Punto de prueba",
        marker=dict(size=10)
    )
)

if mostrar_escenarios:
    pwf_test_5 = pwf_test * 0.95
    pwf_test_10 = pwf_test * 0.90

    q_esc_5 = float(np.interp(pwf_test_5, pwf, q))
    q_esc_10 = float(np.interp(pwf_test_10, pwf, q))

    fig.add_trace(
        go.Scatter(
            x=[q_esc_5],
            y=[pwf_test_5],
            mode="markers",
            name="Escenario -5% Pwf_test",
            marker=dict(size=11, symbol="diamond", color="orange")
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[q_esc_10],
            y=[pwf_test_10],
            mode="markers",
            name="Escenario -10% Pwf_test",
            marker=dict(size=11, symbol="diamond", color="green")
        )
    )

j_texto = "∞" if np.isinf(j) else f"{j:.4f}"
fig.add_annotation(
    xref="paper",
    yref="paper",
    x=0.99,
    y=0.99,
    xanchor="right",
    yanchor="top",
    text=f"Índice de Productividad (J): <b>{j_texto}</b> BPD/psi",
    showarrow=False,
    bgcolor="rgba(255,255,255,0.9)",
    bordercolor="#cfcfcf",
    borderwidth=1,
)

fig.update_layout(
    title="Inflow Performance Relationship",
    xaxis_title="Caudal (BPD)",
    yaxis_title="Pwf (psi)",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

if mostrar_escenarios:
    st.caption(
        f"Escenario -5%: Pwf_test={pwf_test_5:.1f} psi, q={q_esc_5:.2f} BPD | "
        f"Escenario -10%: Pwf_test={pwf_test_10:.1f} psi, q={q_esc_10:.2f} BPD"
    )