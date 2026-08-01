from dataclasses import dataclass
from datetime import UTC, datetime
from random import Random
from uuid import uuid4

from hsk_api.content.learning_path import CHECKPOINT, LESSONS
from hsk_api.models.learning_loop import ChoiceOption, DailyPathBundle, MultiActivityLesson
from hsk_api.models.level_exam import (
    LevelExamAttemptRecord, LevelExamAttemptResponse, LevelExamDefinition,
    LevelExamPublicQuestion, LevelExamQuestion, LevelExamResult,
    LevelExamSkillResult, LevelExamStatusResponse,
)
from hsk_api.repositories.accounts import AccountRepository
from hsk_api.services.daily_paths import DailyPathService


class LevelExamError(ValueError):
    pass


@dataclass
class LevelExamService:
    repository: AccountRepository
    daily_paths: DailyPathService

    def status(self, account_id: str) -> LevelExamStatusResponse:
        level, eligible = self._eligibility(account_id)
        current = self.repository.get_in_progress_level_exam_attempt(account_id, level)
        latest = self.repository.get_latest_completed_level_exam_attempt(account_id, level)
        passed = self.repository.has_passed_level_exam(account_id, level)
        return LevelExamStatusResponse(
            eligible=eligible and not passed, level=level, passed=passed,
            in_progress=self._response(current) if current else None,
            latest_result=latest.result if latest else None,
            reason_vi=("Bạn đã đạt bài thi tổng kết cấp này." if passed else
                       "Bạn đã sẵn sàng làm bài thi tổng kết." if eligible else
                       "Hoàn thành 5 bài, checkpoint ≥80% và ghi nhớ từ vựng ≥70% để mở bài thi."),
        )

    def start_or_resume(self, account_id: str) -> tuple[LevelExamAttemptResponse, bool]:
        level, eligible = self._eligibility(account_id)
        if self.repository.has_passed_level_exam(account_id, level):
            raise LevelExamError("Bạn đã đạt bài thi tổng kết cấp này.")
        if not eligible:
            raise LevelExamError("Bạn chưa đủ điều kiện mở bài thi tổng kết.")
        current = self.repository.get_in_progress_level_exam_attempt(account_id, level)
        if current:
            return self._response(current), False
        definition = self.repository.get_latest_level_exam(account_id, level)
        if definition is None:
            definition = self.repository.save_level_exam(self._build_definition(account_id, level))
        previous_count = self.repository.count_completed_level_exam_attempts(account_id, level)
        order = [question.id for question in definition.questions]
        if previous_count:
            Random(f"{account_id}:{level}:{previous_count}").shuffle(order)
        attempt = LevelExamAttemptRecord(
            id=str(uuid4()), account_id=account_id, exam_id=definition.id, level=level,
            question_order=order, started_at=datetime.now(UTC),
        )
        self.repository.save_level_exam_attempt(attempt)
        return self._response(attempt), True

    def save(self, account_id: str, attempt_id: str, *, question_id: str,
             option_id: str, flagged: bool, current_index: int) -> LevelExamAttemptResponse:
        attempt, definition = self._owned_attempt(account_id, attempt_id)
        if attempt.status != "in_progress":
            raise LevelExamError("Bài thi đã được nộp.")
        question = next((q for q in definition.questions if q.id == question_id), None)
        if question is None or option_id not in {option.id for option in question.options}:
            raise LevelExamError("Đáp án không hợp lệ.")
        attempt.selections[question_id] = option_id
        flags = set(attempt.flagged_question_ids)
        flags.add(question_id) if flagged else flags.discard(question_id)
        attempt.flagged_question_ids = list(flags)
        attempt.current_index = current_index
        self.repository.save_level_exam_attempt(attempt)
        return self._response(attempt)

    def submit(self, account_id: str, attempt_id: str) -> LevelExamResult:
        attempt, definition = self._owned_attempt(account_id, attempt_id)
        if attempt.status != "in_progress":
            if attempt.result is None:
                raise LevelExamError("Không tìm thấy kết quả bài thi.")
            return attempt.result
        if len(attempt.selections) != 20:
            raise LevelExamError("Hãy trả lời đủ 20 câu trước khi nộp bài.")
        skill_results = []
        for skill in ("vocabulary", "grammar", "reading", "listening"):
            questions = [q for q in definition.questions if q.skill == skill]
            correct = sum(attempt.selections.get(q.id) == q.correct_option_id for q in questions)
            skill_results.append(LevelExamSkillResult(
                skill=skill, correct=correct, percent=round(correct / len(questions) * 100),
            ))
        correct = sum(item.correct for item in skill_results)
        overall = round(correct / 20 * 100)
        result = LevelExamResult(
            level=attempt.level, correct=correct, overall_percent=overall,
            passed=overall >= 80 and all(item.percent >= 60 for item in skill_results),
            skills=skill_results, completed_at=datetime.now(UTC),
        )
        attempt.status = "completed"
        attempt.completed_at = result.completed_at
        attempt.result = result
        self.repository.save_level_exam_attempt(attempt)
        return result

    def audio_text(self, account_id: str, attempt_id: str, question_id: str) -> str:
        _, definition = self._owned_attempt(account_id, attempt_id)
        question = next((q for q in definition.questions if q.id == question_id), None)
        if question is None or question.skill != "listening" or not question.audio_text:
            raise LevelExamError("Câu này không có âm thanh nghe.")
        return question.audio_text

    def _owned_attempt(self, account_id: str, attempt_id: str):
        attempt = self.repository.get_level_exam_attempt(attempt_id)
        if attempt is None or attempt.account_id != account_id:
            raise LevelExamError("Không tìm thấy lượt thi.")
        definition = self.repository.get_level_exam(attempt.exam_id)
        if definition is None:
            raise LevelExamError("Không tìm thấy đề thi.")
        return attempt, definition

    def _response(self, attempt: LevelExamAttemptRecord) -> LevelExamAttemptResponse:
        definition = self.repository.get_level_exam(attempt.exam_id)
        by_id = {question.id: question for question in definition.questions}
        return LevelExamAttemptResponse(
            attempt_id=attempt.id, exam_id=attempt.exam_id, level=attempt.level,
            status=attempt.status,
            questions=[LevelExamPublicQuestion(
                id=by_id[qid].id, skill=by_id[qid].skill,
                prompt_vi=by_id[qid].prompt_vi, options=by_id[qid].options,
            ) for qid in attempt.question_order],
            selections=attempt.selections, flagged_question_ids=attempt.flagged_question_ids,
            current_index=attempt.current_index, started_at=attempt.started_at, result=attempt.result,
        )

    def _eligibility(self, account_id: str) -> tuple[int, bool]:
        bundles = self.repository.list_daily_paths(account_id)
        latest = bundles[-1] if bundles else DailyPathBundle(
            path_index=1, level=1, difficulty=1, lessons=LESSONS, checkpoint=CHECKPOINT,
        )
        profile = self.repository.get_profile(account_id)
        eligible = all(q.id in profile.completedLessonIds for q in latest.lessons) and self.daily_paths._is_mastered(
            profile, latest.checkpoint, [lesson.id for lesson in latest.lessons],
        )
        return latest.level, eligible

    def _build_definition(self, account_id: str, level: int) -> LevelExamDefinition:
        bundles = self.repository.list_daily_paths(account_id)
        lessons = bundles[-1].lessons if bundles else LESSONS
        questions = self._questions(lessons)
        return LevelExamDefinition(
            id=str(uuid4()), account_id=account_id, level=level,
            source_path_index=bundles[-1].path_index if bundles else 1,
            questions=questions, created_at=datetime.now(UTC),
        )

    @staticmethod
    def _questions(lessons: list[MultiActivityLesson]) -> list[LevelExamQuestion]:
        vocab = [word for lesson in lessons for word in lesson.vocabulary]
        meanings = list(dict.fromkeys(word.meaning_vi for word in vocab))
        translations = list(dict.fromkeys(line.translation_vi for lesson in lessons for line in lesson.dialogue))
        result: list[LevelExamQuestion] = []
        for index, lesson in enumerate(lessons):
            word = lesson.vocabulary[0]
            vocabulary_choices = [word.meaning_vi] + [m for m in meanings if m != word.meaning_vi]
            result.append(LevelExamService._choice(
                f"exam-vocab-{lesson.id}", "vocabulary", f"“{word.hanzi}” có nghĩa là gì?",
                vocabulary_choices[:4], word.meaning_vi,
            ))
            correct_sentence = "".join(lesson.sentence_order.correct_tokens)
            tokens = lesson.sentence_order.correct_tokens
            grammar_choices = [correct_sentence, "".join(reversed(tokens)),
                               "".join(tokens[1:] + tokens[:1]), "".join(tokens[-1:] + tokens[:-1])]
            result.append(LevelExamService._choice(
                f"exam-grammar-{lesson.id}", "grammar", "Chọn câu có trật tự đúng.",
                list(dict.fromkeys(grammar_choices)), correct_sentence,
            ))
            line = lesson.dialogue[0]
            reading_choices = [line.translation_vi] + [t for t in translations if t != line.translation_vi]
            result.append(LevelExamService._choice(
                f"exam-reading-{lesson.id}", "reading", f"“{line.hanzi}” có nghĩa là gì?",
                reading_choices[:4], line.translation_vi,
            ))
            listening = lesson.listening
            listening_choices = [option.text for option in listening.options]
            correct_text = next(option.text for option in listening.options if option.id == listening.correct_option_id)
            result.append(LevelExamService._choice(
                f"exam-listening-{lesson.id}", "listening", listening.prompt_vi,
                listening_choices, correct_text, audio_text=listening.audio_text,
            ))
        return result

    @staticmethod
    def _choice(question_id: str, skill: str, prompt: str, values: list[str], correct: str,
                audio_text: str | None = None) -> LevelExamQuestion:
        unique = list(dict.fromkeys(values))
        fillers = ["Không có đáp án phù hợp", "Cả ba đáp án trên", "Chưa đủ thông tin", "Một nghĩa khác"]
        for filler in fillers:
            if len(unique) >= 4:
                break
            if filler not in unique:
                unique.append(filler)
        options = [ChoiceOption(id=f"{question_id}-option-{i + 1}", text=value)
                   for i, value in enumerate(unique[:4])]
        return LevelExamQuestion(
            id=question_id, skill=skill, prompt_vi=prompt, options=options,
            correct_option_id=next(option.id for option in options if option.text == correct),
            audio_text=audio_text,
        )
