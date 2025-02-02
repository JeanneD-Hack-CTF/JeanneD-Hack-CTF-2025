import random
import string

# Fonction pour générer des noms de clés de registre aléatoires avec un niveau spécifique
def generate_random_key_name(level=0):
    return f"Key_{''.join(random.choices(string.ascii_letters + string.digits, k=10))}_{level}"

# Fonction pour générer des noms de valeurs aléatoires
def generate_random_value_name():
    return "Value_" + "".join(random.choices(string.ascii_letters + string.digits, k=10))

# Fonction pour générer des données aléatoires pour les valeurs de registre
def generate_random_value_data():
    return "".join(random.choices(string.ascii_letters + string.digits, k=20))

# Fonction pour générer une valeur DWORD aléatoire
def generate_random_dword_value():
    return f"dword:{random.randint(0, 0xFFFFFFFF):08X}"

# Fonction pour générer une valeur binaire aléatoire
def generate_random_binary_value():
    return f"hex:{random.choice(['00', 'FF', 'AA', '55'])}"

# Fonction pour ajouter aléatoirement des occurrences du mot "Notice" et de la valeur spéciale dans les noms de clés et valeurs
def add_special_values_randomly(content, depth):
    special_value = "Tk9UVEhFRkxBR3tDRV9ORVNUUEFTTEVEUkFQRUFVL0ZMQUd9"
    if random.random() < 0.1:  # Ajouter "Notice" ou la valeur spéciale avec une probabilité de 10%
        if random.random() < 0.5:
            # Ajouter dans les noms des clés
            content += f"[{generate_random_key_name(depth)}\\Notice_{''.join(random.choices(string.ascii_letters + string.digits, k=5))}]\n"
        else:
            # Ajouter dans les valeurs
            content += f"\"Notice {''.join(random.choices(string.ascii_letters + string.digits, k=5))}\"=\"{generate_random_value_data()}\"\n"
    
    # Ajouter la valeur spéciale à des endroits aléatoires
    if random.random() < 0.1:  # Ajout de la valeur Tk9UVEhFRkxBR3tDRV9ORVNUUEFTTEVEUkFQRUFVL0ZMQUd9 avec une probabilité de 10%
        content += f"\"SpecialValue_{''.join(random.choices(string.ascii_letters + string.digits, k=5))}\"=\"{special_value}\"\n"
        
    return content

# Fonction pour générer des clés imbriquées jusqu'à 4 niveaux de profondeur
def generate_deep_reg_keys(parent_key, depth=4, num_values=15):
    reg_content = ""
    
    # Générer des sous-clés à chaque niveau de profondeur
    current_key = parent_key
    for i in range(depth):
        current_key = f"{current_key}\\{generate_random_key_name(i)}"
        reg_content += f"[{current_key}]\n"
        
        # Ajouter des valeurs pour cette clé
        for _ in range(num_values):
            value_name = generate_random_value_name()
            
            # Choisir aléatoirement un type de valeur (String, DWORD, Binary, etc.)
            value_type = random.choice(["string", "dword", "binary"])
            
            if value_type == "string":
                value_data = generate_random_value_data()
                reg_content += f"\"{value_name}\"=\"{value_data}\"\n"
            elif value_type == "dword":
                value_data = generate_random_dword_value()
                reg_content += f"\"{value_name}\"={value_data}\n"
            elif value_type == "binary":
                value_data = generate_random_binary_value()
                reg_content += f"\"{value_name}\"={value_data}\n"
        
        # Ajouter le mot "Notice" et la valeur spéciale de manière aléatoire
        reg_content = add_special_values_randomly(reg_content, i)
        
        reg_content += "\n"
    
    return reg_content

# Fonction pour générer le fichier .reg complet
def generate_reg_file(filename):
    with open(filename, 'w') as file:
        # Ajouter l'en-tête pour le fichier .reg
        file.write("Windows Registry Editor Version 5.00\n\n")
        
        # Définir la clé de registre de base
        base_key = "HKEY_LOCAL_MACHINE\\SOFTWARE\\CTF_Jeanne_Hack"
        
        # Générer 1500 clés imbriquées avec des valeurs aléatoires sous cette clé
        for _ in range(1500):  # Générer 1500 grandes clés de niveau supérieur
            reg_content = generate_deep_reg_keys(base_key, depth=7, num_values=25)
            file.write(reg_content)
        
        # Ajouter la clé contenant le flag spécifique, mais de manière cachée dans une sous-clé profonde
        file.write("[HKEY_LOCAL_MACHINE\\SOFTWARE\\CTF_Jeanne_Hack\\RandomKeyLevel_5\\Notice_Key_4321]\n")
        file.write("\"ResetDfsClientInfoDuringRefreshPolicy\"=dword:00000001\n")
        file.write("\"Notice\"=\"SkRIQUNLe3dlTENPbTNfdDBfV2luRG9XJF9jQFRFNm9SeV9FeHBsT3Jlcn0=\"\n")
        
        # Ajouter plusieurs occurrences de la valeur spéciale ailleurs dans le registre
        file.write("[HKEY_LOCAL_MACHINE\\SOFTWARE\\CTF_Jeanne_Hack\\Key_Random_Deep_3]\n")
        file.write("\"SpecialValue_1234\"=\"Tk9UVEhFRkxBR3tDRV9ORVNUUEFTTEVEUkFQRUFVL0ZMQUd9\"\n")
        file.write("[HKEY_LOCAL_MACHINE\\SOFTWARE\\CTF_Jeanne_Hack\\Key_Deep_2\\SubKey_A1]\n")
        file.write("\"SpecialValue_5678\"=\"Tk9UVEhFRkxBR3tDRV9ORVNUUEFTTEVEUkFQRUFVL0ZMQUd9\"\n")

# Appeler la fonction pour générer le fichier .reg
generate_reg_file("generated_complex_registry_with_hidden_flag_and_special_value_1500.reg")

