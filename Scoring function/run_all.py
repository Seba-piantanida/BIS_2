import concurrent.futures
import threading

import websites_scoring 
import linkedin_scoring
import aggregate_by_company
import company_ranking

event_script2_completed = threading.Event()
event_all_previous_completed = threading.Event()

def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        
        future_script1 = executor.submit(websites_scoring.main)
        future_script2 = executor.submit(linkedin_scoring.main)

        
        def on_script2_completed(future):
            
            event_script2_completed.set()

        future_script2.add_done_callback(on_script2_completed)

        
        def run_script3():
            event_script2_completed.wait()  
            aggregate_by_company.main()

        future_script3 = executor.submit(run_script3)

        def on_all_previous_completed(future):
            if future_script1.done() and future_script2.done() and future_script3.done():
                
                event_all_previous_completed.set()

        future_script1.add_done_callback(on_all_previous_completed)
        future_script2.add_done_callback(on_all_previous_completed)
        future_script3.add_done_callback(on_all_previous_completed)

        
        def run_script4():
            event_all_previous_completed.wait()  
            company_ranking.main()

        future_script4 = executor.submit(run_script4)

        
        concurrent.futures.wait([future_script1, future_script2, future_script3, future_script4])

if __name__ == "__main__":
    main()
