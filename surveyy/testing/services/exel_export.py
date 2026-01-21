from django.conf import settings
import os
import pandas as pd
from ..models import Test

SHEETS_DIR = settings.BASE_DIR / "sheets"

COLUMNS = [
    "username",
    "test",
    "question_id",
    "question",
    
    "question_type",
    "answer",
    "answer_correct",
    "user_selected",
]

def export_exel(test: Test):
    user_tests = test.passes.select_related('user').prefetch_related(
        'answers__selected_answers', 'answers__question__answers')

    rows = []
    for ut in user_tests:
        for ua in ut.answers.all():
            selected_ids = set(ua.selected_answers.values_list("id"))
            
            for answer in ua.question.answers.all():
                rows.append([
                    ut.user.username,
                    test.title,
                    ua.question.id,
                    ua.question.text,
                    ua.question.question_type,
                    answer.text,
                    answer.is_correct,
                    answer.id in selected_ids,
                ])
                
    df = pd.DataFrame(rows, columns=COLUMNS)
    file_path = SHEETS_DIR / f"test_{test.id}_analytics.xlsx"
    df.to_excel(file_path, index=False)
    return file_path