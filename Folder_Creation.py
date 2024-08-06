import os

class SimulationFolderManager:
    def __init__(self, main_folder):
        self.main_folder = main_folder
    
    def get_sub_folders(self):
        # Get list of sub-folders
        return [f for f in os.listdir(self.main_folder) if os.path.isdir(os.path.join(self.main_folder, f)) and f.startswith("Sim ")]
    
    def extract_sim_numbers(self, sub_folders):
        # Extract the numbers from sub-folder names
        sim_numbers = []
        for folder in sub_folders:
            try:
                number = int(folder.split()[1])
                sim_numbers.append(number)
            except ValueError:
                pass
        return sim_numbers

    def get_new_folder_name(self):
        sub_folders = self.get_sub_folders()
        sim_numbers = self.extract_sim_numbers(sub_folders)
        
        if sim_numbers:
            max_sim_number = max(sim_numbers)
            new_sim_number = max_sim_number + 1
        else:
            new_sim_number = 1
        
        new_folder_name = f"Sim {new_sim_number}"
        return new_folder_name
    
    def create_new_sim_folder(self):
        new_folder_name = self.get_new_folder_name()
        new_folder_path = os.path.join(self.main_folder, new_folder_name)
        
        # Create the new folder and its sub-folders
        os.makedirs(new_folder_path)
        os.makedirs(os.path.join(new_folder_path, "star_field"))
        os.makedirs(os.path.join(new_folder_path, "data"))
        
        print(f"Created new folder: {new_folder_path}")
        print(f"Created sub-folders: 'star_field' and 'data' inside {new_folder_name}")
        
        return new_folder_path

    
