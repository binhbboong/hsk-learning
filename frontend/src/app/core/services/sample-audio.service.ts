import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment.generated';

@Injectable({ providedIn: 'root' })
export class SampleAudioService {
  private readonly http = inject(HttpClient);

  synthesize(text: string, speed: number): Observable<Blob> {
    return this.http.post(
      `${environment.apiBaseUrl}/api/v1/pronunciation/sample`,
      { text, speed },
      { responseType: 'blob' },
    );
  }
}
