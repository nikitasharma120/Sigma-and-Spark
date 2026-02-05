import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
from pathlib import Path
import os

# Page configuration
st.set_page_config(
    page_title="Faculty Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load data with flexible path handling
@st.cache_data
def load_data():
    """Load data from JSON file - checks multiple locations"""
    
    # Possible file locations
    possible_paths = [
        'data_exploration_stats.json' # Same directory
    ]
    
    # Try each path
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    st.sidebar.success(f"✅ Loaded data from: {path}")
                    return data
            except json.JSONDecodeError:
                st.error(f"❌ Invalid JSON in {path}")
                continue
    
    # If no file found, show error with helpful info
    st.error("❌ Error: Could not find data file!")
    st.info("""
    **Looking for one of these files:**
    - data_exploration_stats.json
    - analytics/data_exploration_output.json
    
    **Current directory:** {}
    
    **Files found in current directory:**
    {}
    """.format(
        os.getcwd(),
        "\n".join(os.listdir('.'))
    ))
    st.stop()

# Try to load data
try:
    data = load_data()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info(f"Current working directory: {os.getcwd()}")
    st.info(f"Files in current directory: {os.listdir('.')}")
    st.stop()

# Title
st.title("🎓 Faculty Analytics Dashboard")
st.markdown("---")

# Overview Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Faculty", data['meta']['total_profiles'])

with col2:
    total_pubs = sum(data['publication_type_distribution'].values())
    st.metric("Total Publications", total_pubs)

with col3:
    st.metric("Avg Courses/Faculty", f"{data['teaching_statistics']['avg_courses_per_faculty']:.2f}")

with col4:
    completeness = (1 - sum(data['missing_values_summary'].values()) / 
                   (data['meta']['total_profiles'] * 6)) * 100
    st.metric("Profile Completeness", f"{completeness:.1f}%")

st.markdown("---")

# Tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["📊 Faculty Distribution", "📚 Publications", "🔍 Data Quality", "🔬 Specializations"])

# TAB 1: Faculty Distribution
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Faculty Type Distribution")
        faculty_data = data['faculty_type_distribution']
        
        fig = go.Figure(data=[go.Pie(
            labels=list(faculty_data.keys()),
            values=list(faculty_data.values()),
            hole=0.4
        )])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Faculty Count by Type")
        
        df_faculty = pd.DataFrame({
            'Type': list(faculty_data.keys()),
            'Count': list(faculty_data.values())
        }).sort_values('Count', ascending=False)
        
        fig = px.bar(
            df_faculty,
            x='Type',
            y='Count',
            color='Count',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Statistics table
    st.markdown("### Statistics Summary")
    total = sum(faculty_data.values())
    stats_data = []
    for ftype, count in sorted(faculty_data.items(), key=lambda x: x[1], reverse=True):
        stats_data.append({
            'Faculty Type': ftype.title(),
            'Count': count,
            'Percentage': f"{(count/total)*100:.1f}%"
        })
    
    st.dataframe(pd.DataFrame(stats_data), use_container_width=True, hide_index=True)

# TAB 2: Publications
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Publication Type Distribution")
        pub_data = data['publication_type_distribution']
        
        fig = go.Figure(data=[go.Pie(
            labels=list(pub_data.keys()),
            values=list(pub_data.values()),
            textposition='inside',
            textinfo='percent+label'
        )])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Publication Counts")
        
        df_pubs = pd.DataFrame({
            'Type': list(pub_data.keys()),
            'Count': list(pub_data.values())
        }).sort_values('Count', ascending=True)
        
        fig = px.bar(
            df_pubs,
            x='Count',
            y='Type',
            orientation='h',
            text='Count',
            color='Count',
            color_continuous_scale='Viridis'
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Publication statistics
    st.markdown("### Publication Insights")
    total_pubs = sum(pub_data.values())
    avg_pubs = total_pubs / data['meta']['total_profiles']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Publications", total_pubs)
    with col2:
        st.metric("Avg per Faculty", f"{avg_pubs:.2f}")
    with col3:
        most_common = max(pub_data.items(), key=lambda x: x[1])
        st.metric("Most Common Type", most_common[0].title())

# TAB 3: Data Quality
with tab3:
    st.subheader("Profile Completeness Analysis")
    
    missing_data = data['missing_values_summary']
    total_profiles = data['meta']['total_profiles']
    
    # Create DataFrame
    df_missing = pd.DataFrame({
        'Field': [k.replace('contact.', '').title() for k in missing_data.keys()],
        'Missing': list(missing_data.values()),
        'Complete': [total_profiles - v for v in missing_data.values()],
        'Missing %': [(v/total_profiles)*100 for v in missing_data.values()],
        'Complete %': [((total_profiles - v)/total_profiles)*100 for v in missing_data.values()]
    }).sort_values('Missing %', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Stacked bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Complete',
            y=df_missing['Field'],
            x=df_missing['Complete'],
            orientation='h',
            marker_color='#4ECDC4',
            text=df_missing['Complete'],
            textposition='inside'
        ))
        
        fig.add_trace(go.Bar(
            name='Missing',
            y=df_missing['Field'],
            x=df_missing['Missing'],
            orientation='h',
            marker_color='#FF6B6B',
            text=df_missing['Missing'],
            textposition='inside'
        ))
        
        fig.update_layout(
            barmode='stack',
            height=400,
            xaxis_title="Number of Profiles",
            yaxis_title="",
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Completeness Score")
        for _, row in df_missing.iterrows():
            st.markdown(f"**{row['Field']}**")
            st.progress(row['Complete %'] / 100)
            st.caption(f"{row['Complete %']:.1f}% complete ({int(row['Complete'])}/{total_profiles})")
            st.markdown("")
    
    # Detailed table
    st.markdown("### Detailed Breakdown")
    st.dataframe(
        df_missing[['Field', 'Complete', 'Missing', 'Complete %', 'Missing %']],
        use_container_width=True,
        hide_index=True
    )

# TAB 4: Specializations
with tab4:
    spec_data = data['specialization_distribution']
    
    # Filter out "Not Available" and single-faculty specializations
    spec_filtered = {k: v for k, v in spec_data.items() 
                    if k != "Not Available" and v > 1}
    
    # Get top 15
    top_specs = dict(sorted(spec_filtered.items(), 
                           key=lambda x: x[1], reverse=True)[:15])
    
    st.subheader("Top 15 Research Specializations")
    
    df_specs = pd.DataFrame({
        'Specialization': list(top_specs.keys()),
        'Faculty Count': list(top_specs.values())
    }).sort_values('Faculty Count', ascending=True)
    
    fig = px.bar(
        df_specs,
        x='Faculty Count',
        y='Specialization',
        orientation='h',
        text='Faculty Count',
        color='Faculty Count',
        color_continuous_scale='Plasma'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Unique Specializations", len(spec_data))
    
    with col2:
        most_common = max(spec_data.items(), key=lambda x: x[1])
        st.metric("Most Common", most_common[0])
    
    with col3:
        single_spec = len([v for v in spec_data.values() if v == 1])
        st.metric("Single-Faculty Specializations", single_spec)
    
    # Top 10 list
    st.markdown("### Top 10 Research Areas")
    top_10 = sorted(spec_filtered.items(), key=lambda x: x[1], reverse=True)[:10]
    
    for i, (spec, count) in enumerate(top_10, 1):
        st.markdown(f"{i}. **{spec}** - {count} faculty")

# Additional Teaching & Research Stats
st.markdown("---")
st.subheader("📈 Teaching & Research Metrics")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Teaching Statistics")
    avg_courses = data['teaching_statistics']['avg_courses_per_faculty']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_courses,
        title={'text': "Avg Courses per Faculty"},
        gauge={
            'axis': {'range': [None, 5]},
            'bar': {'color': "#4ECDC4"},
            'steps': [
                {'range': [0, 2], 'color': "lightgray"},
                {'range': [2, 4], 'color': "#E5F5F5"},
                {'range': [4, 5], 'color': "#FFE5CC"}
            ]
        }
    ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### Research Activity")
    avg_research = data['research_statistics']['avg_topics_per_faculty']
    
    st.metric("Avg Research Topics per Faculty", f"{avg_research:.2f}")
    
    # Estimate faculty with/without research
    with_research = int(avg_research * data['meta']['total_profiles'])
    without_research = data['meta']['total_profiles'] - with_research
    
    fig = go.Figure(data=[
        go.Bar(name='With Research Topics', x=['Faculty'], y=[with_research], marker_color='#4ECDC4'),
        go.Bar(name='Without Research Topics', x=['Faculty'], y=[without_research], marker_color='#FF6B6B')
    ])
    fig.update_layout(barmode='stack', height=300, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Faculty Analytics Dashboard | Built with Streamlit & Plotly</p>
        <p>Developed by Sigma & Spark Team</p>
    </div>
""", unsafe_allow_html=True)
