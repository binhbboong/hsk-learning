import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment.generated';
import {
  SkillCatalog,
  SkillKind,
  SkillLesson,
} from '../models/skill-lesson';


@Injectable({ providedIn: 'root' })
export class SkillApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiBaseUrl}/api/v1/skills`;

  getCatalog(): Observable<SkillCatalog> {
    return this.http.get<SkillCatalog>(this.baseUrl, {
      params: new HttpParams().set('level', 1),
    });
  }

  getLesson(
    kind: Exclude<SkillKind, 'vocabulary'>,
  ): Observable<SkillLesson> {
    return this.http.get<SkillLesson>(`${this.baseUrl}/${kind}`, {
      params: new HttpParams().set('level', 1),
    });
  }
}
