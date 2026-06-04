import ipaddress
import threading
from queue import Queue
from mxc.core.color import print_info, print_success, print_error

class Scanner:
    def __init__(self, threads=50):
        self.threads = threads
        self.queue = Queue()
        self.results = []
        self.lock = threading.Lock()
    
    def expand_cidr(self, cidr):
        """Expandir CIDR a lista de IPs"""
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            return [str(ip) for ip in network.hosts()]
        except Exception as e:
            print_error(f"CIDR inválido: {cidr} - {e}")
            return []
    
    def worker(self, func, *args, **kwargs):
        """Worker para multithreading"""
        while not self.queue.empty():
            try:
                target = self.queue.get()
                result = func(target, *args, **kwargs)
                with self.lock:
                    self.results.append((target, result))
                self.queue.task_done()
            except Exception as e:
                print_error(f"Error en worker: {e}")
                self.queue.task_done()
    
    def scan(self, targets, func, *args, **kwargs):
        """Escaneo masivo con multithreading"""
        # Expandir targets (pueden ser IPs individuales o CIDRs)
        all_targets = []
        for target in targets:
            if '/' in target:
                all_targets.extend(self.expand_cidr(target))
            else:
                all_targets.append(target)
        
        print_info(f"Escaneando {len(all_targets)} hosts con {self.threads} hilos...")
        
        # Llenar queue
        for target in all_targets:
            self.queue.put(target)
        
        # Crear y empezar hilos
        thread_list = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.worker, args=(func, *args), kwargs=kwargs)
            t.start()
            thread_list.append(t)
        
        # Esperar a que terminen
        self.queue.join()
        
        return self.results
