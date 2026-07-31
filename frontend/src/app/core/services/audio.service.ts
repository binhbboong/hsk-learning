import { Injectable } from '@angular/core';

export interface RecordingQuality {
  durationMs: number;
  hasSpeech: boolean | null;
  size: number;
}

export function encodePcm16Wav(
  channels: Float32Array[],
  sampleRate: number,
): Blob {
  const channelCount = Math.max(1, channels.length);
  const frameCount = channels[0]?.length ?? 0;
  const bytesPerSample = 2;
  const dataLength = frameCount * channelCount * bytesPerSample;
  const buffer = new ArrayBuffer(44 + dataLength);
  const view = new DataView(buffer);

  const writeAscii = (offset: number, value: string): void => {
    for (let index = 0; index < value.length; index += 1) {
      view.setUint8(offset + index, value.charCodeAt(index));
    }
  };
  writeAscii(0, 'RIFF');
  view.setUint32(4, 36 + dataLength, true);
  writeAscii(8, 'WAVE');
  writeAscii(12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, channelCount, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * channelCount * bytesPerSample, true);
  view.setUint16(32, channelCount * bytesPerSample, true);
  view.setUint16(34, 16, true);
  writeAscii(36, 'data');
  view.setUint32(40, dataLength, true);

  let offset = 44;
  for (let frame = 0; frame < frameCount; frame += 1) {
    for (let channel = 0; channel < channelCount; channel += 1) {
      const sample = Math.max(-1, Math.min(1, channels[channel]?.[frame] ?? 0));
      view.setInt16(
        offset,
        sample < 0 ? sample * 0x8000 : sample * 0x7fff,
        true,
      );
      offset += bytesPerSample;
    }
  }
  return new Blob([buffer], { type: 'audio/wav' });
}

@Injectable({ providedIn: 'root' })
export class AudioService {
  private recorder: MediaRecorder | null = null;
  private chunks: Blob[] = [];
  private stream: MediaStream | null = null;
  private lastRecording: Blob | null = null;
  private recordingStartedAt = 0;
  private speechFrames = 0;
  private audioContext: AudioContext | null = null;
  private speechMonitor: ReturnType<typeof setInterval> | null = null;
  private lastQuality: RecordingQuality = {
    durationMs: 0,
    hasSpeech: null,
    size: 0,
  };

  speak(text: string, rate: number): boolean {
    if (!('speechSynthesis' in window) || !('SpeechSynthesisUtterance' in window)) {
      return false;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'zh-CN';
    utterance.rate = rate;
    window.speechSynthesis.speak(utterance);
    return true;
  }

  async startRecording(): Promise<boolean> {
    if (!navigator.mediaDevices?.getUserMedia || !('MediaRecorder' in window)) {
      return false;
    }
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.chunks = [];
      this.lastRecording = null;
      this.recordingStartedAt = Date.now();
      this.startSpeechMonitor(this.stream);
      this.recorder = new MediaRecorder(this.stream);
      this.recorder.addEventListener('dataavailable', (event) => {
        if (event.data.size > 0) this.chunks.push(event.data);
      });
      this.recorder.start(250);
      return true;
    } catch {
      this.cleanupStream();
      return false;
    }
  }

  async stopRecording(): Promise<string | null> {
    const recorder = this.recorder;
    if (!recorder || recorder.state === 'inactive') return null;
    return new Promise((resolve) => {
      recorder.addEventListener(
        'stop',
        async () => {
          const blob = new Blob(this.chunks, {
            type: recorder.mimeType || 'audio/webm',
          });
          const hasSpeech = this.audioContext ? this.speechFrames >= 2 : null;
          this.cleanupStream();
          this.lastRecording = await this.toSupportedUpload(blob);
          this.lastQuality = {
            durationMs: Date.now() - this.recordingStartedAt,
            hasSpeech,
            size: this.lastRecording.size,
          };
          this.recorder = null;
          resolve(URL.createObjectURL(blob));
        },
        { once: true },
      );
      recorder.stop();
    });
  }

  revokeRecording(url: string): void {
    URL.revokeObjectURL(url);
  }

  recordingBlob(): Blob | null {
    return this.lastRecording;
  }

  recordingQuality(): RecordingQuality {
    return this.lastQuality;
  }

  private async toSupportedUpload(source: Blob): Promise<Blob> {
    if (source.type === 'audio/wav' || source.type === 'audio/mpeg') {
      return source;
    }
    const AudioContextClass = window.AudioContext;
    if (!AudioContextClass) return source;
    const context = new AudioContextClass();
    try {
      const decoded = await context.decodeAudioData(await source.arrayBuffer());
      const channels = Array.from(
        { length: decoded.numberOfChannels },
        (_, index) => decoded.getChannelData(index),
      );
      return encodePcm16Wav(channels, decoded.sampleRate);
    } catch {
      return source;
    } finally {
      void context.close();
    }
  }

  private startSpeechMonitor(stream: MediaStream): void {
    const AudioContextClass = window.AudioContext;
    if (!AudioContextClass) return;
    try {
      this.audioContext = new AudioContextClass();
      const analyser = this.audioContext.createAnalyser();
      analyser.fftSize = 1024;
      this.audioContext.createMediaStreamSource(stream).connect(analyser);
      const samples = new Float32Array(analyser.fftSize);
      this.speechFrames = 0;
      this.speechMonitor = setInterval(() => {
        analyser.getFloatTimeDomainData(samples);
        const rms = Math.sqrt(
          samples.reduce((sum, sample) => sum + sample * sample, 0) /
            samples.length,
        );
        if (rms >= 0.015) this.speechFrames += 1;
      }, 100);
    } catch {
      this.audioContext = null;
    }
  }

  private cleanupStream(): void {
    if (this.speechMonitor) clearInterval(this.speechMonitor);
    this.speechMonitor = null;
    void this.audioContext?.close();
    this.audioContext = null;
    this.stream?.getTracks().forEach((track) => track.stop());
    this.stream = null;
  }
}
