# pylint: disable = invalid-name, not-callable
from injecta.container.ContainerInterface import ContainerInterface
from databricksbundle.display import display as displayFunction
from databricksbundle.notebook.decorator.DecoratorMetaclass import DecoratorMetaclass
from datalakebundle.notebook.decorator.DataFrameReturningDecorator import DataFrameReturningDecorator
from datalakebundle.notebook.decorator.DuplicateColumnsChecker import DuplicateColumnsChecker

class transformation(DataFrameReturningDecorator, metaclass=DecoratorMetaclass):

    def __init__(self, *args, display=False, checkDuplicateColumns=True): # pylint: disable = unused-argument
        self._display = display
        self._checkDuplicateColumns = checkDuplicateColumns

    def afterExecution(self, container: ContainerInterface):
        if self._checkDuplicateColumns and container.getParameters().datalakebundle.notebook.duplicateColumnsCheck.enabled is True:
            duplicateColumnsChecker: DuplicateColumnsChecker = container.get(DuplicateColumnsChecker)

            dataFrameDecorators = tuple(decoratorArg for decoratorArg in self._decoratorArgs if isinstance(decoratorArg, DataFrameReturningDecorator))
            duplicateColumnsChecker.check(self._result, dataFrameDecorators)

        if self._display and container.getParameters().datalakebundle.notebook.display.enabled is True:
            displayFunction(self._result)
