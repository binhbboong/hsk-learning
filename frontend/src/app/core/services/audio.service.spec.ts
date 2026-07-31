import { encodePcm16Wav } from './audio.service';

describe('AudioService WAV encoding', () => {
  it('encodes browser PCM samples as a mono 16-bit WAV upload', async () => {
    const blob = encodePcm16Wav(
      [new Float32Array([-1, 0, 0.5, 1])],
      16_000,
    );
    const bytes = new Uint8Array(await blob.arrayBuffer());
    const header = new TextDecoder().decode(bytes.slice(0, 12));

    expect(blob.type).toBe('audio/wav');
    expect(header.slice(0, 4)).toBe('RIFF');
    expect(header.slice(8)).toBe('WAVE');
    expect(bytes.length).toBe(52);
    expect(new DataView(bytes.buffer).getUint16(22, true)).toBe(1);
    expect(new DataView(bytes.buffer).getUint32(24, true)).toBe(16_000);
    expect(new DataView(bytes.buffer).getUint16(34, true)).toBe(16);
  });
});
