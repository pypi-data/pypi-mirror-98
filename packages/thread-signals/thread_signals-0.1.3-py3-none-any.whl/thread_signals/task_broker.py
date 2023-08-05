import threading

from thread_signals.task import TaskFuncRun


class Task_broker():
    def __init__(self, executor_thread_id):
        self._executor_thread_id = executor_thread_id

        self._task_list = []
        self._task_list_lock = threading.RLock()

        self._task_list_changed_condition = threading.Condition()

    @classmethod
    def get_any_task_list_changed_condition(cls):
        return cls._any_task_list_changed_condition

    def get_task_list_changed_condition(self):
        return self._task_list_changed_condition

    def _notify_task_list_changed(self):
        with self._task_list_changed_condition:
            self._task_list_changed_condition.notify_all()

        with type(self)._any_task_list_changed_condition:
            type(self)._any_task_list_changed_condition.notify_all()

    def _add_task_to_queue_and_wait(self, task, timeout, sync_call=True):
        # add task to list
        with self._task_list_lock:
            self._task_list.append(task)

        self._notify_task_list_changed()

        # nothing to wait
        if not sync_call:
            return

        # wait for execution if sync call
        res = task.wait(timeout)
        if not res: return False

        return (task.is_successful(), task.get_result(), task.get_exception())

    def run_func_as_task(self, func, args, kwargs, timeout, sync_call=True):
        t = TaskFuncRun(self._executor_thread_id, func, args, kwargs)
        return self._add_task_to_queue_and_wait(t, timeout, sync_call)

    def _get_earliest_task(self):
        with self._task_list_lock:
            if len(self._task_list) > 0:
                t = self._task_list[0]
                del self._task_list[0]
            else:
                t = None

        return t

    def _run_task(self, task, reraise_error=False):
        task.run_task()
        if reraise_error and not task.is_successful():
            raise task.get_exception()

    def run_all_tasks(self, reraise_error=False):
        if threading.get_ident() != self._executor_thread_id:
            raise Exception('Tasks could only be run from execution thread!')

        t = self._get_earliest_task()
        while t is not None:
            self._run_task(t, reraise_error)
            t = self._get_earliest_task()

        # notify task executors about task list changed
        self._notify_task_list_changed()

    def get_task_count(self):
        with self._task_list_lock:
            res = len(self._task_list)
        return res

    _any_task_list_changed_condition = threading.Condition()

    # one broker per thread
    _broker_list_lock = threading.RLock()
    _broker_list = {}  # thread_id: broker

    @classmethod
    def get_task_broker(cls, executor_thread_id):
        with cls._broker_list_lock:
            if executor_thread_id in cls._broker_list:
                res = cls._broker_list[executor_thread_id]
            else:
                res = cls(executor_thread_id)
                cls._broker_list[executor_thread_id] = res

        return res


def get_thread_broker(thread_ident=None):
    if thread_ident is None:
        return Task_broker.get_task_broker(threading.get_ident())
    else:
        return Task_broker.get_task_broker(thread_ident)
