# pyconductor-grpc
Python GRPC client for Netflix's Conductor


## Usage
1. Define your work function:
```python
def sleep_work_function(sleep_duration: int, sleep_message: str, **kwargs) -> dict:
    time.sleep(sleep_duration)
    output_data = {'message': sleep_message}
    return output_data
```

2. Work
```python
with TaskWorker(
    task_concurrency=25,
    task_service=TaskService(),
    task_type='sleep',
    work_function=work_function,
    work_concurrency=10,
) as worker:
    worker.work()
```


## Code generation
```shell
scripts/generate-code.sh
```


## Notes
The generated Python message types verify field types when objects are constructed from them. For example:
```
>>> from model.task_result_pb2 import TaskResult
>>> TaskResult(task_id=1)
TypeError: Cannot set conductor.proto.TaskResult.task_id to 0: 0 has type <class 'int'>, but expected one of: (<class 'bytes'>, <class 'str'>) for field TaskResult.task_id
>>> TaskResult(task_id='1')
>>>
```


## Publishing
To build and upload:

```shell
pip install --upgrade build twine
python -m build
twine upload dist/*
```

or

```shell
pipx install build
pipx install twine
pyproject-build
twine upload dist/*
```
