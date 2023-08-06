# standard library imports
import collections.abc
import functools
import logging
import os
import socket
import threading
import time
import typing
from typing_extensions import TypedDict, Literal  # be backwards compatabile with python 3.6 and 3.7
from abc import ABC, abstractmethod
from concurrent.futures import Future

# third-party imports
import grpc
from grpc import RpcError
from grpc._channel import _Rendezvous
from grpc.framework.foundation import logging_pool
from google.protobuf import json_format

# application imports
from pyconductor_grpc.service.task_service_pb2 import (
    AckTaskRequest,
    AckTaskResponse,
    BatchPollRequest,
    PollRequest,
    PollResponse,
    UpdateTaskRequest,
)
from pyconductor_grpc.service.task_service_pb2_grpc import TaskServiceStub
from pyconductor_grpc.service.workflow_service_pb2 import GetWorkflowStatusRequest
from pyconductor_grpc.service.workflow_service_pb2_grpc import WorkflowServiceStub
from pyconductor_grpc.model.startworkflowrequest_pb2 import StartWorkflowRequest
from pyconductor_grpc.model.taskresult_pb2 import TaskResult


# java client forces client caller to provide worker id
default_worker_id = socket.gethostname()

# logs
logging.basicConfig(level=os.getenv('LOGLEVEL', logging.INFO))


class ConductorTask(TypedDict, total=False):
    taskType: str
    status: Literal[
        'IN_PROGRESS',
        'CANCELED',
        'FAILED',
        'FAILED_WITH_TERMINAL_ERROR',
        'COMPLETED',
        'COMPLETED_WITH_ERRORS',
        'SCHEDULED',
        'TIMED_OUT',
        'SKIPPED',
    ]
    inputData: dict
    referenceTaskName: str
    retryCount: int
    seq: int
    correlationId: str
    pollCount: int
    taskDefName: str
    scheduledTime: int
    startTime: int
    endTime: int
    updateTime: int
    startDelayInSeconds: int
    retriedTaskId: str
    retried: bool
    executed: bool
    callbackFromWorker: bool
    responseTimeoutSeconds: int
    workflowInstanceId: str
    workflowType: str
    taskId: str
    reasonForIncompletion: str
    callbackAfterSeconds: int
    workerId: str
    outputData: dict
    #     WorkflowTask workflowTask = 27;
    domain: str
    #     google.protobuf.Any inputMessage = 29;
    #     google.protobuf.Any outputMessage = 30;
    rateLimitPerFrequency: int
    rateLimitFrequencyInSeconds: int
    externalInputPayloadStoragePath: str
    externalOutputPayloadStoragePath: str
    workflowPriority: int
    executionNameSpace: str
    isolationGroupId: str
    iteration: int
    subWorkflowId: str


# using alternative TypedDict syntax because of key called @type
ConductorOutputMessage = TypedDict('ConductorOutputMessage', {
    '@type': str,  # 'conductor.proto.TaskExecLog'
    'log': str,
    'taskId': str,
    'createdTime': int,  # milliseconds since epoch
})


class ConductorTaskResult(TypedDict, total=False):
    workflowInstanceId: str
    taskId: str
    reasonForIncompletion: str
    callbackAfterSeconds: int
    workerId: str
    status: Literal[
        'IN_PROGRESS',
        'FAILED',
        'FAILED_WITH_TERMINAL_ERROR',
        'COMPLETED',
    ]
    outputData: dict
    outputMessage: ConductorOutputMessage


class ConductorWorkflow(TypedDict, total=False):
    status: Literal[
        'RUNNING',
        'COMPLETED',
        'FAILED',
        'TIMED_OUT',
        'TERMINATED',
        'PAUSED',
    ]
    endTime: int
    workflowId: str
    parentWorkflowId: str
    parentWorkflowTaskId: str
    tasks: typing.List[ConductorTask]
    input: dict
    output: dict
    workflowType: str
    version: int
    correlationId: str
    reRunFromWorkflowId: str
    reasonForIncompletion: str
    schemaVersion: int
    event: str
    taskToDomain: dict
    failedReferenceTaskNames: typing.List[str]
    #     WorkflowDef workflowDefinition = 19;
    externalInputPayloadStoragePath: str
    externalOutputPayloadStoragePath: str
    priority: int
    variables: dict
    lastRetriedTime: int


class AckTaskFailed(Exception):
    def __eq__(self, other):
        return True


def replace_grpc_error_with(error):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except RpcError as e:
                new_error = error()
                new_error.code = e.code
                new_error.details = e.details
                raise new_error from e
        return wrapper

    return decorator


class ConductorError(Exception):
    """Base Exception for errors coming back from conductor or the protocol"""


class StartWorkflowError(ConductorError):
    """Indicates that there was an error in the request/response for the start_workflow endpoint"""


class GetWorkflowStatusError(ConductorError):
    """Indicates that there was an error in the request/response for the get_workflow_status endpoint"""


class PollError(ConductorError):
    """Indicates that there was an error in the request/response for the poll endpoint"""


class AckTaskError(ConductorError):
    """Indicates that there was an error in the request/response for the ack_task endpoint"""


class UpdateTaskError(ConductorError):
    """Indicates that there was an error in the request/response for the update_task endpoint"""


class StreamingError(ConductorError):
    """Indicates that there was an error in the request/response for the update_task endpoint"""


class NonGrpcIterator(collections.abc.Iterator):

    def __init__(self, iterator):
        self.iterator = iterator

    @replace_grpc_error_with(StreamingError)  # rethrow core GRPC errors as a ConductorError
    def __next__(self):
        result = None
        while result is None:
            try:
                result = next(self.iterator)
            except _Rendezvous:
                continue  # skip normal errors in the course of streaming due to items no longer being available
        return json_format.MessageToDict(result)  # convert GRPC messages to dicts


class ClientBase(object):
    def __init__(self, connection_uri: str = None, channel: grpc.Channel = None):
        """
        Specify a connection URI or a custom channel object.
        If a URI is specified, a channel will automatically be created.
        If a channel object is specified, the URI will be ignored.
        Default is to connect to localhost:8090

        :param connection_uri: URI of Conductor API
        :param channel: gRPC channel
        """
        if not channel:
            if not connection_uri:
                connection_uri = os.getenv("CONDUCTOR_SERVER_URL", "localhost:8090")
            self._channel = grpc.insecure_channel(connection_uri)
        else:
            self._channel = channel


class WorkflowService(ClientBase):
    """Conductor Workflow API client."""

    def __init__(self, connection_uri: str = None, channel: grpc.Channel = None):
        """See ClientBase for descriptions of connection_uri and channel."""
        super(WorkflowService, self).__init__(connection_uri, channel)
        self.stub = WorkflowServiceStub(self._channel)

    @replace_grpc_error_with(StartWorkflowError)
    def start_workflow(
        self,
        name: str,
        version: int = 0,
        correlation_id: str = "",
        input: typing.Dict = None,
        # task_to_domain: typing.Mapping[str, str] = None,
        # workflow_def: WorkflowDefinition = None,
        # external_input_payload_storage_path: str = "",
        priority: int = 1,
    ) -> str:
        """Starts an instance of the workflow with the given name and returns a workflow instance id."""
        response = self.stub.StartWorkflow(
            json_format.ParseDict(
                {
                    'name': name,
                    'version': version,
                    'correlation_id': correlation_id,
                    'input': input,
                    'priority': priority,
                },
                StartWorkflowRequest()
            )
        )
        return response.workflow_id

    @replace_grpc_error_with(GetWorkflowStatusError)
    def get_workflow_status(
        self,
        workflow_id: str,
        include_tasks=True,
    ) -> ConductorWorkflow:
        """Returns workflow information for the workflow instance with the given id."""
        return json_format.MessageToDict(
            self.stub.GetWorkflowStatus(
                GetWorkflowStatusRequest(
                    workflow_id=workflow_id,
                    include_tasks=include_tasks,
                )
            )
        )


class TaskService(ClientBase):
    """Conductor Task API client."""

    def __init__(self, connection_uri: str = None, channel: grpc.Channel = None):
        """See ClientBase for descriptions of connection_uri and channel."""
        super(TaskService, self).__init__(connection_uri, channel)
        self.stub = TaskServiceStub(self._channel)

    @replace_grpc_error_with(AckTaskError)
    def ack_task(self, task_id: str, worker_id: str = default_worker_id) -> bool:
        """
        Acknowledge a task poll.

        :param task_id: identifier of the task being acknowledged
        :param worker_id: identifier of the worker doing the polling
        :return: true if the task was found and acknowledged; false otherwise.
            If the server returns false, the client should NOT attempt to ack again.
        """
        ack_response: AckTaskResponse = self.stub.AckTask(
            AckTaskRequest(task_id=task_id, worker_id=worker_id)
        )
        return ack_response.ack

    def batch_poll(
        self,
        task_type: str,
        worker_id: str = default_worker_id,
        domain: str = None,
        count: int = None,
        timeout: int = None,
    ) -> typing.Iterator[ConductorTask]:
        """
        Perform a batch poll for tasks of a specific task type.

        :param task_type: the task type being polled
        :param worker_id: identifier of the worker doing the polling
        :param domain: domain of the task type
        :param count: maximum number of tasks to be returned; actual number can be less than this number
        :param timeout: poll wait timeout
        :return: iterator of tasks
        """
        batch_poll_response = self.stub.BatchPoll(
            BatchPollRequest(
                task_type=task_type,
                worker_id=worker_id,
                domain=domain,
                count=count,
                timeout=timeout,
            )
        )

        return NonGrpcIterator(batch_poll_response)

    @replace_grpc_error_with(PollError)
    def poll(
        self, task_type: str, worker_id: str = default_worker_id, domain: str = None,
    ) -> typing.Union[ConductorTask, None]:
        """
        Perform a poll for a task of a specific task type.

        :param task_type: the task type being polled
        :param worker_id: identifier of the worker doing the polling
        :param domain: domain of the task type
        :return: the task if one exists; None otherwise
        """
        response: PollResponse = self.stub.Poll(
            PollRequest(
                task_type=task_type,
                worker_id=worker_id,
                domain=domain,
            )
        )
        task = response.task
        return json_format.MessageToDict(task)

    @replace_grpc_error_with(UpdateTaskError)
    def update_task(self, result: ConductorTaskResult) -> str:
        """
        Updates the result of a task execution.

        :param result: the task result to send
        :return: the task_id
        """
        task_result = json_format.ParseDict(result, TaskResult())
        return self.stub.UpdateTask(UpdateTaskRequest(result=task_result)).task_id

    def batch_ack_tasks(
        self, tasks: typing.Iterable[ConductorTask], max_threads=1,
    ) -> typing.Tuple[typing.Tuple[ConductorTask, typing.Optional[bool], typing.Optional[Exception]], ...]:
        """
        Acknowledge many tasks. The Conductor API does not support actual batching. This method calls the
        single endpoint many times in parallel.

        :param tasks: tasks to acknowledge
        :param max_threads: number of threads for distributing requests

        Return a tuple of tuples (task_id, acked, exception) after all responses return.
        """
        def _ack_task(task: ConductorTask) -> typing.Tuple[ConductorTask, typing.Optional[bool], typing.Optional[Exception]]:
            try:
                return task, self.ack_task(task['taskId'], task['workerId']), None
            except RpcError as e:
                return task, None, e

        with logging_pool.pool(max_workers=max_threads) as executor:
            return tuple(executor.map(_ack_task, tasks))

    def batch_update_tasks(
        self, task_results: typing.Iterable[ConductorTaskResult], max_threads=1,
    ) -> typing.Tuple[typing.Tuple[ConductorTaskResult, typing.Optional[Exception]], ...]:
        """
        Update many tasks with their results. The Conductor API does not support actual batching.
        This method calls the single endpoint many times in parallel.

        :param task_results: task results to send to Conductor
        :param max_threads: number of threads for distributing requests

        Return a tuple of tuples (task result, exception) after all responses return.
        """
        def _update_task(
                task_result: ConductorTaskResult
        ) -> typing.Tuple[ConductorTaskResult, typing.Optional[Exception]]:
            try:
                self.update_task(task_result)
                return task_result, None
            except RpcError as e:
                return task_result, e

        with logging_pool.pool(max_workers=max_threads) as executor:
            return tuple(executor.map(_update_task, task_results))


class BaseTaskWorker(ABC):
    """
    Work on Conductor tasks.
    """

    def __init__(
        self,
        task_service: TaskService,
        task_type: str,
        work_function: typing.Callable,
        work_concurrency: int = 1,
        poll_interval_ms: int = 1000,
        poll_timeout_ms: int = 0,
        task_domain: str = None,
        update_retry_count: int = 3,
        worker_id: str = None,
    ):
        """
        :param task_service: TaskService instance for communicating with Conductor
        :param task_type: a task type registered with Conductor
        :param work_function: function that converts inputs to outputs
        :param work_concurrency: number of threads to allocate to this executor
        :param poll_interval_ms: minimum time (milliseconds) between poll calls to Conductor
        :param poll_timeout_ms: wait time (milliseconds) for a single poll
        :param task_domain: domain for the task type
        :param update_retry_count: maximum retries when updating a task
        :param worker_id: worker id
        """
        self._task_service = task_service
        self._task_type = task_type
        self._work_function = work_function
        self._poll_timeout_ms = poll_timeout_ms
        self._poll_interval_ms = poll_interval_ms
        self._task_domain = task_domain
        self._update_retry_count = update_retry_count
        self._worker_id = worker_id

        if work_concurrency < 1:
            raise ValueError('thread count must be greater than or equal to 1')
        self._executor = logging_pool.pool(max_workers=work_concurrency)
        self._max_thread_count = work_concurrency
        self._active_thread_count = 0
        self._active_thread_count_lock = threading.Lock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def shutdown(self):
        self._executor.shutdown()

    def work(self) -> None:
        """Work forever."""

        logging.info(
            f'Polling for task {self._task_type} at a {self._poll_interval_ms} ms interval '
            f'with {self._max_thread_count} threads, with worker id as {self._worker_id}'
        )

        while True:
            result = self._work_once()
            if result is None:
                time.sleep(self._poll_interval_ms / 1000)

    def _work_once(self) -> typing.Optional[Future]:
        # compute available threads
        available_thread_count = self._max_thread_count - self._active_thread_count

        # do nothing if thread pool has no available threads
        if available_thread_count == 0:
            return None

        tasks = tuple(self._batch_poll())

        if not tasks:
            return None

        self._before_work_once()
        future = self._executor.submit(self.execute_tasks, tasks)
        future.add_done_callback(self._after_work_once)
        return future

    def _batch_poll(self) -> typing.Iterator[ConductorTask]:
        """Wrapper for TaskService.batch_poll which handles errors during task iteration."""

        batch_poll_size = self._get_batch_poll_size()

        # batch poll for tasks; response may contain fewer tasks than requested, but it should never contain more
        return self._task_service.batch_poll(
            task_type=self._task_type,
            worker_id=self._worker_id,
            domain=self._task_domain,
            count=batch_poll_size,
            timeout=self._poll_timeout_ms,
        )

    @abstractmethod
    def _get_batch_poll_size(self) -> int:
        """Hook for subclasses to declare number of tasks in batch poll."""
        raise NotImplementedError()

    @abstractmethod
    def execute_tasks(self, tasks: typing.Iterable[ConductorTask]) -> typing.Any:
        """Hook for subclasses to execute tasks."""
        raise NotImplementedError()

    def _before_work_once(self):
        logging.debug('Reserving thread for work')
        self._adjust_active_thread_count(1)

    def _after_work_once(self, _: Future):
        logging.debug('Releasing thread for work')
        self._adjust_active_thread_count(-1)

    def _adjust_active_thread_count(self, n: int) -> None:
        """
        Increment or decrement active-thread counter.

        :param n: positive or negative integer
        """
        with self._active_thread_count_lock:
            self._active_thread_count += n


class TaskWorker(BaseTaskWorker):
    """
    Work on Conductor tasks individually.

    Usage:
    with TaskWorker(
        task_concurrency=25,
        task_service=TaskService(),
        task_type='sleep',
        work_function=work_function,
        work_concurrency=10,
    ) as worker:
        worker.work()
    """
    def __init__(self, task_concurrency: int, *args, **kwargs):
        """
        :param task_concurrency: number of tasks to run in parallel in one execute_tasks invocation.
        :param work_function: function that takes task input data items as kwargs and
            returns a single dict of task output data

        See BaseTaskWorker for definitions of remaining parameters.
        """
        super().__init__(*args, **kwargs)
        self.task_concurrency = task_concurrency

    def _get_batch_poll_size(self) -> int:
        return self.task_concurrency

    def execute_tasks(
            self, tasks: typing.Iterable[ConductorTask],
    ) -> typing.Tuple[typing.Tuple[ConductorTask, typing.Optional[ConductorTaskResult],
                      typing.Optional[Exception]], ...]:
        """Execute tasks in separate work function invocations."""
        return tuple(self._executor.map(self._execute_task, tasks))

    def _execute_task(
            self, task: ConductorTask
    ) -> typing.Tuple[ConductorTask, typing.Optional[ConductorTaskResult], typing.Optional[Exception]]:
        """
        Execute the work function for the given task instance.

        Steps:
        - ack task: notify Conductor that we are working on the task instance
        - execute work function
        - update task: notify Conductor about success or failure

        :param task: the Conductor task to execute
        :return: the orignal task along with the task result or an exception
        """
        try:
            acked = self._task_service.ack_task(task['taskId'])
        except RpcError as e:
            return task, None, e

        if not acked:
            return task, None, AckTaskFailed()

        try:
            # Task.input_data is not a proto message, but Task is
            input_data = task['inputData']
            output_data = self._work_function(**input_data)
            if output_data is not None and type(output_data) is not dict:
                raise Exception('Task work function must return a dict')
            status = 'COMPLETED'
            reason_for_incompletion = ''
        except Exception as err:
            err_msg = f'Error executing task {task["taskId"]}: {self._work_function.__name__} with error: {str(err)}'
            output_data = None
            status = 'FAILED'
            reason_for_incompletion = err_msg
        finally:
            task_result = ConductorTaskResult(
                workflowInstanceId=task.get('workflowInstanceId'),
                taskId=task['taskId'],
                reasonForIncompletion=reason_for_incompletion,
                callbackAfterSeconds=0,
                workerId=task.get('workerId'),
                status=status,
                outputData=output_data,
                outputMessage={
                    '@type': 'conductor.proto.TaskExecLog',
                    'log': '',
                    'taskId': task['taskId'],
                    'createdTime': round(time.time()*1000),
                },
            )

        try:
            self._task_service.update_task(task_result)
        except RpcError as e:
            return task, None, e

        return task, task_result, None


class BatchTaskWorker(BaseTaskWorker):
    """
    Work on Conductor tasks, one batch at a time.

    Usage:

    with BatchTaskWorker(
        batch_size=1000,
        batch_threads=10,
        task_service=TaskService(),
        task_type='sleep',
        work_function=batch_work_function,
        work_concurrency=2,
    ) as worker:
        worker.work()
    """

    def __init__(self, batch_size: int, batch_threads: int = 1, *args, **kwargs):
        """
        :param batch_size: number of tasks to provide in one call to the work function
        :param batch_threads: threads dedicated to calling single-request Conductor APIs in parallel,
            separate from work threads defined in attribute `work_concurrency`
        :param work_function: function that takes a sequence of task dicts and
            returns a sequence of output elements that are one of: dict, None, exception.
            If output element is a dict, the task is completed with the dict as output data.
            If output element is None, the task is completed with no output data.
            If output element is an exception, the task is failed and the exc. message is the "reason for incompletion".

        See BaseTaskWorker for definitions of remaining parameters.
        """
        super().__init__(*args, **kwargs)
        self.batch_size = batch_size
        self.batch_threads = batch_threads

    def _get_batch_poll_size(self) -> int:
        return self.batch_size

    def execute_tasks(
        self, tasks: typing.Iterable[ConductorTask],
    ) -> typing.Tuple[typing.Tuple[ConductorTask, typing.Optional[ConductorTaskResult], typing.Optional[Exception]], ...]:
        """Execute tasks in one batch work function invocation."""

        # ack tasks
        batch_ack_out = self._task_service.batch_ack_tasks(tasks, max_threads=self.batch_threads)

        # extract acked tasks from batch ack output
        # must check for True strictly: ack result can be False if ack is rejected or None if there is an exception
        acked_tasks = tuple(out[0] for out in batch_ack_out if out[1] is True)

        # call work_function on task dicts
        work_function_input = acked_tasks
        work_function_output: typing.Sequence[ConductorTaskResult] = self._work_function(work_function_input)

        # handle work function outputs
        task_results = []
        work_function_exceptions = dict()
        for task_result in work_function_output:
            # drop result if there is no task id because there is no way to tell what task to update
            if not isinstance(task_result, collections.abc.Mapping) or 'taskId' not in task_result:
                logging.warning(f'Work function result has no task id (dropping): {task_result}')
                continue
            else:
                task_id = task_result['taskId']
            try:
                json_format.ParseDict(task_result, TaskResult())  # TODO: should we keep this just for safety?
            except json_format.ParseError as parse_error:
                logging.warning(f'Work function result cannot be parsed: {parse_error}')
                work_function_exceptions[task_id] = parse_error
            else:
                task_results.append(task_result)

        # update tasks
        batch_update_out = self._task_service.batch_update_tasks(
            task_results=task_results, max_threads=self.batch_threads,
        )

        # compute tasks dropped by work function
        input_task_ids = set(t['taskId'] for t in acked_tasks)
        output_task_ids = set(tr['taskId'] for tr in task_results)
        work_function_dropped_task_ids = input_task_ids - output_task_ids - work_function_exceptions.keys()

        # organize final output
        batch_execute_out = self._make_batch_execution_output(
            tasks, batch_ack_out, batch_update_out, work_function_exceptions, work_function_dropped_task_ids,
        )

        return batch_execute_out

    @staticmethod
    def _make_batch_execution_output(
        tasks_in,
        batch_ack_out,
        batch_update_out,
        work_function_exceptions: typing.Dict[str, Exception],
        work_function_dropped_task_ids: typing.Set[str],
    ) -> typing.Tuple[typing.Tuple[ConductorTask, typing.Optional[ConductorTaskResult], typing.Optional[Exception]], ...]:
        """
        Make output for execute_tasks.

        :param tasks_in: tasks passed into execute_tasks
        :param batch_ack_out: output from batch_ack_tasks
        :param batch_update_out: output from batch_update_tasks
        :param work_function_dropped_task_ids: set of task ids dropped by the work function
        :param work_function_exceptions: dict of task ids and their work function exceptions
        """
        # collect exceptions and task_results by task id
        exceptions = dict()
        task_results = dict()
        for task_result, exception in batch_update_out:
            if exception is not None:
                exceptions[task_result['taskId']] = exception
            else:
                task_results[task_result['taskId']] = task_result
        for task, acked, exception in batch_ack_out:
            if exception is not None:
                exceptions[task['taskId']] = exception
            elif not acked:
                exceptions[task['taskId']] = AckTaskFailed()

        exceptions.update(**work_function_exceptions)
        exceptions.update(**{task_id: WorkFunctionDroppedTask() for task_id in work_function_dropped_task_ids})

        # return tasks in original task order
        return tuple(
            (task, task_results.get(task['taskId'], None), exceptions.get(task['taskId'], None)) for task in tasks_in
        )


class WorkFunctionDroppedTask(Exception):
    pass
