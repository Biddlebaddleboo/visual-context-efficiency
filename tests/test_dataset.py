from pathlib import Path

from vce.dataset import load_tasks


def test_sample_dataset_loads():
    tasks = load_tasks(Path("dataset/tasks.jsonl"))
    assert len(tasks) >= 10
    assert len({task.task_id for task in tasks}) == len(tasks)
    assert all(task.instruction for task in tasks)
