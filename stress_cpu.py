import threading
import math

def cpu_stress():
    while True:
        math.sqrt(12345 * 6789)

threads = []

# Nombre de threads à créer pour stresser le CPU
num_threads = 4  # Vous pouvez ajuster ce nombre en fonction de votre besoin

for i in range(num_threads):
    thread = threading.Thread(target=cpu_stress)
    thread.start()
    threads.append(thread)

# Empêche le script de se terminer immédiatement
for thread in threads:
    thread.join()
