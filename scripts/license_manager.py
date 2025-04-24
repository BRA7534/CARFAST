"""
Gestionnaire de licences et de sécurité pour CarFast
"""

import os
import json
import uuid
import hmac
import time
import base64
import hashlib
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from cryptography.fernet import Fernet
from pathlib import Path

class LicenseManager:
    """Gestionnaire de licences et de sécurité."""
    
    def __init__(self, license_key: str):
        self.license_key = license_key
        self._encryption_key = self._generate_encryption_key()
        self._fernet = Fernet(self._encryption_key)
        self._device_id = self._get_device_id()
        self._last_verification = None
        self._cache_path = Path("license_cache.enc")
        
    def _generate_encryption_key(self) -> bytes:
        """Génère une clé de chiffrement unique basée sur la licence."""
        return base64.urlsafe_b64encode(hashlib.sha256(self.license_key.encode()).digest())
        
    def _get_device_id(self) -> str:
        """Génère un ID unique pour l'appareil."""
        try:
            # Récupérer des informations matérielles uniques
            machine_id = str(uuid.getnode())  # MAC address
            if os.name == 'nt':  # Windows
                import wmi
                c = wmi.WMI()
                system_info = c.Win32_ComputerSystemProduct()[0]
                return hashlib.sha256(f"{machine_id}{system_info.UUID}".encode()).hexdigest()
            else:  # Linux/Mac
                with open('/etc/machine-id', 'r') as f:
                    machine_id = f.read().strip()
                return hashlib.sha256(machine_id.encode()).hexdigest()
        except Exception:
            # Fallback : utiliser un ID persistant stocké
            id_file = Path("device_id")
            if id_file.exists():
                return id_file.read_text().strip()
            else:
                device_id = str(uuid.uuid4())
                id_file.write_text(device_id)
                return device_id

    def _verify_signature(self, data: str, signature: str) -> bool:
        """Vérifie la signature des données."""
        expected = hmac.new(
            self.license_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected)

    def _encrypt_data(self, data: Dict) -> bytes:
        """Chiffre les données de licence."""
        return self._fernet.encrypt(json.dumps(data).encode())

    def _decrypt_data(self, encrypted_data: bytes) -> Dict:
        """Déchiffre les données de licence."""
        try:
            decrypted = self._fernet.decrypt(encrypted_data)
            return json.loads(decrypted.decode())
        except Exception:
            return {}

    def verify_license(self) -> Tuple[bool, str]:
        """
        Vérifie la validité de la licence.
        
        Returns:
            Tuple[bool, str]: (validité, message)
        """
        try:
            # Vérifier le cache si la dernière vérification est récente
            if self._last_verification and \
               (datetime.now() - self._last_verification) < timedelta(hours=24):
                if self._cache_path.exists():
                    cached_data = self._decrypt_data(self._cache_path.read_bytes())
                    if cached_data.get('valid_until') and \
                       datetime.fromisoformat(cached_data['valid_until']) > datetime.now():
                        return True, "Licence valide (cache)"

            # Préparer les données de vérification
            verification_data = {
                'license_key': self.license_key,
                'device_id': self._device_id,
                'timestamp': int(time.time()),
                'app_version': '1.0.0'
            }
            
            # Créer la signature
            signature = hmac.new(
                self.license_key.encode(),
                json.dumps(verification_data).encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Envoyer la requête de vérification
            response = requests.post(
                'https://api.carfast.com/verify_license',
                json={
                    'data': verification_data,
                    'signature': signature
                },
                timeout=10
            )
            
            if response.status_code == 200:
                license_data = response.json()
                
                # Vérifier la signature de la réponse
                if not self._verify_signature(
                    json.dumps(license_data['data']),
                    license_data['signature']
                ):
                    return False, "Signature de licence invalide"
                
                # Vérifier les restrictions
                data = license_data['data']
                if not data.get('active'):
                    return False, "Licence inactive"
                    
                if data.get('device_limit') and \
                   len(data['registered_devices']) >= data['device_limit']:
                    return False, "Limite d'appareils atteinte"
                    
                if data.get('valid_until'):
                    valid_until = datetime.fromisoformat(data['valid_until'])
                    if valid_until < datetime.now():
                        return False, "Licence expirée"
                
                # Mettre à jour le cache
                self._last_verification = datetime.now()
                self._cache_path.write_bytes(self._encrypt_data(data))
                
                return True, "Licence valide"
                
            return False, "Échec de la vérification de la licence"
            
        except Exception as e:
            # En cas d'erreur, vérifier le cache hors ligne
            if self._cache_path.exists():
                try:
                    cached_data = self._decrypt_data(self._cache_path.read_bytes())
                    if cached_data.get('valid_until'):
                        valid_until = datetime.fromisoformat(cached_data['valid_until'])
                        if valid_until > datetime.now():
                            return True, "Licence valide (hors ligne)"
                except Exception:
                    pass
            
            return False, f"Erreur de vérification: {str(e)}"

    def protect_code(self) -> None:
        """Implémente des mesures anti-débogage et anti-manipulation."""
        try:
            import sys
            import trace
            
            # Détecter les débogueurs
            def detect_debugger():
                import ctypes
                if os.name == 'nt':
                    return ctypes.windll.kernel32.IsDebuggerPresent() != 0
                else:
                    try:
                        with open('/proc/self/status') as f:
                            return 'TracerPid:\t0\n' not in f.read()
                    except:
                        return False
            
            # Détecter les modifications de code
            def verify_code_integrity():
                code_hash = hashlib.sha256(
                    open(__file__, 'rb').read()
                ).hexdigest()
                return code_hash == self._get_original_hash()
            
            if detect_debugger():
                raise RuntimeError("Débogage détecté")
            
            if not verify_code_integrity():
                raise RuntimeError("Intégrité du code compromise")
            
            # Désactiver le traçage
            sys.settrace(lambda *args, **kwargs: None)
            
        except Exception as e:
            raise RuntimeError(f"Violation de sécurité: {str(e)}")

    def _get_original_hash(self) -> str:
        """Récupère le hash original du code."""
        try:
            response = requests.get(
                'https://api.carfast.com/code_hash',
                headers={'License-Key': self.license_key},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()['hash']
        except:
            pass
        
        # Fallback vers un hash local
        return "local_hash_for_development"

class AntiPiracy:
    """Mesures anti-piratage supplémentaires."""
    
    @staticmethod
    def detect_virtualization() -> bool:
        """Détecte si l'application s'exécute dans un environnement virtualisé."""
        try:
            if os.name == 'nt':
                import wmi
                c = wmi.WMI()
                
                # Vérifier les marqueurs de virtualisation
                for item in c.Win32_ComputerSystem():
                    if item.Manufacturer in ['VMware, Inc.', 'Microsoft Corporation', 'innotek GmbH']:
                        return True
                        
                # Vérifier les processus suspects
                processes = set(p.Name.lower() for p in c.Win32_Process())
                vm_processes = {'vmtoolsd.exe', 'vboxservice.exe', 'vboxtray.exe'}
                if vm_processes & processes:
                    return True
            else:
                # Vérifier les fichiers caractéristiques
                vm_files = [
                    '/sys/class/dmi/id/product_name',
                    '/sys/class/dmi/id/sys_vendor',
                    '/proc/scsi/scsi'
                ]
                for file in vm_files:
                    if os.path.exists(file):
                        with open(file) as f:
                            content = f.read().lower()
                            if any(x in content for x in ['vmware', 'virtualbox', 'qemu']):
                                return True
                                
            return False
        except:
            return False
    
    @staticmethod
    def detect_tampering() -> bool:
        """Détecte les tentatives de modification du code."""
        try:
            # Vérifier les outils de décompilation
            suspicious_processes = {
                'ida64.exe', 'x64dbg.exe', 'ollydbg.exe',
                'dnspy.exe', 'de4dot.exe', 'fiddler.exe'
            }
            
            if os.name == 'nt':
                import wmi
                c = wmi.WMI()
                running_processes = set(p.Name.lower() for p in c.Win32_Process())
                if suspicious_processes & running_processes:
                    return True
            else:
                import psutil
                running_processes = set(p.name().lower() for p in psutil.process_iter())
                if suspicious_processes & running_processes:
                    return True
            
            return False
        except:
            return False
    
    @staticmethod
    def detect_hooking() -> bool:
        """Détecte les tentatives d'injection de code."""
        try:
            if os.name == 'nt':
                import ctypes
                
                # Vérifier les hooks d'API Windows
                kernel32 = ctypes.windll.kernel32
                ntdll = ctypes.windll.ntdll
                
                # Vérifier si certaines fonctions sont hookées
                original_functions = {
                    'CreateFileW': kernel32.CreateFileW,
                    'ReadFile': kernel32.ReadFile,
                    'WriteFile': kernel32.WriteFile
                }
                
                for name, func in original_functions.items():
                    # Vérifier si l'adresse de la fonction a été modifiée
                    current_addr = ctypes.cast(func, ctypes.c_void_p).value
                    if AntiPiracy._is_hooked_address(current_addr):
                        return True
            
            return False
        except:
            return False
    
    @staticmethod
    def _is_hooked_address(addr: int) -> bool:
        """Vérifie si une adresse mémoire semble être hookée."""
        try:
            if os.name == 'nt':
                # Les hooks sont souvent dans des régions mémoire suspectes
                import ctypes
                
                class MEMORY_BASIC_INFORMATION(ctypes.Structure):
                    _fields_ = [
                        ("BaseAddress", ctypes.c_void_p),
                        ("AllocationBase", ctypes.c_void_p),
                        ("AllocationProtect", ctypes.c_ulong),
                        ("RegionSize", ctypes.c_size_t),
                        ("State", ctypes.c_ulong),
                        ("Protect", ctypes.c_ulong),
                        ("Type", ctypes.c_ulong),
                    ]
                
                mbi = MEMORY_BASIC_INFORMATION()
                if ctypes.windll.kernel32.VirtualQuery(
                    addr,
                    ctypes.byref(mbi),
                    ctypes.sizeof(mbi)
                ):
                    # Vérifier si la mémoire est dans une région suspecte
                    return mbi.Type != 0x1000000  # MEM_IMAGE
            
            return False
        except:
            return False

def check_security() -> Tuple[bool, str]:
    """
    Vérifie toutes les mesures de sécurité.
    
    Returns:
        Tuple[bool, str]: (sécurité_ok, message)
    """
    try:
        # Vérifier la virtualisation
        if AntiPiracy.detect_virtualization():
            return False, "Environnement virtualisé détecté"
        
        # Vérifier les modifications
        if AntiPiracy.detect_tampering():
            return False, "Tentative de modification détectée"
        
        # Vérifier l'injection de code
        if AntiPiracy.detect_hooking():
            return False, "Tentative d'injection détectée"
        
        return True, "Vérification de sécurité réussie"
        
    except Exception as e:
        return False, f"Erreur lors de la vérification: {str(e)}"
