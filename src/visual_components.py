import plotly.graph_objects as go

def get_radar_chart(scores):
    categories = ['Pacing', 'Clarity', 'Engagement', 'Overall', 'Pacing']
    # Repeat first element to close the radar
    score_values = [
        scores['pacing'], 
        scores['clarity'], 
        scores['engagement'], 
        scores['overall'],
        scores['pacing']
    ]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=score_values,
        theta=categories,
        fill='toself',
        name='Your Score',
        fillcolor='rgba(37, 99, 235, 0.4)',
        line=dict(color='#2563EB')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False
            )
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20)
    )

    return fig
