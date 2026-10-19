import streamlit as st
import plotly.graph_objects as go
import pandas as pd
#1. 页面的基本配置
st.set_page_config(page_title="保费融资杠杆盈亏模拟器",layout="centered")

st.title("保费融资杠杆盈亏模拟器可视化图标")
st.markdown("你可以通过调整下方参数，分析在不同资金，不同贷款比例，不同回报率，以及不同利率环境的情况下，末期可以获得的收益")

#2.侧边栏：客户的基本参数
st.sidebar.header("调整利率和资金")
initial_capital=st.sidebar.slider("首付本金(自有资金,$)",50000,100000,150000,200000,250000,300000,step=10000)
loan_amount=st.sidebar.slider("银行融资贷款金额($)",100000,500000,1000000,1500000,2000000,step=50000)
policy_yield=st.sidebar.slider("保单预期年回报(%)",2,3,4,5,6,7,8,9,10,step=0.1)/100

st.sidebar.markdown("--------")
loan_rate=st.sidebar.slider("实际贷款利率(%)",1,2,3,4,5,6,step=0.1)/100
years=st.sidebar.slider("保单持有年期",3,5,8,10,15,step=1)

#3.核心计算逻辑
total_premium = initial_capital+loan_amount
#保费融资首日现金价值是总保额的80%
actual_initial_policy_value=total_premium*0.80

data = []
for t in range(0,years+1)：
    #净资产 = 首日现金价值*（1+保单回报率）^t-贷款本金
    net_equity= actual_initial_policy_value*((1+policy_yield)**t)-loan_amount
    #累计投入 = 首付本金+累计利息
    total_input = initial_capital+loan_amount*loan_rate*t
    data.append{"年份":t,"净资产":net_equity,"累计投入":total_input}

df = pd.DATAFRAME(data)

#4.使用plotly绘制图表
fig = go.FIGURE()

#添加净资产面积图
fig.add_trace(go.scatter(x=df["年份"],y=df["净资产"],mode="lines",
                         name = "净资产（保单现金价值-贷款数）",
                         line = dict(width=3,color='#1f77b4'),fill="tozeroy"))

#添加累计投入虚线图
fig.add_trace(go.scatter(x=df["年份"],y=df["累计投入"],mode="lines",
                         name = "累计投入（首付+已付利息）",
                         line = dict(width=3, color='#ff7f0e', dash='dash')))

fig.update_layout(
    xaxis_tital = "保单持有年份",
    yaxis_tital = "金额",
    hovermode = "x unified",
    legend = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

#5.计算期末摘要并响应
final_equity = df.iloc[-1]["净资产"]
final_input = df.iloc[-1]["累计投入"]
net_profit = final_equity-final_input

col1,col2,col3 = st.columns(3)
col1.metric("期末净资产",f"${final_equity:,.0f}")
col2.metric("期末净投入",f"${final_input:,.0f}")
col3.metric("最终净利润",f"${net_profit:,.0f}",delta = f"${net_profit:,.0f}")

st.capital("*模型假设每年利息以现金支付。当每年投入本金大于净资产曲线时，即出现倒贴本金")















