from .transcription import AudioTranscriber
from .audio_processing import AudioAnalyzer
from .text_analysis import TextAnalyzer

class ScoringEngine:
    def __init__(self):
        self.transcriber = AudioTranscriber()
        self.audio_analyzer = AudioAnalyzer()
        self.text_analyzer = TextAnalyzer()

    def generate_report(self, audio_path):
        transcription_res = self.transcriber.transcribe(audio_path)
        transcript = transcription_res['text']
        
        audio_metrics = self.audio_analyzer.analyze(audio_path)
        active_duration = audio_metrics["active_duration"]
        
        text_metrics = self.text_analyzer.analyze(transcript)
        semantic_feedback = self.text_analyzer.semantic_analysis(transcript)
        
        # 1. Pacing score based on ACTIVE speech time
        if active_duration > 0:
            wpm = (text_metrics["total_words"] / active_duration) * 60
        else:
            wpm = 0
            
        pacing_score = max(0, 100 - abs(wpm - 150))
        
        # 2. Clarity/Fluency Score
        # Minus 5 points per filler word per 100 words roughly
        if text_metrics["total_words"] > 0:
            fillers_per_100 = (text_metrics["filler_count"] / text_metrics["total_words"]) * 100
        else:
            fillers_per_100 = 0
            
        clarity_score = max(0, 100 - (fillers_per_100 * 5))
        
        # 3. Engagement Score
        pitch_score = min(100, (audio_metrics["pitch_variation"] / 40.0) * 100)
        vocab_score = min(100, text_metrics["vocab_richness"] * 100)
        engagement_score = (pitch_score + vocab_score * 2) / 3
        
        overall_score = (pacing_score + clarity_score + engagement_score) / 3

        return {
            "scores": {
                "overall": int(overall_score),
                "pacing": int(pacing_score),
                "clarity": int(clarity_score),
                "engagement": int(engagement_score)
            },
            "raw_metrics": {
                "wpm": int(wpm),
                "filler_count": text_metrics["filler_count"],
                "pauses": audio_metrics["pause_count"]
            },
            "transcript": transcript,
            "segments": transcription_res["segments"],
            "semantic_feedback": semantic_feedback
        }
