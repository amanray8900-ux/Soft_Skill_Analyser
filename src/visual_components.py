import plotly.graph_objects as go

def get_radar_chart(scores):
    categories = ['Pacing', 'Clarity', 'Engagement', 'Fluency', 'Pacing']

    fluency_score = int((scores['clarity'] * 0.6) + (scores['pacing'] * 0.4))

    score_values = [
        scores['pacing'],
        scores['clarity'],
        scores['engagement'],
        fluency_score,
        scores['pacing']
    ]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=score_values,
        theta=categories,
        fill='toself',
        name='Your Score',
        fillcolor='rgba(99, 102, 241, 0.25)',
        line=dict(color='#6366F1', width=2.5),
        marker=dict(color='#6366F1', size=7)
    ))

    fig.update_layout(
        polar=dict(
            bgcolor='rgba(255,255,255,0.03)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=True,
                tickvals=[25, 50, 75, 100],
                ticktext=['25', '50', '75', '100'],
                tickfont=dict(size=10, color='rgba(255,255,255,0.4)'),
                gridcolor='rgba(255,255,255,0.1)',
                linecolor='rgba(255,255,255,0.1)',
            ),
            angularaxis=dict(
                tickfont=dict(size=13, color='rgba(255,255,255,0.85)'),
                gridcolor='rgba(255,255,255,0.1)',
                linecolor='rgba(255,255,255,0.15)',
            )
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(family="Inter, sans-serif")
    )

    return fig
    