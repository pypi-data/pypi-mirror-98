import os
import shutil
import warnings


class OutputsSettings:
    """
    Used to create the `logs` folder to monitor the convergence of the calibration algorithm.
    """
    # TODO mettre les variables par défaut à None
    # TODO: Réfléchir aux cas d'usages : est-ce qu'on veut tout ou rien,
    # TODO: ou bien la possibilité d'avoir l'affichage console et/ou logs dans un fold
    # TODO: Aussi, bien définir la création du path
    def __init__(self, settings):
        self.console_print_periodicity = None
        self.plot_periodicity = None
        self.save_periodicity = None

        self.root_path = None
        self.parameter_convergence_path = None
        self.plot_path = None
        self.patients_plot_path = None

        self._get_console_print_periodicity(settings)
        self._get_plot_periodicity(settings)
        self._get_save_periodicity(settings)
        self._create_root_folder(settings)

    def _get_console_print_periodicity(self, settings):
        if 'console_print_periodicity' not in settings.keys():
            return

        if settings['console_print_periodicity'] is None:
            self.console_print_periodicity = None
        else:
            try:
                self.console_print_periodicity = int(settings['console_print_periodicity'])
            except ValueError:
                print("The 'console_print_periodicity' parameters you provided is not an int")

    def _get_plot_periodicity(self, settings):
        if 'plot_periodicity' not in settings.keys():
            return

        if settings['plot_periodicity'] is None:
            self.plot_periodicity = None
        else:
            try:
                self.plot_periodicity = int(settings['plot_periodicity'])
            except ValueError:
                print("The 'plot_periodicity' parameters you provided is not an int")

    def _get_save_periodicity(self, settings):
        if 'save_periodicity' not in settings.keys():
            return

        if settings['save_periodicity'] is None:
            self.save_periodicity = None
        else:
            try:
                self.save_periodicity = int(settings['save_periodicity'])
            except ValueError:
                print("The 'save_periodicity' parameters you provided is not an int")

    def _create_root_folder(self, settings):
        # Get a path to put the outputs
        if 'path' not in settings.keys():
            warnings.warn("You did not provide a path for your outputs. "
                          "They have been initialized in the working directory.")
            settings['path'] = os.path.join(os.getcwd(), '_outputs')

        settings['path'] = os.path.join(os.getcwd(), settings['path'])

        parent_directory = os.path.abspath(os.path.join(settings['path'], '..'))

        # Check if the parent directory exists
        if not os.path.exists(parent_directory):
            raise ValueError(
                "Parent directory : \n {0} \n of the logs path you provided does not exist".format(parent_directory))

        # Check if the folder does not exist : if not, create
        existence_cdt = os.path.exists(settings['path'])
        if not existence_cdt:
            os.makedirs(settings['path'])

        # Check if the folder is empty or not
        emptiness_cdt = [f for f in os.listdir(settings['path']) if not f.startswith('.')] == []
        if emptiness_cdt:
            self._create_dedicated_folders(settings['path'])
        else:
            if settings['overwrite_logs_folder']:
                print('\n...overwrite logs folder...')
                self._clean_folder(settings['path'])
                self._create_dedicated_folders(settings['path'])
            else:
                raise ValueError("The logs folder already exists! Give an other path of use "
                                 "keyword argument <overwrite_logs_folder=True>.")

    def _clean_folder(self, path):
        shutil.rmtree(path)
        os.makedirs(path)

    def _create_dedicated_folders(self, path):
        self.root_path = path
        self.parameter_convergence_path = os.path.join(path, 'parameter_convergence')
        self.plot_path = os.path.join(path, 'plots')
        self.patients_plot_path = os.path.join(self.plot_path, 'patients')

        os.makedirs(self.parameter_convergence_path)
        os.makedirs(self.plot_path)
        os.makedirs(self.patients_plot_path)

    # ---- LEGACY
    # def _ask_user_if_erase(self, path):
    #     user_answer = input("Do you want to erase the existing files "
    #                         "in the logs folder {} you provided? [y]/[n]".format(path)).lower().strip()
    #     if user_answer == "y":
    #         return True
    #     elif user_answer == "n":
    #         return False
    #     else:
    #         self._ask_user_if_erase(path)
