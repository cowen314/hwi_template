from source.application_parameters.application_parameters import LocalFileParameters
from source.application_parameters.application_parameter_sections import UserParameters


if __name__ == "__main__":
    user_input = input("Parameters sections may be overwritten. Enter 'Y' to proceed. Enter anything else to exit. Command: ")
    if user_input == 'Y':
        print("Writing parameter sections")
        LocalFileParameters.initialize()
        user_params = UserParameters(["co", "co", "to", "mo", "cd"])
        LocalFileParameters.write(user_params)
        LocalFileParameters.deinitialize()
    else:
        print("Parameter sections will not be written")
    print("Exiting")
