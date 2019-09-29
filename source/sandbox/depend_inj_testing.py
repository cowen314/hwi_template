from source.engines.user_workflow_engine import UserWorkflowEngine
from source.application_parameters.application_parameters import LocalFileParameters
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


def test_dependency_injector_main(login_controller):
    print("This would be the top level of the application")
    login_controller.login_requested("jimbob")


class TestLoginController:
    def __init__(self, user_workflow_engine):
        self._wf_engine = user_workflow_engine

    def login_requested(self, username):
        print("Test method called")
        success = self._wf_engine.try_login(username)
        print("Login successful? %s" % success)


class ApplicationIocContainer(containers.DeclarativeContainer):
    config = providers.Configuration('config')
    print(config)

    # services
    app_params = LocalFileParameters
    application_parameters = providers.Singleton(app_params)
    init_app_params = providers.Callable(app_params.initialize)

    # engines
    ui_workflow_engine = providers.Singleton(
        UserWorkflowEngine,
        application_parameters=application_parameters)

    # controllers
    test_controller = providers.Singleton(
        TestLoginController,
        user_workflow_engine=ui_workflow_engine)

    # main
    main = providers.Callable(
        test_dependency_injector_main,
        login_controller=test_controller
    )


if __name__ == "__main__":
    container = ApplicationIocContainer(
        config={
            "test token": "test key"
        }
    )

    container.init_app_params()
    container.main()

