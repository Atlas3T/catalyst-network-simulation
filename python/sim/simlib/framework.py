
class simulation_section():
    """Defines input needed from previous sections along with required config which that input must not contradict.

    """
    input_filenames
    mapped_func

    def __init__(self, name :str, description : str, config, input_requirements : list):
        """
        Args:
            name (str): Section name, will be used for any output.
            config (:obj:`dict` of :obj:`namedtuple`): Description of `param2`. Multiple
                lines are supported.
            input_requirements (:obj:`list` of :obj:`str`): Input requirement is a .

        """
        self.name = name
        self.description = description
        self.config = config
        self.input_requirements = input_requirements

        if not (self.requirements_provided()):
            Exception("Requirements can't be met.")


    def requirements_provided(self):
        """
            If requirements can be satisfied, will fill input_filenames with filenames corresponding to the input_requirements list.
        Returns:
            
                If all requirements can't be satisfied, will return False

        """
        return False

    
class new_filename_provider()
    def __init__(self, section_name):
        """
        Args:
            name (str): Section name, will be used for any output.
            config (:obj:`dict` of :obj:`namedtuple`): Description of `param2`. Multiple
                lines are supported.
            input_requirements (:obj:`list` of :obj:`str`): Description of `param3`.

        """
        self.section_name = section_name
        names_dict = []
        section_id = 
    

    def get_unique(self, object_desc: str):
        if(self.names_dict.contains(object_desc))
    


    



