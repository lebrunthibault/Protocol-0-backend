import json
import redis
from enum import Enum
from typing import List

TaskIds = List[str]


class TaskCacheKey(Enum):
    NOTIFICATION = "p0.notification_tasks"
    REVOKED_TASKS = "p0.revoked_tasks"


class TaskCache():
    def __init__(self):
        self._cache = redis.Redis(host='localhost', port=6379, db=0)

    def clear(self):
        for key in list(TaskCacheKey):
            self._cache.delete(key.value)

    def get_tasks(self, task_type: TaskCacheKey) -> TaskIds:
        return self._get_list_from_cache(task_type)

    def revoked_tasks(self) -> TaskIds:
        return self._get_list_from_cache(TaskCacheKey.REVOKED_TASKS)

    def _get_list_from_cache(self, key: TaskCacheKey) -> List[str]:
        cache_item = self._cache.get(key.value)

        if cache_item:
            task_ids = json.loads(cache_item)
            assert isinstance(task_ids, List)
            return task_ids
        else:
            return []

    def clear_tasks(self, task_type: TaskCacheKey) -> None:
        self._cache.set(task_type.value, json.dumps([]))

    def add_task(self, task_type: TaskCacheKey, task_id: str) -> None:
        tasks = self.get_tasks(task_type)
        tasks.append(task_id)
        self._cache.set(task_type.value, json.dumps(tasks))

    def add_revoke_task(self, task_id: str) -> None:
        tasks = self.revoked_tasks()
        tasks.append(task_id)
        self._cache.set(TaskCacheKey.REVOKED_TASKS.value, json.dumps(tasks))
