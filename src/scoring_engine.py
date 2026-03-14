from .transcription import AudioTranscriber
from .audio_processing import AudioAnalyzer
from .text_analysis import TextAnalyzer

class ScoringEngine:
    def __init__(self):
        self.transcriber = AudioTranscriber()
        self.audio_analyzer = AudioAnalyzer()
        self.text_analyzer = TextAnalyzer()

    def _pacing_score(self, wpm):
        if wpm <= 0:
            return 0
        if 130 <= wpm <= 170:
            return 100
        elif wpm < 130:
            return max(0, 100 - ((130 - wpm) * 1.2))
        else:
            return max(0, 100 - ((wpm - 170) * 1.2))

    def _clarity_score(self, filler_count, total_words):
        if total_words == 0:
            return 0
        filler_ratio = filler_count / total_words
        penalty = filler_ratio * 200
        return max(0, int(100 - penalty))

    def _engagement_score(self, pitch_variation, vocab_richness, pause_count):
        pitch_score = min(100, (pitch_variation / 60.0) * 100)
        vocab_score = min(100, vocab_richness * 100)

        if pause_count <= 2:
            pause_penalty = 0
        elif pause_count <= 5:
            pause_penalty = (pause_count - 2) * 5
        else:
            pause_penalty = 15 + (pause_count - 5) * 8

        pause_penalty = min(40, pause_penalty)
        raw_score = (pitch_score * 0.4) + (vocab_score * 0.4)
        return max(0, int(raw_score - pause_penalty))

    def generate_report(self, audio_path):
        transcription_res = self.transcriber.transcribe(audio_path)
        transcript = transcription_res.get('text', '').strip()

        if not transcript:
            return self._empty_report("Transcription returned no speech. Please check your audio file.")

        audio_metrics = self.audio_analyzer.analyze(audio_path)
        active_duration = audio_metrics.get("active_duration", 0)
        pitch_variation = audio_metrics.get("pitch_variation", 0)
        pause_count = audio_metrics.get("pause_count", 0)

        text_metrics = self.text_analyzer.analyze(transcript)
        total_words = text_metrics.get("total_words", 0)
        filler_count = text_metrics.get("filler_count", 0)
        vocab_richness = text_metrics.get("vocab_richness", 0)

        if active_duration > 0 and total_words > 0:
            wpm = (total_words / active_duration) * 60
        else:
            wpm = 0

        pacing_score = self._pacing_score(wpm)
        clarity_score = self._clarity_score(filler_count, total_words)
        engagement_score = self._engagement_score(pitch_variation, vocab_richness, pause_count)

        overall_score = (
            (clarity_score * 0.40) +
            (pacing_score * 0.35) +
            (engagement_score * 0.25)
        )

        semantic_feedback = self.text_analyzer.semantic_analysis(transcript)

        return {
            "scores": {
                "overall": int(overall_score),
                "pacing": int(pacing_score),
                "clarity": int(clarity_score),
                "engagement": int(engagement_score)
            },
            "raw_metrics": {
                "wpm": int(wpm),
                "filler_count": filler_count,
                "pauses": pause_count,
                "active_duration": round(active_duration, 1),
                "total_words": total_words,
                "vocab_richness": round(vocab_richness, 2)
            },
            "transcript": transcript,
            "segments": transcription_res.get("segments", []),
            "semantic_feedback": semantic_feedback
        }

    def _empty_report(self, message):
        return {
            "scores": {
                "overall": 0,
                "pacing": 0,
                "clarity": 0,
                "engagement": 0
            },
            "raw_metrics": {
                "wpm": 0,
                "filler_count": 0,
                "pauses": 0,
                "active_duration": 0,
                "total_words": 0,
                "vocab_richness": 0
            },
            "transcript": "",
            "segments": [],
            "semantic_feedback": message
        }