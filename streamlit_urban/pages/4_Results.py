import streamlit as st

import pandas as pd
st.markdown("# Modelling Results")
st.sidebar.markdown("# Modelling Results")
#st.header("Modelling Results", divider=True)
#df = pd.read_csv("static/l2_2015.csv")
#st.map(df,color='color',size=1)


#tab_year_5, tab_year1 = st.tabs(["5 year model", "1 year model"])
#with tab_year_5:
st.subheader("5 year", divider=True)

option = int(st.selectbox(
        "Select Year",
        (2015,2016,2017,2018,2019,2020),
    ))
    
    #st.write("Trained Model Year:", option , " Predictions for Year:", option+1)
    
pred_filename = "static/export_"+str(option)+".csv"
label_filename = "static/label_"+str(option)+".csv"
#print(option)
df = pd.read_csv(label_filename)
print(df.columns)
df.loc[df["label"] ==0.0, "color"] = '#003b73' #HDU label
df.loc[df["label"] ==1.0, "color"] = '#0074b7' #LDU label
df.loc[df["label"] ==2.0, "color"] = '#bfd7ed' #peri label
df['size']=1000
     
# now read the preds 
df_preds = pd.read_csv(pred_filename)
print(df_preds.columns)
df_preds.loc[df_preds["label"] ==0.0, "color"] = '#a82810' #HDU label
df_preds.loc[df_preds["label"] ==1.0, "color"] = '#f67b50' #LDU label
df_preds.loc[df_preds["label"] ==2.0, "color"] = '#fbc490' #peri label
df_preds['size']=1
    
# concat both dfs
df_no_c = df[['longitude','latitude','label']]
df_preds_no_c = df_preds[['longitude','latitude','label']]
    
full_merge = df_no_c.merge(df_preds_no_c, how = 'inner' ,indicator=False)
    
full_merge.loc[full_merge["label"] ==2.0, "color"] = '#a3ebb1'
full_merge.loc[full_merge["label"] ==1.0, "color"] = '#18a558'
full_merge.loc[full_merge["label"] ==0.0, "color"] = '#116530' 
full_merge['size']=1
all_dfs = pd.concat([df[['longitude','latitude','label','color','size']],df_preds[['longitude','latitude','label','color','size']],full_merge], axis=0)
    
selection = st.radio(
        "",
        ["Only Labels", "Only Predictions", "Comparison"],
        horizontal = True
        )
    
if selection == "Only Labels":
            st.markdown("<span style='color:#003b73'>High Density Urban|&nbsp;</span> <span style='color:#0074b7'>Low Density Urban|&nbsp;</span> <span style='color:#bfd7ed'>Peri-Urban</span>",
                 unsafe_allow_html=True)
           
            a = st.map(df,color='color',size=1)
elif selection == "Only Predictions":
            st.markdown("<span style='color:#a82810'>High Density Urban|&nbsp; </span> <span style='color:#f67b50'>Low Density Urban|&nbsp; </span> <span style='color:#fbc490'>Peri-Urban</span>",
                 unsafe_allow_html=True)
            a = st.map(df_preds,color='color',size=1)
else:
            st.markdown("Correct Predictions - <span style='color:#116530'>High Density Urban|&nbsp; </span> <span style='color:#18a558'>Low Density Urban|&nbsp; </span> <span style='color:#a3ebb1'>Peri-Urban</span>",
                 unsafe_allow_html=True)
            a = st.map(all_dfs,color='color',size='size')