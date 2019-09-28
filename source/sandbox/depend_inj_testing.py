from source.engines.user_workflow_engine import UserWorkflowEngine
from source.application_parameters.application_parameters import LocalFileParameters
from source.ui.controllers.simple_daq_controllers import LoginController
import pinject
from dependency_injector import containers
from dependency_injector import providers

""" PINJECT (a library) """


def test_pinject():
    obj_graph = pinject.new_object_graph()
    obj_graph.provide(LocalFileParameters)

    """
    pinject allows implicit injection of dependencies
    e.g. if I pass a class called HeatingElement to pinject and another class takes an arg heating_element in it's
    constructor, pinject will automatically pass an instance of HeatingElement as that parameter.
    
    
    """


""" DEPENDENCY-INJECTOR (another library) """


def test_dependency_injector(login_controller):
    pass


class ApplicationIocContainer(containers.DeclarativeContainer):
    # services
    application_parameters = providers.Singleton(LocalFileParameters)

    # engines
    ui_workflow_engine = providers.Singleton(
        UserWorkflowEngine,
        application_parameters=application_parameters)

    # controllers
    test_controller = providers.Singleton(
        LoginController,
        user_workflow_engine=ui_workflow_engine)

    # main
    main = providers.Callable(
        test_dependency_injector,
        login_controller=test_controller
    )


if __name__=="__main__":
    container = ApplicationIocContainer(
        config={

        }
    )

    container.main()