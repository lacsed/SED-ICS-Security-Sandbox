def print_opc_server(semaphore):
    semaphore.release()

def print_opc_client(semaphore1, semaphore2):
    semaphore1.acquire()
    semaphore2.release()

def print_input_valve(semaphore2, semaphore3):
    semaphore2.acquire()
    semaphore3.release()

def print_level_high(semaphore3, semaphore4):
    semaphore3.acquire()
    semaphore4.release()

def print_output_valve(semaphore4):
    semaphore4.acquire()
