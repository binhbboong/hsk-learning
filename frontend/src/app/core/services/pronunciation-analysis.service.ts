import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment.generated';

export interface PronunciationResult {
  verdict: 'correct' | 'needs_practice';
  score: number;
  content_score: number;
  transcript: string;
  feedback_vi: string;
  focus_vi: string[];
  syllables: {
    target: string;
    tone: number;
    status: 'good' | 'review' | 'uncertain';
    heard: string;
    tip_vi: string;
  }[];
  disclaimer_vi: string;
}

@Injectable({ providedIn: 'root' })
export class PronunciationAnalysisService {
  private readonly http = inject(HttpClient);

  analyze(blob: Blob, targetText: string, targetPinyin: string): Observable<PronunciationResult> {
    const form = new FormData();
    form.append('audio', blob, `recording.${blob.type.includes('wav') ? 'wav' : 'webm'}`);
    form.append('target_text', targetText);
    form.append('target_pinyin', targetPinyin);
    return this.http.post<PronunciationResult>(
      `${environment.apiBaseUrl}/api/v1/pronunciation/analyze`,
      form,
    );
  }
}
