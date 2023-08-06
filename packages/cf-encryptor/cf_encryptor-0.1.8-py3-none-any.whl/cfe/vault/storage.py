from .crypto import *
import os, sys
import hashlib
import logging

# Data structure for an entry in the vault
class VaultEntry:
    def __init__(self, entryname="", key=None):
        self.name = entryname
        if key is None:
            key = generate_random_key()
        self.entry_key = key
        self.salt = os.urandom(16)

    def get_key(self):
        return self.entry_key

    def get_name(self):
        return self.name

    def encrypt_entry(self, password):
        key = self.entry_key.decode()
        entry = f"cfe_check,{self.name},{key}"
        key = generate_password_key(password, self.salt)
        ciphertext = encrypt(key, entry)
        return self.salt + ciphertext
    
    ''' Returns true if successfully decrypted and stored, and false otherwise '''
    def decrypt_and_store_entry(self, password, entry_ciphertext):
        salt, ciphertext = entry_ciphertext[:16], entry_ciphertext[16:]
        key = generate_password_key(password, salt)
        try:
            entry_data = decrypt(key, ciphertext).decode()

            # Check if decryption is successful
            if entry_data.startswith("cfe_check"):
                _, self.name, self.entry_key = entry_data.split(",")
                self.entry_key = str.encode(self.entry_key)
                self.salt = salt
                return True
            else:
                return False
        except:
            return False

    
# Primary Vault Class 
class Vault:
    def __init__(self, password):
        # Dictionary with hash of password: entries
        self.entries = []
        self.other_entries = []
        self.password =  password
        self._on_init()

    ''' 
    Gets a list of all data entries accessible by a 
    user passed password in the vault
    
    Inputs:

    Returns:
    a list of all data entries accessible by password
    '''
    def get_data_list(self):
        return self.entries
    
    ''' 
    Gets data for a particular entry with the name 
    entry_name 
    
    Inputs:
    entry_name - a string that represents the name of 
    entry being queried

    Returns: 
    data entry with entry_name name and accessible by password. 
    If data entry with entry_name name does not exist in vault, returns 
    None.
    '''
    def get_data(self, entry_name_prefix):
        for entry in self.entries:
            if entry.get_name().startswith(entry_name_prefix):
                return entry    
        return None

    '''
    Creates a new data entry with the name entry_name 

    Inputs:
    password - a string that represents a user password
    entry_name - a string that represents the name of the 
    entry being created

    Returns:
    new VaultEntry if vault successfully creates a new entry with that password lock
    old VaultEntry if entry with name entry_name already exists under password
    None if error occurs in creation or cannot authenticate query
    '''
    def create_data(self, entry_name):
        for entry in self.entries:
            if entry.get_name() == entry_name:
                return entry
        new_entry = VaultEntry(entry_name)
        self.entries.append(new_entry)
        self._on_save()
        return new_entry

    
    '''
    Deletes a data entry in the vault with name entry_name

    Inputs:
    entry_name - a string that represents the name of the entry to be deleted

    Returns:
    True if an entry with entry_name under that password is succesfully deleted.
    False otherwise.
    '''
    def delete_data(self, entry_name_prefix):
        i = 0
        for entry in self.entries:
            if entry.get_name().startswith(entry_name_prefix):
                self.entries.pop(i)
                self._on_save()
                return True
            else:
                i += 1
        return False

        
    ''' Called when program exits.
        Performs the following functionalities:
            - Encrypt entries
            - Save new password hash to entry dictionary to local file
    '''
    def _on_save(self):
        with open("vault/cfe_vault.dat", "wb+") as f:
            for entry in self.entries:
                entry_ct = entry.encrypt_entry(self.password)
                f.write(entry_ct)
                f.write(str.encode('\n'))
            for entry_ct in self.other_entries:
                f.write(entry_ct)
                f.write(str.encode('\n'))
            
        
    ''' Loaded when vault is initiatlized
        Performs the following functionalities:
            - Load password hash to entry dictionary from local file
            - Unhash all entries
            - Load internal data structures
    ''' 
    def _on_init(self):
        all_entries = []
        try:
            with open("vault/cfe_vault.dat", "rb") as f:
                all_entries = f.readlines()
        except:
            logging.error(f"Couldn't initialize the CFE vault. Did you run 'cfe init'?")
            sys.exit()
        
        for entry_ct in all_entries:
            potential_entry = VaultEntry()
            if potential_entry.decrypt_and_store_entry(self.password, entry_ct):
                self.entries.append(potential_entry)
            else:
                self.other_entries.append(entry_ct)
        

        
if __name__ == "__main__":
    print("Toy Example")
    entry_keys = []
    entry_keys.append(generate_random_key())
    sample_vault = Vault("password123")
    sample_vault.create_data("arkasfile.txt")
    sample_entry = sample_vault.get_data("arkasfile.txt")
    sample_vault.delete_data("arkasfile.txt")
    