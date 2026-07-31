import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ReviewQuizService {
  private readonly fallbackMeanings = [
    'xin chào', 'cảm ơn', 'tạm biệt', 'học sinh',
    'giáo viên', 'bạn', 'tốt', 'Trung Quốc',
  ];

  optionsFor(card: { id: string; meaningVi: string }, meanings: string[]): string[] {
    const unique = [card.meaningVi, ...meanings, ...this.fallbackMeanings]
      .filter((value, index, values) => value && values.indexOf(value) === index);
    return [card.meaningVi, ...unique.filter((value) => value !== card.meaningVi).slice(0, 3)]
      .map((value) => ({ value, rank: this.hash(`${card.id}:${value}`) }))
      .sort((left, right) => left.rank - right.rank)
      .map(({ value }) => value);
  }

  private hash(value: string): number {
    let result = 0;
    for (const character of value) result = (result * 31 + character.charCodeAt(0)) | 0;
    return result;
  }
}
