from d6tflow.tasks import TaskData
from d6tflow.targets.torch import PyTorchTarget

class PyTorchModel(TaskData):
    """
    Task which saves to .torch models
    """
    target_class = PyTorchTarget
    target_ext = '.torch'

